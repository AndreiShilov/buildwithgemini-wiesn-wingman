"""Seed script for WiesnWingman Oktoberfest tents collection in Firestore."""
from google.cloud import firestore

# IMPORTANT: Hardcoded GCP project ID string to avoid project number resolution issues on Agent Platform
GCP_PROJECT_ID = "qwiklabs-gcp-04-06c7bc5ed227"

TENTS_DATA = [
    {
        "id": "hacker-pschorr",
        "name": "Hacker-Pschorr (Himmel der Bayern)",
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
        "transit_tip": "Walk south to Poccistraße to avoid U4/U5 lines."
    },
    {
        "id": "ochsenbraterei",
        "name": "Ochsenbraterei",
        "brewery": "Spaten-Franziskaner-Bräu",
        "beer_served": "Spaten Oktoberfestbier (6.3%)",
        "vibe": "Famous spit-roasted whole oxen, slightly calmer traditional atmosphere, great acoustic brass music.",
        "crowd": "Foodies, engineering leaders, cross-generational festivalgoers",
        "signature_dish": "Whole roasted ox on a spit with red wine gravy & dumplings",
        "table_capacity": 7600,
        "standing_rules": "Bench standing only. Always toast neighbors when 'Ein Prosit' plays.",
        "transit_tip": "Theresienwiese station is right behind, or 10 min stroll to Schwanthalerhöhe."
    }
]

def seed():
    db = firestore.Client(project=GCP_PROJECT_ID)
    collection_ref = db.collection("wiesn_tents")
    print(f"Connecting to Firestore for project: {GCP_PROJECT_ID}...")
    for tent in TENTS_DATA:
        doc_id = tent["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(tent)
        print(f"  ✓ Seeded tent: {tent['name']} (ID: {doc_id})")
    print("Done seeding wiesn_tents collection!")

if __name__ == "__main__":
    seed()
