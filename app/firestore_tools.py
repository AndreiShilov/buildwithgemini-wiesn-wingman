"""Firestore backend tools for WiesnWingman Oktoberfest tents."""
from typing import Any, Dict, List, Optional
from google.cloud import firestore

# IMPORTANT: Hardcoded GCP project ID string to avoid project number resolution issues on Agent Platform
GCP_PROJECT_ID = "qwiklabs-gcp-04-06c7bc5ed227"

_db: Optional[firestore.Client] = None

def get_firestore_client() -> firestore.Client:
    """Returns a singleton Firestore client with hardcoded project ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=GCP_PROJECT_ID)
    return _db


def list_oktoberfest_tents() -> List[Dict[str, Any]]:
    """Retrieves all Oktoberfest tents from Firestore with details like brewery, beer served, vibe, crowd, and signature dishes.

    Returns:
        A list of dictionaries containing tent details.
    """
    db = get_firestore_client()
    tents = []
    docs = db.collection("wiesn_tents").stream()
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        tents.append(data)
    return tents


def get_oktoberfest_tent_details(tent_id_or_name: str) -> Dict[str, Any]:
    """Gets detailed information for a specific Oktoberfest tent by its ID or name (e.g. 'hacker-pschorr', 'schottenhamel', 'paulaner-festzelt', 'ochsenbraterei').

    Args:
        tent_id_or_name: The ID or partial name of the tent to look up.

    Returns:
        A dictionary with the tent's details, rules, vibe, signature dishes, and transit tips.
    """
    db = get_firestore_client()
    query_str = tent_id_or_name.lower().strip()

    # Direct document lookup by ID
    doc = db.collection("wiesn_tents").document(query_str).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    # Fuzzy match across documents
    docs = db.collection("wiesn_tents").stream()
    for d in docs:
        data = d.to_dict()
        name = data.get("name", "").lower()
        if query_str in d.id.lower() or query_str in name:
            data["id"] = d.id
            return data

    return {
        "status": "not_found",
        "message": f"No Oktoberfest tent found matching '{tent_id_or_name}'. Try 'hacker-pschorr', 'schottenhamel', 'paulaner-festzelt', or 'ochsenbraterei'."
    }


def add_or_update_oktoberfest_tent(
    tent_id: str,
    name: str,
    brewery: str,
    beer_served: str,
    vibe: str,
    crowd: str,
    signature_dish: str,
    standing_rules: str,
    transit_tip: str,
    table_capacity: Optional[int] = None
) -> Dict[str, Any]:
    """Adds a new Oktoberfest tent or updates an existing tent in Firestore.

    Args:
        tent_id: Unique identifier for the tent (e.g. 'augustiner-festhalle', 'marstall').
        name: Full name of the tent.
        brewery: Associated Munich brewery (e.g. 'Augustiner-Bräu', 'Hofbräu').
        beer_served: Specific Oktoberfest Märzen beer and ABV%.
        vibe: Description of atmosphere, music style, and energy level.
        crowd: Typical demographic or attendee profile.
        signature_dish: Traditional food specialties.
        standing_rules: Rules for standing on benches vs. tables and etiquette.
        transit_tip: Tips for avoiding crowd bottlenecks when leaving.
        table_capacity: Optional total seating capacity.

    Returns:
        A dictionary indicating success and saved details.
    """
    db = get_firestore_client()
    doc_ref = db.collection("wiesn_tents").document(tent_id.lower().strip())
    data = {
        "id": tent_id.lower().strip(),
        "name": name,
        "brewery": brewery,
        "beer_served": beer_served,
        "vibe": vibe,
        "crowd": crowd,
        "signature_dish": signature_dish,
        "standing_rules": standing_rules,
        "transit_tip": transit_tip,
    }
    if table_capacity is not None:
        data["table_capacity"] = table_capacity

    doc_ref.set(data, merge=True)
    return {
        "status": "success",
        "message": f"Tent '{name}' (ID: {tent_id}) successfully saved in Firestore.",
        "tent": data
    }


def list_wiesn_rules(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves universal Oktoberfest tent rules, safety regulations, and cultural etiquette from Firestore.

    Args:
        category: Optional category filter (e.g. 'safety_and_conduct', 'legal_and_security', 'seating_and_entry', 'timing', 'etiquette', 'security').

    Returns:
        A list of rules with title, category, and explanation.
    """
    db = get_firestore_client()
    rules = []
    docs = db.collection("wiesn_rules").stream()
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        if category and data.get("category", "").lower() != category.lower():
            continue
        rules.append(data)
    return rules


def get_wiesn_rule_detail(rule_id_or_keyword: str) -> Dict[str, Any]:
    """Gets details on a specific Oktoberfest rule or etiquette guideline (e.g. 'table', 'bench', 'theft', 'stein', 'tipping', 'toast', 'prost', 'hours', 'bags').

    Args:
        rule_id_or_keyword: Keyword or ID of the rule to look up.

    Returns:
        The matching rule description and advice.
    """
    db = get_firestore_client()
    kw = rule_id_or_keyword.lower().strip()
    docs = db.collection("wiesn_rules").stream()
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        if kw in doc.id.lower() or kw in data.get("title", "").lower() or kw in data.get("rule", "").lower():
            return data
    return {
        "status": "not_found",
        "message": f"No specific rule found for '{rule_id_or_keyword}'. Use list_wiesn_rules to see all rules."
    }

