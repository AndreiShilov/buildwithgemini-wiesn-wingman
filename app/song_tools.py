"""Song Whisperer tools for WiesnWingman: Oktoberfest brass band sing-along prompter."""
from typing import Any, Dict, List, Optional

WIESN_SONGS_CATALOG = [
    {
        "id": "ein-prosit",
        "title": "Ein Prosit der Gemütlichkeit",
        "artist_origin": "Traditional Bavarian Toasting Anthem (Bernhard Stern)",
        "frequency": "Played every 15-20 minutes in all tents",
        "german_lyrics": (
            "Ein Prosit, ein Prosit\n"
            "Der Gemütlichkeit!\n"
            "Ein Prosit, ein Prosit\n"
            "Der Gemütlichkeit!\n"
            "(Band shout: Oans, zwoa, drei, Gsuffa!)"
        ),
        "phonetic_guide": (
            "Ine PRO-zit, ine PRO-zit\n"
            "Dair geh-MEET-lish-kite!\n"
            "Ine PRO-zit, ine PRO-zit\n"
            "Dair geh-MEET-lish-kite!\n"
            "(Shout: Ohnss, tsvy, dry, ZOO-fah!)"
        ),
        "english_translation": (
            "A toast, a toast\n"
            "To coziness, good times, and fellowship!\n"
            "A toast, a toast\n"
            "To coziness, good times, and fellowship!\n"
            "(One, two, three, chug/drink up!)"
        ),
        "ritual_action": (
            "1. Stand up immediately on your bench when you hear the opening horn.\n"
            "2. Sway your Maßkrug left-to-right to the rhythm of the music.\n"
            "3. Clink bottom-to-bottom with table neighbors on 'Gsuffa!'\n"
            "4. Make direct eye contact with each person you clink with (failing eye contact is 7 years bad luck!).\n"
            "5. Take a generous sip, sit back down, and high five your table."
        )
    },
    {
        "id": "fuerstenfeld",
        "title": "Fürstenfeld (I will ham noch Fürstenfeld)",
        "artist_origin": "S.T.S. (Austrian Folk-Rock Classic)",
        "frequency": "Played 3-5 times per evening, huge sing-along anthem",
        "german_lyrics": (
            "I will ham noch Fürstenfeld!\n"
            "I brauch ka große Welt,\n"
            "I will ham noch Fürstenfeld,\n"
            "I will ham!"
        ),
        "phonetic_guide": (
            "Ee vill hahm nokh FEER-sten-feld!\n"
            "Ee browkh kah GROH-seh velt,\n"
            "Ee vill hahm nokh FEER-sten-feld,\n"
            "Ee vill hahm!"
        ),
        "english_translation": (
            "I want to go home to Fürstenfeld!\n"
            "I don't need the big wide world,\n"
            "I want to go home to Fürstenfeld,\n"
            "I want to go home!"
        ),
        "ritual_action": (
            "1. Wrap arms around your bench neighbors' shoulders.\n"
            "2. Sway side-to-side in unison with the entire tent.\n"
            "3. Belter out the chorus with maximum passion into the air."
        )
    },
    {
        "id": "fliegerlied",
        "title": "Fliegerlied (So a schöner Tag)",
        "artist_origin": "DONIKKL",
        "frequency": "Played late afternoon through evening; mandatory choreographed dance",
        "german_lyrics": (
            "Und ich flieg, flieg, flieg wie ein Flieger,\n"
            "Bin so stark, stark, stark wie ein Tiger,\n"
            "Und so groß, groß, groß wie 'ne Giraffe,\n"
            "So hoch, wo-o-oh!\n"
            "Und ich spring, spring, spring immer wieder,\n"
            "Und ich schwimm, schwimm, schwimm zu dir rüber,\n"
            "Und ich nehm, nehm, nehm dich bei der Hand,\n"
            "Weil ich dich mag, und ich sag:\n"
            "Heut ist so ein schöner Tag! La-la-la-la-la!"
        ),
        "phonetic_guide": (
            "Oont ikh fleeg, fleeg, fleeg vee ine FLEE-ger,\n"
            "Bin zoh shtahrk, shtahrk, shtahrk vee ine TEE-ger,\n"
            "Oont zoh grohs, grohs, grohs vee nuh zhee-RAH-feh,\n"
            "Zoh hokh, voh-oh-oh!\n"
            "Oont ikh shpring, shpring, shpring im-mer VEE-der,\n"
            "Oont ikh shwim, shwim, shwim tsoo deer ROO-ber,\n"
            "Oont ikh naym, naym, naym dikh by dair hahnt,\n"
            "Vyle ikh dikh mahk, oont ikh zahk:\n"
            "Hoyt ist zoh ine SHER-ner tahk!"
        ),
        "english_translation": (
            "And I fly, fly, fly like an airplane,\n"
            "Am so strong, strong, strong like a tiger,\n"
            "And as tall, tall, tall as a giraffe,\n"
            "So high, wo-o-oh!\n"
            "And I jump, jump, jump again and again,\n"
            "And I swim, swim, swim over to you,\n"
            "And I take, take, take you by the hand,\n"
            "Because I like you, and I say:\n"
            "Today is such a beautiful day!"
        ),
        "ritual_action": (
            "Do the choreographed actions while standing on the bench:\n"
            "• 'Flieg': Spread arms like airplane wings\n"
            "• 'Stark': Flex your biceps like a bodybuilder\n"
            "• 'Groß': Reach both hands high in the sky\n"
            "• 'Spring': Jump up and down on the bench\n"
            "• 'Schwimm': Do breaststroke swimming motions\n"
            "• 'Nehm dich bei der Hand': Grab neighbor's hand and spin!"
        )
    },
    {
        "id": "sierra-madre",
        "title": "Sierra Madre del Sur",
        "artist_origin": "Schürzenjäger",
        "frequency": "Played right before tent closing (~10:15 PM), the emotional finale",
        "german_lyrics": (
            "Sierra, Sierra Madre del Sur,\n"
            "Sierra, Sierra Madre!\n"
            "Wenn der Morgen erwacht und das Tal noch versinkt,\n"
            "Und die Sonne die Berge vergold't..."
        ),
        "phonetic_guide": (
            "See-AIR-ah, See-AIR-ah MAH-dray del zoor,\n"
            "See-AIR-ah, See-AIR-ah MAH-dray!\n"
            "Ven dair MOR-gen er-VAKHT oont dahs tahl nokh fair-ZINKT..."
        ),
        "english_translation": (
            "Sierra, Sierra Madre of the South,\n"
            "Sierra, Sierra Madre!\n"
            "When morning awakens and the valley still rests,\n"
            "And the sun turns the mountains to gold..."
        ),
        "ritual_action": (
            "1. The lights in the tent dim.\n"
            "2. Everyone turns on their smartphone flashlights (or waves sparklers/lighters).\n"
            "3. Put arms around friends and strangers alike, wave lights slowly back and forth.\n"
            "4. The final emotional farewell to the tent for the night."
        )
    },
    {
        "id": "country-roads",
        "title": "Take Me Home, Country Roads",
        "artist_origin": "John Denver (Oktoberfest Brass Anthem version)",
        "frequency": "Played every 1-2 hours in every major tent",
        "german_lyrics": (
            "Country roads, take me home\n"
            "To the place I belong!\n"
            "West Virginia, mountain mama,\n"
            "Take me home, country roads!"
        ),
        "phonetic_guide": (
            "CUN-tree roads, take me home\n"
            "To the place I be-LONG!\n"
            "West Vir-JIN-ya, mountain mama,\n"
            "Take me home, CUN-tree roads!"
        ),
        "english_translation": "English original - international crowd unites!",
        "ritual_action": (
            "1. Stand on bench, pump your Maß in the air on every beat.\n"
            "2. Belt the chorus at top volume together with 10,000 people."
        )
    },
    {
        "id": "sweet-caroline",
        "title": "Sweet Caroline",
        "artist_origin": "Neil Diamond (Oktoberfest Brass Edition)",
        "frequency": "Prime time party anthem (8 PM - 10 PM)",
        "german_lyrics": (
            "Sweet Caroline... (Audience: BA! BA! BA!)\n"
            "Good times never seemed so good! (Audience: SO GOOD! SO GOOD! SO GOOD!)\n"
            "I've been inclined... (Audience: BA! BA! BA!)\n"
            "To believe they never would!"
        ),
        "phonetic_guide": "Sing in English, hit the loud crowd chants: 'BAH! BAH! BAH!' and 'SO GOOD! SO GOOD!'",
        "english_translation": "Classic party sing-along.",
        "ritual_action": (
            "Raise fists and shout 'BAH! BAH! BAH!' and 'SO GOOD! SO GOOD! SO GOOD!' right in time with the horns."
        )
    }
]


def identify_song_and_lyrics(song_query: str) -> Dict[str, Any]:
    """Looks up brass band sing-along song lyrics, English phonetic guide, translations, and bench rituals for Oktoberfest anthems.

    Args:
        song_query: The name, partial title, or lyric snippet of the song (e.g. 'Ein Prosit', 'Fliegerlied', 'Country Roads', 'Fürstenfeld', 'Sierra Madre', 'Sweet Caroline', 'prosit', 'toast', 'tiger').

    Returns:
        A dictionary with the song title, German lyrics, phonetic pronunciation guide, English meaning, and step-by-step tent ritual actions.
    """
    q = song_query.lower().strip()
    
    # 1. Exact or partial match on catalog
    for s in WIESN_SONGS_CATALOG:
        if (q in s["id"] or 
            q in s["title"].lower() or 
            q in s["german_lyrics"].lower() or 
            q in s["ritual_action"].lower()):
            return {
                "status": "found",
                "song": s
            }
            
    # Default fallback: list available anthems
    available = [f"{s['title']} ({s['id']})" for s in WIESN_SONGS_CATALOG]
    return {
        "status": "not_found",
        "message": f"Couldn't identify a specific Wiesn anthem matching '{song_query}'.",
        "available_anthems": available,
        "tip": "Try 'Ein Prosit', 'Fliegerlied', 'Fürstenfeld', 'Sierra Madre', or 'Country Roads'."
    }


def list_popular_wiesn_anthems() -> List[Dict[str, str]]:
    """Returns a list of the top Oktoberfest brass band anthems and when they are played in the tents."""
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "frequency": s["frequency"],
            "origin": s["artist_origin"]
        }
        for s in WIESN_SONGS_CATALOG
    ]


async def identify_song_from_audio(
    audio_source: str,
    mime_type: Optional[str] = "audio/wav",
) -> Dict[str, Any]:
    """Listens to an audio recording of a brass band or crowd singing at Oktoberfest and identifies the anthem, lyrics, and bench rituals.

    Accepts:
      - A web URL to an audio file (http:// or https://)
      - A Google Cloud Storage URI (gs://bucket/path.mp3)
      - A base64-encoded audio string (e.g. from browser microphone)
      - A local audio file path

    Args:
        audio_source: URL, GCS URI, file path, or base64-encoded audio data of the brass band audio snippet.
        mime_type: MIME type of the audio (e.g. 'audio/wav', 'audio/mp3', 'audio/ogg', 'audio/webm', 'audio/m4a'). Defaults to 'audio/wav'.

    Returns:
        A dictionary with the identified song, confidence analysis, lyrics, phonetic pronunciation, and bierbank ritual actions.
    """
    import base64
    import os
    import urllib.request
    from google import genai
    from google.genai import types

    audio_bytes = None
    resolved_mime = mime_type or "audio/wav"

    try:
        # 1. Handle HTTP / HTTPS URL
        if audio_source.startswith("http://") or audio_source.startswith("https://"):
            req = urllib.request.Request(audio_source, headers={"User-Agent": "WiesnWingman/1.0"})
            with urllib.request.urlopen(req) as resp:
                audio_bytes = resp.read()
                content_type = resp.headers.get("Content-Type")
                if content_type:
                    resolved_mime = content_type.split(";")[0].strip()

        # 2. Handle Google Cloud Storage URI
        elif audio_source.startswith("gs://"):
            from google.cloud import storage
            parts = audio_source[5:].split("/", 1)
            bucket_name, blob_name = parts[0], parts[1]
            client_gcs = storage.Client(project="qwiklabs-gcp-04-06c7bc5ed227")
            bucket = client_gcs.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            audio_bytes = blob.download_as_bytes()
            if blob.content_type:
                resolved_mime = blob.content_type

        # 3. Handle Local File Path
        elif os.path.exists(audio_source):
            with open(audio_source, "rb") as f:
                audio_bytes = f.read()

        # 4. Handle Base64 string
        else:
            cleaned = audio_source.strip()
            if "," in cleaned and "base64" in cleaned:
                # data:audio/wav;base64,...
                header, data = cleaned.split(",", 1)
                cleaned = data
                if "audio/" in header:
                    resolved_mime = header.split(";")[0].replace("data:", "")
            audio_bytes = base64.b64decode(cleaned)

    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not load audio data from source: {str(e)}",
            "tip": "Provide a valid URL, file path, GCS URI, or base64 audio string."
        }

    if not audio_bytes:
        return {
            "status": "error",
            "message": "Empty audio content provided.",
        }

    # Ask Gemini multimodal model to listen and identify the Oktoberfest song
    catalog_titles = [f"'{s['title']}' (id: {s['id']})" for s in WIESN_SONGS_CATALOG]
    prompt = (
        "You are an expert Bavarian brass band musician and Oktoberfest connoisseur. "
        "Listen carefully to this audio clip recorded in an Oktoberfest beer tent. "
        "Identify the song, brass melody, or sing-along anthem being played. "
        f"Our known Wiesn song catalog includes: {', '.join(catalog_titles)}. "
        "Respond in strictly valid JSON format with the following keys:\n"
        "{\n"
        '  "song_title": "<Identified song title>",\n'
        '  "catalog_id": "<one of the catalog IDs if matched, or null>",\n'
        '  "confidence": "<high | medium | low>",\n'
        '  "audio_analysis": "<Brief description of what instruments/singing was heard>",\n'
        '  "search_query": "<Best title or keyword to match against song database>"\n'
        "}"
    )

    try:
        client = genai.Client(vertexai=True, project="qwiklabs-gcp-04-06c7bc5ed227", location="global")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=resolved_mime),
                prompt,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        import json
        analysis = json.loads(response.text)
        
        # Cross reference with our catalog
        matched_song = None
        cid = analysis.get("catalog_id")
        if cid:
            for s in WIESN_SONGS_CATALOG:
                if s["id"] == cid:
                    matched_song = s
                    break

        if not matched_song and analysis.get("search_query"):
            res = identify_song_and_lyrics(analysis["search_query"])
            if res.get("status") == "found":
                matched_song = res["song"]

        return {
            "status": "identified",
            "identified_song": analysis.get("song_title"),
            "confidence": analysis.get("confidence", "high"),
            "audio_clues": analysis.get("audio_analysis", ""),
            "song_details": matched_song,
            "tip": "Display the lyrics and ritual actions so the user can immediately sing along and perform the bench moves!"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Gemini audio recognition error: {str(e)}"
        }
