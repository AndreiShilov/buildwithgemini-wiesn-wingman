"""Menu, dietary scanner, and bill/tip splitting tools for WiesnWingman."""
from typing import Any, Dict, List, Optional
import math

TRADITIONAL_WIESN_FOOD_CATALOG = [
    {
        "id": "hendl",
        "german_name": "Klassisches Wiesn-Hendl",
        "english_name": "Crispy Half Roasted Chicken",
        "price_eur": 16.50,
        "dietary": ["meat", "gluten-free-adaptable"],
        "description": "The quintessential Oktoberfest food. Crispy golden skin, parsley butter stuffing, juicy roast chicken. Eaten entirely with your hands!",
        "recommended_pairing": "1 Maß Festbier Märzen"
    },
    {
        "id": "schweinshaxe",
        "german_name": "Knusprige Schweinshaxe",
        "english_name": "Crisp Bavarian Pork Knuckle",
        "price_eur": 24.80,
        "dietary": ["meat"],
        "description": "Massive roasted pork shank with extra crackling blistered skin, served with dark beer caraway gravy and potato dumpling (Kartoffelknödel).",
        "recommended_pairing": "1 Maß Dark/Märzen Festbier"
    },
    {
        "id": "steckerlfisch",
        "german_name": "Steckerlfisch (Makrele)",
        "english_name": "Grilled Fish on a Wooden Stick",
        "price_eur": 22.00,
        "dietary": ["pescatarian", "gluten-free"],
        "description": "Whole spiced mackerel grilled over open charcoal spits, served with fresh lemon and a giant Brezn.",
        "recommended_pairing": "Augustiner Festbier or Weißbier"
    },
    {
        "id": "obatzda",
        "german_name": "Hausgemachter Obatzda mit Riesenbrezn",
        "english_name": "Bavarian Camembert Cheese Spread with Giant Pretzel",
        "price_eur": 12.50,
        "dietary": ["vegetarian"],
        "description": "Aged Camembert mashed with rich butter, sweet paprika, chopped onions, and a splash of beer. Served with fresh chives and radishes.",
        "recommended_pairing": "Light or wheat beer, great shared appetizer"
    },
    {
        "id": "kaesespaetzle",
        "german_name": "Allgäuer Käsespätzle",
        "english_name": "Homemade Bavarian Cheese Spaetzle",
        "price_eur": 17.20,
        "dietary": ["vegetarian"],
        "description": "Tender egg noodles layered with molten mountain cheeses (Bergkäse, Emmentaler) and topped with a generous mountain of crispy fried onions.",
        "recommended_pairing": "1 Maß Festbier or Radler"
    },
    {
        "id": "vegan_schnitzel",
        "german_name": "Veganes Schnitzel mit Kartoffelsalat",
        "english_name": "Plant-based Schnitzel with Bavarian Potato Salad",
        "price_eur": 18.50,
        "dietary": ["vegan", "vegetarian"],
        "description": "Crispy breaded plant protein schnitzel served with warm vinegar-and-oil Bavarian potato salad (no mayo) and lemon wedge.",
        "recommended_pairing": "Festbier or mineral water"
    },
    {
        "id": "kaiserschmarrn",
        "german_name": "Kaiserschmarrn mit Zwetschgenröster",
        "english_name": "Caramelized Shredded Pancake with Plum Compote",
        "price_eur": 14.50,
        "dietary": ["vegetarian", "dessert"],
        "description": "Fluffy, thick torn pancake caramelized in butter and sugar, dusted with powdered sugar, served with warm stewed plum or apple sauce.",
        "recommended_pairing": "Espresso or coffee"
    },
    {
        "id": "riesenbrezn",
        "german_name": "Frische Münchner Riesenbrezn",
        "english_name": "Giant Bavarian Pretzel",
        "price_eur": 6.50,
        "dietary": ["vegetarian", "vegan"],
        "description": "Warm, chewy, giant salt-crusted pretzel baked fresh daily.",
        "recommended_pairing": "Essential companion to any Maß"
    }
]

FESTBIER_PRICE_EUR = 15.20  # standard ~€14.80 - €15.40 average per Maß


def get_tent_food_menu(dietary_preference: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves the traditional Oktoberfest tent food menu with prices, descriptions, and dietary filtering.

    Args:
        dietary_preference: Optional filter (e.g. 'vegetarian', 'vegan', 'meat', 'gluten-free', 'dessert').

    Returns:
        A list of matching dishes with German names, translations, prices, and pairing notes.
    """
    if not dietary_preference:
        return TRADITIONAL_WIESN_FOOD_CATALOG
    
    pref = dietary_preference.lower().strip()
    return [
        dish for dish in TRADITIONAL_WIESN_FOOD_CATALOG
        if any(pref in tag.lower() for tag in dish["dietary"])
    ]


def calculate_bill_and_tip_split(
    num_people: int,
    total_mass_beers: int,
    dishes_ordered: Optional[List[str]] = None,
    tip_percentage: float = 10.0
) -> Dict[str, Any]:
    """Calculates total tent bill, standard Bedienung (waitstaff) tip, and per-person rounded split in Euros.

    Args:
        num_people: Number of people sharing the table/bill.
        total_mass_beers: Total number of 1L beer steins ordered.
        dishes_ordered: List of dish IDs or food names ordered (e.g. ['hendl', 'obatzda', 'kaesespaetzle']).
        tip_percentage: Tip percentage to include for the waitstaff (standard is 8-15%, default 10%).

    Returns:
        A dictionary with subtotal, beer cost, food cost, recommended tip, total with tip, and per-person rounded cash split.
    """
    beer_cost = total_mass_beers * FESTBIER_PRICE_EUR
    food_cost = 0.0
    items_breakdown = [f"{total_mass_beers}x Maß Festbier (€{beer_cost:.2f})"]

    if dishes_ordered:
        for item in dishes_ordered:
            item_clean = item.lower().strip()
            matched = False
            for dish in TRADITIONAL_WIESN_FOOD_CATALOG:
                if item_clean in dish["id"] or item_clean in dish["german_name"].lower() or item_clean in dish["english_name"].lower():
                    food_cost += dish["price_eur"]
                    items_breakdown.append(f"1x {dish['german_name']} (€{dish['price_eur']:.2f})")
                    matched = True
                    break
            if not matched:
                # Default estimate for unknown dish
                food_cost += 18.0
                items_breakdown.append(f"1x {item} (estimated €18.00)")

    subtotal = beer_cost + food_cost
    tip_multiplier = max(0.05, min(0.25, tip_percentage / 100.0))
    tip_amount = subtotal * tip_multiplier
    total_with_tip = subtotal + tip_amount

    people_count = max(1, num_people)
    per_person_raw = total_with_tip / people_count
    # Cash rounding: waitstaff prefer whole round Euro amounts (e.g. €38 instead of €37.32)
    per_person_rounded = math.ceil(per_person_raw)
    final_rounded_total = per_person_rounded * people_count

    return {
        "status": "calculated",
        "num_people": people_count,
        "items_breakdown": items_breakdown,
        "subtotal_eur": round(subtotal, 2),
        "beer_subtotal_eur": round(beer_cost, 2),
        "food_subtotal_eur": round(food_cost, 2),
        "recommended_tip_eur": round(tip_amount, 2),
        "total_with_tip_eur": round(total_with_tip, 2),
        "per_person_exact_eur": round(per_person_raw, 2),
        "per_person_cash_rounded_eur": per_person_rounded,
        "final_rounded_pool_eur": final_rounded_total,
        "bedienung_tipping_rule": "In Munich tents, waitstaff pay the brewery upfront for each round in cash! Round up each person to the nearest whole Euro to ensure fast service."
    }
