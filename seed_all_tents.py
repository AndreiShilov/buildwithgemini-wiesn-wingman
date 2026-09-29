"""Comprehensive seeder for all 14 large Oktoberfest tents + universal festival rules in Firestore."""
from google.cloud import firestore

GCP_PROJECT_ID = "qwiklabs-gcp-04-06c7bc5ed227"

ALL_14_TENTS = [
    {
        "id": "hacker-pschorr",
        "name": "Hacker-Festzelt (Himmel der Bayern)",
        "brewery": "Hacker-Pschorr",
        "beer_served": "Hacker-Pschorr Oktoberfest Märzen (6.0%)",
        "vibe": "Young, energetic, famous painted ceiling depicting Bavarian heaven, rock & brass mix in evening.",
        "crowd": "Devs, locals, international party crowd, music lovers",
        "signature_dish": "Hendl (half roasted chicken) & Kaiserschmarrn",
        "table_capacity": 9300,
        "standing_rules": "Standing on benches encouraged; standing on tables is strictly prohibited (immediate eviction).",
        "transit_tip": "Exit via Theresienwiese or walk 7 mins to Goetheplatz (U3/U6) to skip U4/U5 stampede."
    },
    {
        "id": "schottenhamel",
        "name": "Schottenhamel Festhalle",
        "brewery": "Spaten-Franziskaner-Bräu",
        "beer_served": "Spaten Oktoberfestbier (6.3%)",
        "vibe": "Historic tent where the Mayor taps the first keg ('O'zapft is!'), traditional, tech & startup networking hub.",
        "crowd": "Founders, student fraternities, corporate groups, young professionals",
        "signature_dish": "Spanferkel (roast suckling pig) & Brezen",
        "table_capacity": 10000,
        "standing_rules": "Strict bench-only standing rules. Keep walkways clear for Bedienungen (waitstaff).",
        "transit_tip": "Closest to main entrance. Use Poccistraße (U3/U6) or Hackerbrücke (S-Bahn)."
    },
    {
        "id": "paulaner-festzelt",
        "name": "Paulaner Festzelt (Winzerer Fähndl)",
        "brewery": "Paulaner",
        "beer_served": "Paulaner Oktoberfestbier (6.0%)",
        "vibe": "Giant rotating beer mug on tower, cozy Gemütlichkeit, brass band classics, sing-along center.",
        "crowd": "Celebrities, FC Bayern players, seasoned Oktoberfest veterans, tech teams",
        "signature_dish": "Schweinshaxe (crispy pork knuckle) with potato dumpling & sauerkraut",
        "table_capacity": 8450,
        "standing_rules": "Benches only. Do NOT attempt to take beer mugs outside (police will fine for theft).",
        "transit_tip": "Walk south to Poccistraße (U3/U6) to avoid U4/U5 lines."
    },
    {
        "id": "augustiner-festhalle",
        "name": "Augustiner-Festhalle",
        "brewery": "Augustiner-Bräu",
        "beer_served": "Augustiner Oktoberfestbier (6.0%) from traditional wooden barrels (Hirschen)",
        "vibe": "The local favorite! Classic Bavarian Gemütlichkeit, friendly, authentic, and legendary smooth wooden-barrel beer.",
        "crowd": "Munich locals, seasoned Wiesn traditionalists, families by day, jovial crowds by night",
        "signature_dish": "Augustiner Spanferkel & crispy duck with red cabbage",
        "table_capacity": 8500,
        "standing_rules": "Standing on benches only. Respect the traditional atmosphere and elder locals.",
        "transit_tip": "Use Theresienwiese or walk towards Hackerbrücke (10 min)."
    },
    {
        "id": "hofbraeu-festzelt",
        "name": "Hofbräu-Festzelt",
        "brewery": "Staatliches Hofbräuhaus",
        "beer_served": "Hofbräu Oktoberfestbier (6.3%)",
        "vibe": "Massive international party epicenter! Huge standing area directly in front of the band, high decibel sing-alongs.",
        "crowd": "International travelers (Americans, Australians, Italians), exchange students, party animals",
        "signature_dish": "Bavarian Hendl, giant pretzels, and hearty sausage platters",
        "table_capacity": 9992,
        "standing_rules": "Features a large standing-only area ('Stehbereich'). Chugging beer while standing on benches triggers huge cheers but also security scrutiny.",
        "transit_tip": "Very crowded exits; walk to Goetheplatz (U3/U6) to avoid crush."
    },
    {
        "id": "loewenbraeu-festzelt",
        "name": "Löwenbräu-Festzelt",
        "brewery": "Löwenbräu",
        "beer_served": "Löwenbräu Oktoberfestbier (6.1%)",
        "vibe": "Marked by a 4.5m roaring lion over the door ('Löööwenbräu' roar every few mins). Vibrant sports and international party scene.",
        "crowd": "TSV 1860 Munich fans, international visitors, university students",
        "signature_dish": "Half duck, roast beef with onion relish (Zwiebelrostbraten)",
        "table_capacity": 8500,
        "standing_rules": "Benches only. Tables strictly forbidden. Keep main center aisle unobstructed.",
        "transit_tip": "Head north toward Hackerbrücke or south to Goetheplatz."
    },
    {
        "id": "ochsenbraterei",
        "name": "Ochsenbraterei (Spaten-Festhalle)",
        "brewery": "Spaten-Franziskaner-Bräu",
        "beer_served": "Spaten Oktoberfestbier (6.3%)",
        "vibe": "Famous spit-roasted whole oxen, slightly calmer traditional atmosphere, great acoustic brass music.",
        "crowd": "Foodies, engineering leaders, cross-generational festivalgoers",
        "signature_dish": "Whole roasted ox on a spit with red wine gravy & dumplings",
        "table_capacity": 7600,
        "standing_rules": "Bench standing only. Always toast neighbors when 'Ein Prosit' plays.",
        "transit_tip": "Theresienwiese station is right behind, or 10 min stroll to Schwanthalerhöhe."
    },
    {
        "id": "armbrustschuetzenzelt",
        "name": "Armbrustschützenzelt",
        "brewery": "Paulaner",
        "beer_served": "Paulaner Oktoberfestbier (6.0%)",
        "vibe": "Alpine hunting lodge decor with traditional crossbow competitions hosted in the rear shooting hall.",
        "crowd": "Crossbow marksmen, traditional folk costume clubs (Trachtenvereine), local families",
        "signature_dish": "Venison ragout, roasted chicken, and wild game specialties",
        "table_capacity": 7430,
        "standing_rules": "Standing on benches allowed during band sets. Observe quietness near the shooting range hall.",
        "transit_tip": "Use Theresienwiese or walk to Poccistraße."
    },
    {
        "id": "schuetzen-festzelt",
        "name": "Schützen-Festzelt",
        "brewery": "Löwenbräu",
        "beer_served": "Löwenbräu Oktoberfestbier (6.1%)",
        "vibe": "Located under the Bavaria statue, famous for shooting competitions, high-society chic, and delicious suckling pig.",
        "crowd": "Munich high society, sports shooters, stylish young crowd, tech execs",
        "signature_dish": "Spanferkel in dark beer sauce with potato salad (legendary reputation)",
        "table_capacity": 6500,
        "standing_rules": "Benches only. Popular balcony terrace area with strict table reservations.",
        "transit_tip": "Right under the Bavaria statue; walk to Schwanthalerhöhe (U4/U5) or Goetheplatz (U3/U6)."
    },
    {
        "id": "braeurosl",
        "name": "Pschorr-Bräurosl",
        "brewery": "Hacker-Pschorr",
        "beer_served": "Hacker-Pschorr Oktoberfestbier (6.0%)",
        "vibe": "Renowned for its in-house yodeler ('Bräurosl') and hosting 'Gay Sunday' on the first Sunday of Wiesn. High energy, singing.",
        "crowd": "LGBTQ+ community on first Sunday, traditionalists, party crowds, yodeling fans",
        "signature_dish": "Kassler, pork roasts, and organic Bavarian cheese platters (Obatzda)",
        "table_capacity": 8250,
        "standing_rules": "Benches only. Respect fellow guests dancing in the aisles when crowd surges.",
        "transit_tip": "Near northern perimeter; walk to Theresienwiese or Hackerbrücke."
    },
    {
        "id": "fischer-vroni",
        "name": "Fischer-Vroni",
        "brewery": "Augustiner-Bräu",
        "beer_served": "Augustiner Oktoberfestbier (6.0%) from wooden barrels",
        "vibe": "Cozy, distinctive maritime ship look with a 15-meter outdoor grill of fish on a stick. Pours Augustiner from wooden barrels!",
        "crowd": "Seafood connoisseurs, older Munich crowd, LGBTQ+ community on 2nd Monday (Rosa Wiesn)",
        "signature_dish": "Steckerlfisch (whole grilled mackerel/trout on a wooden skewer)",
        "table_capacity": 3862,
        "standing_rules": "Much smaller and cozier. Bench standing occurs later in evening.",
        "transit_tip": "Near main entrance; head to Theresienwiese or walk north toward Central Station."
    },
    {
        "id": "kaefer-wiesn-schaenke",
        "name": "Käfer Wiesn-Schänke",
        "brewery": "Paulaner",
        "beer_served": "Paulaner (served in ceramic steins / Kefer mugs)",
        "vibe": "Charming wooden farmhouse alpine chalet. The prime VIP and celebrity hotspot. Open late until 1:00 AM!",
        "crowd": "Celebrities, politicians, athletes, executives, VIP networkers",
        "signature_dish": "Crispy roast duck, beef tartare, gourmet Kaiserschmarrn",
        "table_capacity": 3433,
        "standing_rules": "Intimate setting, standing on benches rare; upscale tavern mingling. Stays open after 11 PM.",
        "transit_tip": "Stay until closing (1:00 AM) and take taxi or night buses/U-Bahn from Goetheplatz."
    },
    {
        "id": "kufflers-weinzelt",
        "name": "Kufflers Weinzelt (The Wine Tent)",
        "brewery": "N/A (Nymphenburger Sekt & Paulaner Weißbier)",
        "beer_served": "Paulaner Weißbier (until 9 PM only), over 15 wines and champagnes",
        "vibe": "The refuge for wine, champagne, and wheat beer lovers. Open until 1:00 AM with upbeat pop/rock bands.",
        "crowd": "Wine lovers, stylish partygoers, late-night revelers transitioning from beer tents",
        "signature_dish": "Thai duck curry, Flammkuchen, Kaiserschmarrn, cheese delicacies",
        "table_capacity": 2500,
        "standing_rules": "High tables and benches. Standing on chairs/tables forbidden.",
        "transit_tip": "Closes at 1:00 AM; night connections via Goetheplatz or Poccistraße."
    },
    {
        "id": "marstall",
        "name": "Marstall Festzelt",
        "brewery": "Spaten-Franziskaner-Bräu",
        "beer_served": "Spaten Oktoberfestbier (6.3%) & Franziskaner Weißbier",
        "vibe": "Elegantly decorated with equestrian and carousel motifs, modern hospitality, welcoming and stylish.",
        "crowd": "Couples, corporate groups, young professionals, conference attendees",
        "signature_dish": "Organic pork roasts, vegetarian spaetzle, delicate desserts",
        "table_capacity": 4300,
        "standing_rules": "Benches only. Tables strictly prohibited.",
        "transit_tip": "Located right at the main entrance; fast access to Theresienwiese U-Bahn."
    }
]

UNIVERSAL_RULES = [
    {
        "id": "standing_bench_vs_table",
        "title": "Benches vs. Tables",
        "category": "safety_and_conduct",
        "rule": "Standing on benches is permitted and encouraged once the band starts playing. Standing on tables is strictly forbidden across all tents and will result in immediate ejection by security (Ordner)."
    },
    {
        "id": "masskrug_theft",
        "title": "Maßkrug (Beer Stein) Theft",
        "category": "legal_and_security",
        "rule": "Taking a beer stein outside the tent or festival grounds is treated as criminal theft. Munich police and security confiscate over 100,000 steins yearly and issue immediate fines."
    },
    {
        "id": "unreserved_seating_quota",
        "title": "Walk-In / Unreserved Seating Quotas",
        "category": "seating_and_entry",
        "rule": "By city law, at least 25% of all indoor seats must remain unreserved at all times. On weekends and holidays before 3:00 PM, up to 50% must be reserved for walk-ins. Arrive before 10 AM on weekends or before 3 PM on weekdays to claim a bench."
    },
    {
        "id": "closing_times",
        "title": "Closing Times and Last Call",
        "category": "timing",
        "rule": "Beer service stops at 10:30 PM in large tents, music ends at 10:30 PM, and tents close at 11:30 PM. Exceptions: Käfer Wiesn-Schänke and Kufflers Weinzelt remain open until 1:00 AM (last call at 12:15 AM)."
    },
    {
        "id": "tipping_bedienung",
        "title": "Tipping Waitstaff (Bedienung)",
        "category": "etiquette",
        "rule": "Waitstaff work brutal 16-hour shifts carrying up to 10-12 steins. Always round up your bill (e.g. if a Maß is €14.80 - €15.20, give €16 or €17). Generous early tipping guarantees prompt refills throughout the night."
    },
    {
        "id": "toast_etiquette_prost",
        "title": "The Prost (Toasting) Ritual",
        "category": "etiquette",
        "rule": "Whenever the band plays 'Ein Prosit der Gemütlichkeit' (usually every 15-20 minutes), everyone stands up, clinks steins (bottom-to-bottom, never rim-to-rim to avoid cracking the heavy glass), makes direct eye contact, says 'Prost!', and takes a drink."
    },
    {
        "id": "bag_and_backpack_restrictions",
        "title": "Luggage & Bag Policy",
        "category": "security",
        "rule": "Backpacks and bags exceeding 3 liters capacity (approx 20cm x 15cm x 10cm) are forbidden on the festival grounds. Security checks every entrance; luggage storage depots are available at the perimeter."
    }
]

def seed_database():
    db = firestore.Client(project=GCP_PROJECT_ID)
    print(f"Connecting to Firestore ({GCP_PROJECT_ID})...")
    
    # 1. Seed Tents
    tents_ref = db.collection("wiesn_tents")
    print("\n--- Seeding All 14 Large Oktoberfest Tents ---")
    for tent in ALL_14_TENTS:
        doc_id = tent["id"]
        tents_ref.document(doc_id).set(tent)
        print(f"  ✓ {tent['name']} ({doc_id})")
        
    # 2. Seed Universal Rules
    rules_ref = db.collection("wiesn_rules")
    print("\n--- Seeding Universal Wiesn Etiquette & Regulations ---")
    for r in UNIVERSAL_RULES:
        doc_id = r["id"]
        rules_ref.document(doc_id).set(r)
        print(f"  ✓ {r['title']} ({doc_id})")
        
    print("\n🎉 Fully populated Firestore with all 14 large tents and key festival rules!")

if __name__ == "__main__":
    seed_database()
