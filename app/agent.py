# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types


MODEL = "gemini-3.8-flash"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


from app.firestore_tools import (
    list_oktoberfest_tents,
    get_oktoberfest_tent_details,
    add_or_update_oktoberfest_tent,
    list_wiesn_rules,
    get_wiesn_rule_detail,
)
from app.song_tools import (
    identify_song_and_lyrics,
    list_popular_wiesn_anthems,
    identify_song_from_audio,
)
from app.pacer_tools import (
    calculate_drink_pacer_and_bac,
)
from app.networking_tools import (
    generate_bierbank_icebreaker,
)
from app.menu_tools import (
    get_tent_food_menu,
    calculate_bill_and_tip_split,
)
from app.image_gen_tools import (
    generate_bierbank_survivor_badge,
)
from app.transit_tools import (
    check_tent_occupancy_barometer,
    compute_live_transit_escape_route,
    get_live_oktoberfest_news_and_alerts,
)


from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from app.a2ui_utils import a2ui_callback


# WRITE: after each turn, send the session to Memory Bank for extraction.
async def generate_memories_callback(callback_context: CallbackContext):
    await callback_context.add_session_to_memory()
    return None


try:
    from a2ui.schema.manager import A2uiSchemaManager
    from a2ui.basic_catalog.provider import BasicCatalog

    schema_manager = A2uiSchemaManager(
        version="0.8",
        catalogs=[BasicCatalog.get_config("0.8")],
    )

    instruction = schema_manager.generate_system_prompt(
        role_description="""You are WiesnWingman (Bierbank Copilot), a personal AI wingman helping attendees navigate Oktoberfest tents, network on beer benches, and survive the festivities.
You remember the user's stated preferences and facts from previous conversations and use them to personalize your responses.
In particular, ALWAYS pay close attention to, remember, and adapt to:
- Beer preferences: Preferred breweries (e.g. Augustiner, Hacker-Pschorr, Paulaner), favorite beer types/styles (Festbier, Helles, Weißbier, Radler, Alkoholfrei), and alcohol tolerance/pacing limits.
- Song preferences: Favorite brass band tent anthems (Ein Prosit, Fürstenfeld, Fliegerlied, Sierra Madre, Sweet Caroline) and sing-along habits.
- Public transport preferences: Preferred Munich transit routes (U-Bahn lines U4/U5/U3/U6, S-Bahn, Tram, Bus), preferred escape stations (Theresienwiese, Schwanthalerhöhe, Goetheplatz, Hauptbahnhof), and walking tolerances.
Also remember any stated dietary restrictions, tech background, and table companions.

You have superpowers across:
1. Tent knowledge: Full information on all 14 large Oktoberfest tents (brewery, beers, atmosphere, crowd profiles, signature dishes, capacity, standing rules, transit tips) stored in Firestore.
2. Universal Oktoberfest rules & etiquette: Standing guidelines, Maßkrug theft fines, walk-in unreserved quotas, tipping, and toasting rituals.
3. Song Whisperer: Identifying brass band anthems (Ein Prosit, Fürstenfeld, Fliegerlied, Sierra Madre, Country Roads), providing German lyrics, English phonetics, and bench ritual actions.
4. Stamina Pacer: Calculating alcohol pacing, estimated Blood Alcohol Content (BAC / Promille), hours until sober, and evaluating readiness for tomorrow morning's commitments (e.g. hackathon demo, presentations).
5. Tech Networking on the Bierbank: Generating tailored tech icebreakers (automotive, cloud, AI/ML, cybersecurity, frontend) and cultural etiquette tips for striking up conversations with table neighbors.
6. Menu & Bill Splitting: Catalog of traditional Bavarian tent dishes (Hendl, Schweinshaxe, Steckerlfisch, Obatzda, Käsespätzle, vegan options) and calculating cash bill/tip splits for the table.
7. Commemorative Bierbank Badge / Survivor Certificate: Generating vintage-illustrated Bavarian souvenir badges with Imagen/Multimodal image gen and publishing them to Cloud Storage for public viewing.

Use the available tools whenever relevant to fetch data, compute calculations, generate badges, and guide the user.""",
        workflow_description="Analyze the request, call relevant tools, and return structured A2UI display cards when presenting tent details, menus, survivor badges, pacer stats, songs, or bills.",
        ui_description=(
            "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
            "Never nest a Card inside a Card. "
            "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
            "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
            "nothing in adk web). "
            "You may include one Image component, but only when you have a public https "
            "URL for the image (for example the URL an image tool returns after uploading "
            "to a public bucket). Set the Image url to that exact https link, for example "
            "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
            "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
            "not have a public URL, add a short Text line noting the image instead. "
            "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
            "headings and emphasis. "
            "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
            "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
        ),
        include_schema=True,
        include_examples=True,
    )
except ImportError:
    from app.a2ui_instruction import instruction


root_agent = Agent(
    # Keep in sync with agents-cli-manifest.yaml: agents-cli derives this name
    # from the project `name:` recorded there, and telemetry reports it as
    # gen_ai.agent.name. Renaming the agent only here makes the two disagree,
    # and anything selecting traces by name stops finding this agent's.
    name="simple_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        PreloadMemoryTool(),
        get_weather,
        get_current_time,
        list_oktoberfest_tents,
        get_oktoberfest_tent_details,
        add_or_update_oktoberfest_tent,
        list_wiesn_rules,
        get_wiesn_rule_detail,
        identify_song_and_lyrics,
        list_popular_wiesn_anthems,
        identify_song_from_audio,
        calculate_drink_pacer_and_bac,
        generate_bierbank_icebreaker,
        get_tent_food_menu,
        calculate_bill_and_tip_split,
        generate_bierbank_survivor_badge,
        check_tent_occupancy_barometer,
        compute_live_transit_escape_route,
        get_live_oktoberfest_news_and_alerts,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
