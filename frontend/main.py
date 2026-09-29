"""Minimal FastAPI proxy for a deployed A2A agent (Agent Runtime, agents-cli 1.1.0+).

The browser talks ONLY to this proxy (same origin, no CORS, no GCP creds in the
browser). The proxy authenticates with Application Default Credentials and
forwards chat to the deployed agent over the A2A protocol, returning replies as
structured parts the chat UI knows how to show:

  * {"kind": "text", "text": ...}  -> a normal chat bubble
  * {"kind": "a2ui", "data": ...}  -> one A2UI message (beginRendering /
    surfaceUpdate); static/index.html renders these as a card.

Supports text queries and multimodal audio clips (base64 audio recorded in
the browser or uploaded).
"""

import base64
import os
import uuid

try:
    from dotenv import load_dotenv

    load_dotenv()
    load_dotenv("../.env")
except ImportError:
    pass

import google.auth
import google.auth.transport.requests
import httpx
from a2a.client import ClientConfig, ClientFactory

try:
    # a2a-sdk 0.3.x compatibility
    from a2a.types import (
        FilePart,
        TextPart,
        TransportProtocol,
    )
    _IS_A2A_V0 = True
except ImportError:
    _IS_A2A_V0 = False
    FilePart = None
    TextPart = None
    TransportProtocol = None

from a2a.types import (
    AgentCard,
    Message,
    Part,
    Role,
)

try:
    from a2a.types import SendMessageRequest, StreamResponse
    from google.protobuf.json_format import MessageToDict, ParseDict
except ImportError:
    SendMessageRequest = None
    StreamResponse = None
    MessageToDict = None
    ParseDict = None

try:
    from a2a.types import TaskArtifactUpdateEvent
except ImportError:
    TaskArtifactUpdateEvent = None

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

RESOURCE = os.environ.get(
    "AGENT_ENGINE_RESOURCE_NAME",
    "projects/919079686564/locations/us-central1/reasoningEngines/8653041611632017408",
)
# The agent's app directory (matches agent_directory in agents-cli-manifest.yaml).
AGENT_DIRECTORY = os.environ.get("AGENT_DIRECTORY", "app")
# Location is embedded in the resource name: projects/<p>/locations/<loc>/reasoningEngines/<id>.
LOCATION = RESOURCE.split("/locations/")[1].split("/")[0]

# A2A endpoint for an Agent Runtime deployment, via the Agent Engine HTTP
# passthrough. The card lives at the well-known path under this base.
A2A_BASE = (
    f"https://{LOCATION}-aiplatform.googleapis.com/reasoningEngines/v1/"
    f"{RESOURCE}/api/a2a/{AGENT_DIRECTORY}"
)
A2A_CARD_URL = f"{A2A_BASE}/.well-known/agent-card.json"

# The agent tags its A2UI data parts with this mime type.
_A2UI_MIME = "application/json+a2ui"

# One set of ADC credentials, refreshed per request (access tokens expire ~1h).
_creds, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)


def _auth_headers() -> dict[str, str]:
    _creds.refresh(google.auth.transport.requests.Request())
    return {
        "Authorization": f"Bearer {_creds.token}",
        "Content-Type": "application/json",
    }


app = FastAPI()


@app.exception_handler(Exception)
async def _json_errors(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "parts": [{"kind": "text", "text": f"Error: {type(exc).__name__}: {exc}"}]
        },
    )


# Reuse ONE A2A context per user so the agent remembers the conversation.
_contexts: dict[str, str] = {}
# Cache the agent card after the first fetch.
_card: AgentCard | None = None


async def _get_card(client: httpx.AsyncClient) -> AgentCard:
    global _card
    if _card is None:
        resp = await client.get(A2A_CARD_URL)
        resp.raise_for_status()
        card_json = resp.json()
        if ParseDict is not None and not _IS_A2A_V0:
            card = ParseDict(card_json, AgentCard(), ignore_unknown_fields=True)
            if getattr(card, "supported_interfaces", None):
                card.supported_interfaces[0].url = A2A_BASE
        else:
            card = AgentCard(**card_json)
            card.url = A2A_BASE
        _card = card
    return _card


def _extract_parts(parts: list) -> list[dict]:
    out: list[dict] = []
    for p in parts:
        # Protobuf Part from a2a-sdk 1.x
        if MessageToDict is not None and not isinstance(p, dict) and hasattr(p, "DESCRIPTOR"):
            d = MessageToDict(p)
            if d.get("text"):
                out.append({"kind": "text", "text": d["text"]})
            elif d.get("data") is not None:
                a2ui_data = d["data"]
                if isinstance(a2ui_data, dict) and "data" in a2ui_data:
                    inner = a2ui_data["data"]
                    if isinstance(inner, dict) and ("beginRendering" in inner or "surfaceUpdate" in inner):
                        a2ui_data = inner
                out.append({"kind": "a2ui", "data": a2ui_data})
            elif d.get("url"):
                out.append({"kind": "text", "text": d["url"]})
            continue

        # Dict representation
        if isinstance(p, dict):
            if p.get("text"):
                out.append({"kind": "text", "text": p["text"]})
            elif p.get("data") is not None:
                a2ui_data = p["data"]
                if isinstance(a2ui_data, dict) and "data" in a2ui_data:
                    inner = a2ui_data["data"]
                    if isinstance(inner, dict) and ("beginRendering" in inner or "surfaceUpdate" in inner):
                        a2ui_data = inner
                out.append({"kind": "a2ui", "data": a2ui_data})
            elif p.get("url"):
                out.append({"kind": "text", "text": p["url"]})
            continue

        # a2a-sdk 0.3.x object representation
        root = getattr(p, "root", p)
        if TextPart and isinstance(root, TextPart) and getattr(root, "text", None):
            out.append({"kind": "text", "text": root.text})
        elif getattr(root, "text", None) and isinstance(getattr(root, "text", None), str):
            out.append({"kind": "text", "text": root.text})
        elif getattr(root, "data", None) is not None:
            a2ui_data = root.data
            if isinstance(a2ui_data, dict) and "data" in a2ui_data:
                inner = a2ui_data["data"]
                if isinstance(inner, dict) and ("beginRendering" in inner or "surfaceUpdate" in inner):
                    a2ui_data = inner
            meta = getattr(root, "metadata", None) or {}
            mime = meta.get("mimeType") if isinstance(meta, dict) else None
            if mime == _A2UI_MIME or getattr(root, "media_type", None) == _A2UI_MIME or not mime:
                out.append({"kind": "a2ui", "data": a2ui_data})
        elif FilePart and isinstance(root, FilePart):
            uri = getattr(getattr(root, "file", None), "uri", None)
            if uri:
                out.append({"kind": "text", "text": uri})
    return out


@app.post("/chat")
async def chat(req: Request):
    body = await req.json()
    message = body.get("message", "")
    user_id = body.get("user_id") or "web-user"
    audio_b64 = body.get("audio")
    mime_type = body.get("mime_type", "audio/webm")

    audio_bytes: bytes | None = None
    clean_mime = (mime_type or "audio/webm").split(";")[0].strip()
    if audio_b64:
        try:
            if "," in audio_b64:
                audio_b64 = audio_b64.split(",", 1)[1]
            audio_bytes = base64.b64decode(audio_b64)
        except Exception as e:
            return JSONResponse({"parts": [{"kind": "text", "text": f"Error decoding audio: {e}"}]})

    parts: list[dict] = []

    async with httpx.AsyncClient(headers=_auth_headers(), timeout=120) as client:
        card = await _get_card(client)
        if _IS_A2A_V0:
            factory = ClientFactory(
                ClientConfig(
                    supported_transports=[
                        TransportProtocol.jsonrpc,
                        TransportProtocol.http_json,
                    ],
                    httpx_client=client,
                )
            )
            a2a_client = factory.create(card)

            msg_parts = []
            if message:
                msg_parts.append(Part(root=TextPart(text=message)))
            if not msg_parts:
                msg_parts.append(Part(root=TextPart(text="Listen to this Oktoberfest audio recording and identify the song, lyrics, and rituals.")))

            msg = Message(
                message_id=str(uuid.uuid4()),
                role=Role.user,
                parts=msg_parts,
                context_id=_contexts.get(user_id),
            )

            last_task = None
            got_artifact_update = False
            async for event in a2a_client.send_message(msg):
                if not isinstance(event, tuple):
                    continue
                task, update = event
                if task is not None:
                    last_task = task
                    if getattr(task, "context_id", None):
                        _contexts[user_id] = task.context_id
                if TaskArtifactUpdateEvent and isinstance(update, TaskArtifactUpdateEvent):
                    got_artifact_update = True
                    parts.extend(_extract_parts(update.artifact.parts))

            if not got_artifact_update and last_task is not None:
                for artifact in getattr(last_task, "artifacts", None) or []:
                    parts.extend(_extract_parts(artifact.parts))
        else:
            # a2a-sdk 1.x
            factory = ClientFactory(ClientConfig(streaming=True, httpx_client=client))
            a2a_client = factory.create(card)
            role_val = getattr(Role, "ROLE_USER", 1)

            msg_parts = []
            if message:
                msg_parts.append(Part(text=message))
            if audio_bytes:
                msg_parts.append(Part(raw=audio_bytes, media_type=clean_mime))
            if not msg_parts:
                msg_parts.append(Part(text="Listen to this Oktoberfest brass band recording, identify the anthem and lyrics, and explain the ritual actions."))

            msg = Message(
                message_id=str(uuid.uuid4()),
                role=role_val,
                parts=msg_parts,
                context_id=_contexts.get(user_id) or "",
            )
            req_msg = SendMessageRequest(message=msg) if SendMessageRequest else msg
            async for event in a2a_client.send_message(req_msg):
                if hasattr(event, "artifact_update") and event.HasField("artifact_update"):
                    update = event.artifact_update
                    if getattr(update, "context_id", None):
                        _contexts[user_id] = update.context_id
                    parts.extend(_extract_parts(update.artifact.parts))
                elif hasattr(event, "status_update") and event.HasField("status_update"):
                    if getattr(event.status_update, "context_id", None):
                        _contexts[user_id] = event.status_update.context_id
                elif hasattr(event, "task") and event.HasField("task"):
                    if getattr(event.task, "context_id", None):
                        _contexts[user_id] = event.task.context_id
                    for artifact in getattr(event.task, "artifacts", None) or []:
                        parts.extend(_extract_parts(artifact.parts))
                elif isinstance(event, tuple):
                    task, update = event
                    if task is not None and getattr(task, "context_id", None):
                        _contexts[user_id] = task.context_id
                    if hasattr(update, "artifact") and hasattr(update.artifact, "parts"):
                        parts.extend(_extract_parts(update.artifact.parts))

    if not parts:
        parts = [{"kind": "text", "text": "(The agent didn't return a reply.)"}]
    return JSONResponse({"parts": parts})


# Serve the chat UI (keep this mount last so /chat wins).
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
