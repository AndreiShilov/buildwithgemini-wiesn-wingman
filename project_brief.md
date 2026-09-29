# My agent: WiesnWingman (Bierbank Copilot)
One-liner: A conversational AI wingman that helps tech conference attendees navigate Oktoberfest tents, network effortlessly on beer benches, and survive the night with a catalog of tents, songs, traditional Bavarian dishes, and etiquette guidelines.

Tool coverage:
- Memory: User profile & session state (conference role, company/tech stack, sobriety/pacing goals, morning commitments like hackathon pitch time, drinks consumed so far, dietary restrictions).
- Tools:
    1. Bavarian dialect translator & cultural etiquette advisor (`translate_bavarian`, `get_tent_rules`).
    2. Brass band song prompter & lyrics lookup (`identify_song_and_lyrics`).
    3. Networking icebreaker generator grounded in tent vibe + neighbor's company/domain (`generate_icebreaker`).
    4. Stamina/alcohol pacer & transit router (`log_drink_and_check_pace`, `get_transit_route`).
- Catalog/UI:
    - Tent directory & atmosphere guides (Hacker-Pschorr, Schottenhamel, Paulaner, etc.).
    - Traditional tent food menu cards (with vegetarian/vegan badges and price/tipping breakdown).
    - Brass band sing-along songbook cards (German & phonetic lyrics).
- Image gen: Generates a commemorative vintage Bavarian postcard or personalized "Bierbank Badge / Survivor Certificate" (e.g. customized cartoon caricature in Lederhosen/Dirndl with stats).
- Sandbox: Blood alcohol content (BAC) estimation formula & bill/tip split calculation with local currency rounding.

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): Code sandbox for BAC & bill-splitting calculations, audio input for brass band song/dialect recognition (Multimodal Live API), MVG transit route lookup.
