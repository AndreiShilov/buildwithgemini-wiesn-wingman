"""Networking and icebreaker tools for WiesnWingman: Bierbank tech networking."""
from typing import Any, Dict, List, Optional

SAMPLE_TECH_ICEBREAKERS = {
    "automotive": [
        "Ask them: 'Does your autonomous driving sensor fusion handle spilled Festbier on the road?'",
        "Say: 'Forget Level 5 autonomy, after 2 Maß my internal navigation is strictly Level 0. What stack are you guys building?'"
    ],
    "cloud": [
        "Ask them: 'If Oktoberfest has 10,000 requests per second for beer, what is the autoscaling policy for the Bedienungen?'",
        "Say: 'My memory cache is dropping packets after this 6.3% Spaten. How is your team handling multi-region redundancy on GCP?'"
    ],
    "ai_ml": [
        "Ask them: 'Is anyone fine-tuning an LLM to decode Bavarian dialect at 100dB brass band volume?'",
        "Say: 'My prompt engineering tonight is down to one token: \"Noch a Maß bittschön\". What models are you training lately?'"
    ],
    "security": [
        "Ask them: 'The Ordner (security guards) here have zero-trust architecture dialed in. How does your zero-trust posture compare?'",
        "Say: 'Stealing a Maßkrug is a direct security breach with instant physical ejection. What is your team’s latest incident response war story?'"
    ],
    "frontend": [
        "Ask them: 'How would you CSS flexbox 10 sweaty developers onto a single wooden beer bench without overflow-hidden?'",
        "Say: 'The real-world latency between ordering a Hendl and eating it is brutal. What framework are you betting on this year?'"
    ],
    "general": [
        "Say: 'Prost! We have 12 minutes before the band plays Ein Prosit again—what is the most exciting project you are hacking on right now?'",
        "Ask them: 'Are you here with a local Munich crew or did your company fly you in for the tech conference?'"
    ]
}


def generate_bierbank_icebreaker(
    neighbor_company_or_domain: str,
    tent_name: Optional[str] = None,
    user_tech_stack: Optional[str] = None
) -> Dict[str, Any]:
    """Generates context-aware, witty tech conversation starters tailored for meeting fellow developers or founders on an Oktoberfest beer bench.

    Args:
        neighbor_company_or_domain: Company name or tech field (e.g. 'BMW', 'Google Cloud', 'autonomous driving', 'cybersecurity', 'frontend', 'AI / LLMs', 'robotics').
        tent_name: Name of the current tent (e.g. 'Schottenhamel', 'Hacker-Pschorr', 'Paulaner').
        user_tech_stack: What you work on (optional, e.g. 'Python backend', 'Cloud architect').

    Returns:
        A dictionary with 2-3 tailored icebreakers, cultural etiquette tips for bench networking, and a suggested follow-up topic.
    """
    domain_lower = neighbor_company_or_domain.lower()
    
    # Categorize domain
    if any(k in domain_lower for k in ["bmw", "auto", "car", "driving", "audi", "porsche", "adas"]):
        category = "automotive"
    elif any(k in domain_lower for k in ["cloud", "gcp", "aws", "azure", "kubernetes", "infra"]):
        category = "cloud"
    elif any(k in domain_lower for k in ["ai", "ml", "llm", "gemini", "agent", "deep learning"]):
        category = "ai_ml"
    elif any(k in domain_lower for k in ["security", "cyber", "infosec", "auth", "crypto"]):
        category = "security"
    elif any(k in domain_lower for k in ["frontend", "react", "vue", "css", "web"]):
        category = "frontend"
    else:
        category = "general"

    openers = SAMPLE_TECH_ICEBREAKERS.get(category, SAMPLE_TECH_ICEBREAKERS["general"])
    
    tent_context = f"in {tent_name}" if tent_name else "on the Bierbank"
    
    return {
        "status": "ready",
        "target_domain": neighbor_company_or_domain,
        "category": category,
        "tent_context": tent_context,
        "icebreakers": openers,
        "networking_rules": [
            "Never pitch aggressively—Oktoberfest networking is 80% camaraderie and 20% tech curiosity.",
            "Always clink your Maß with them before starting the chat ('Prost! Oans, zwoa, gsuffa!').",
            "Exchange LinkedIn or GitHub QR codes directly on your phone screen before the noise level peaks."
        ],
        "follow_up_question": "What is the hardest bug you've had to solve in production recently?"
    }
