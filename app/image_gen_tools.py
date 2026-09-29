"""Image generation tools for WiesnWingman: Generates commemorative Bierbank Badges / Survivor Postcards."""
import uuid
from typing import Any, Dict, Optional
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools.tool_context import ToolContext

# Hardcoded project configuration
GCP_PROJECT_ID = "qwiklabs-gcp-04-06c7bc5ed227"
BUCKET_NAME = "wiesn-wingman-media-qwiklabs"
MODEL_NAME = "gemini-3.1-flash-lite-image"
MODEL_LOCATION = "global"


async def generate_bierbank_survivor_badge(
    attendee_name: str,
    tent_name: str,
    drinks_had: int,
    tech_role: str,
    tool_context: ToolContext,
    custom_title: Optional[str] = "Official Bierbank Survivor & Tech Pioneer",
) -> Dict[str, Any]:
    """Generates an authentic Bavarian commemorative Oktoberfest postcard / Bierbank Survivor badge using gemini-3.1-flash-lite-image in the global region.

    Saves the generated image to session artifacts via tool_context.save_artifact (so it appears in the Playground's Artifacts panel)
    and uploads the image bytes directly to public Google Cloud Storage, returning its public HTTPS URL.

    Args:
        attendee_name: Name of the attendee or team.
        tent_name: Name of the Oktoberfest tent (e.g. 'Hacker-Pschorr', 'Schottenhamel', 'Paulaner').
        drinks_had: Number of Maß beers conquered.
        tech_role: Attendee's tech profession or title (e.g. 'Cloud Engineer', 'ML Researcher', 'Full-stack Dev').
        tool_context: Injected ADK ToolContext used to save session artifacts.
        custom_title: Optional honorary Bavarian title.

    Returns:
        A dictionary with the public Cloud Storage image URL, artifact filename, and badge stats.
    """
    image_prompt = (
        f"Generate a vintage 19th-century Bavarian Munich Oktoberfest art-nouveau commemorative badge and souvenir certificate. "
        f"In the center, a festive golden emblem celebrating '{attendee_name}' as '{custom_title}'. "
        f"Detailed Bavarian blue-and-white rhombuses border, pretzel illustrations, hops, foaming beer steins with frothy crowns, "
        f"and the historic rustic wooden festival tent '{tent_name}' in the background. "
        f"Typography reads '{tech_role}', '{drinks_had} Maß Conquered', and 'WiesnWingman Verified'. "
        f"Rich warm colors, nostalgic lithograph poster aesthetic, high resolution, intricate vector details."
    )

    try:
        # 1. Generate image using gemini-3.1-flash-lite-image in the global region
        client = genai.Client(vertexai=True, project=GCP_PROJECT_ID, location=MODEL_LOCATION)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=image_prompt
        )

        image_bytes = None
        mime_type = "image/jpeg"
        if response.candidates:
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        image_bytes = part.inline_data.data
                        if hasattr(part.inline_data, "mime_type") and part.inline_data.mime_type:
                            mime_type = part.inline_data.mime_type
                        break
                if image_bytes:
                    break

        if not image_bytes:
            return {
                "status": "error",
                "message": "Model did not return image bytes."
            }

        # 2. Save image as an ADK session artifact via tool_context.save_artifact
        ext = "png" if "png" in mime_type.lower() else "jpg"
        unique_id = uuid.uuid4().hex[:8]
        artifact_filename = f"bierbank_badge_{unique_id}.{ext}"

        artifact_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )
        try:
            await tool_context.save_artifact(
                filename=artifact_filename,
                artifact=artifact_part
            )
        except Exception as artifact_err:
            print(f"Note: artifact save warning (e.g. runner without artifact store): {artifact_err}")

        # 3. Upload image bytes directly to the public Cloud Storage bucket
        object_key = f"badges/{artifact_filename}"
        storage_client = storage.Client(project=GCP_PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(object_key)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{object_key}"

        return {
            "status": "success",
            "attendee_name": attendee_name,
            "tent": tent_name,
            "drinks_had": drinks_had,
            "tech_role": tech_role,
            "badge_title": custom_title,
            "artifact_name": artifact_filename,
            "public_url": public_url,
            "image_markdown": f"![Bierbank Survivor Badge - {attendee_name}]({public_url})",
            "message": f"Badge saved as artifact '{artifact_filename}' and uploaded to Cloud Storage: {public_url}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Image generation failed: {str(e)}"
        }
