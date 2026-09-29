"""Stamina Pacer tools for WiesnWingman: Blood Alcohol Content (BAC) estimation & morning schedule alignment."""
from typing import Any, Dict, Optional

# Average Oktoberfest Festbier properties:
# 1 Maß = 1 Liter of ~6.0% ABV Festbier
# Pure alcohol per Maß = 1000 ml * 0.06 * 0.8 g/ml = ~48 grams of pure ethanol!
# (Equivalent to ~2.5 to 3 standard US/UK beers per single Maß!)
GRAMS_ALCOHOL_PER_MASS = 48.0
METABOLIC_ELIMINATION_RATE_PER_HOUR = 0.015  # average % BAC reduction per hour (Widmark rate: ~0.015 g/dL per hr)

def calculate_drink_pacer_and_bac(
    mass_count: float,
    hours_drinking: float,
    body_weight_kg: float = 75.0,
    gender: str = "male",
    next_morning_event: str = "Hackathon Pitch",
    event_start_time_str: str = "09:00"
) -> Dict[str, Any]:
    """Calculates estimated Blood Alcohol Content (BAC), hours until sober, and evaluates readiness for tomorrow morning's commitments.

    Args:
        mass_count: Number of Maß (1-liter Oktoberfest beers) consumed so far.
        hours_drinking: Total duration of drinking in hours (e.g. 2.5).
        body_weight_kg: Approximate body weight in kilograms (defaults to 75kg).
        gender: 'male' (r=0.68) or 'female' (r=0.55) for Widmark body water factor.
        next_morning_event: Description of tomorrow's primary morning commitment (e.g. 'Project Pitch', 'Keynote', 'Coding Sprint').
        event_start_time_str: Tomorrow's start time in HH:MM format (e.g. '09:00', '10:00').

    Returns:
        A dictionary containing estimated peak BAC, current BAC, time to reach 0.00% sobriety, warning level, hydration/pacing advice, and transit curfew recommendation.
    """
    if mass_count <= 0:
        return {
            "status": "sober",
            "current_bac_percent": 0.0,
            "drinks_summary": "0 Maß consumed.",
            "recommendation": "You're completely clear! Stay hydrated with water or Apfelschorle.",
            "morning_readiness": f"100% ready for '{next_morning_event}' at {event_start_time_str}."
        }

    # Widmark formula: BAC = [Alcohol in grams / (Body weight in grams * r)] * 100 - (Beta * hours)
    r = 0.68 if gender.lower() == "male" else 0.55
    total_alcohol_grams = mass_count * GRAMS_ALCOHOL_PER_MASS
    weight_grams = max(40.0, body_weight_kg) * 1000.0

    peak_bac = (total_alcohol_grams / (weight_grams * r)) * 100.0
    elapsed_hours = max(0.5, hours_drinking)
    metabolized = METABOLIC_ELIMINATION_RATE_PER_HOUR * elapsed_hours
    current_bac = max(0.0, peak_bac - metabolized)

    # Hours until 0.00% BAC from now
    hours_to_zero = current_bac / METABOLIC_ELIMINATION_RATE_PER_HOUR if current_bac > 0 else 0.0

    # Risk assessment
    if current_bac >= 0.15:
        risk_level = "CRITICAL / HIGH RISK"
        curfew_advice = "STOP DRINKING ALCOHOL IMMEDIATELY. Switch to water + electrolytes now. Leave the tent before 21:30 to avoid U-Bahn crush."
    elif current_bac >= 0.08:
        risk_level = "ELEVATED (Legally Intoxicated)"
        curfew_advice = "Slow down! 1 Maß of Festbier is equal to nearly 3 standard beers. Order an Apfelschorle or Radler next, and eat a hearty pretzel (Breze) or Hendl."
    elif current_bac >= 0.03:
        risk_level = "MILD BUZZ / ACTIVE"
        curfew_advice = "Good social pacing. Alternate each subsequent Maß with 0.5L water."
    else:
        risk_level = "NEGLIGIBLE"
        curfew_advice = "You're in the green zone. Enjoy the atmosphere responsibly."

    # Compare with tomorrow's schedule
    morning_warning = (
        f"You need approximately {hours_to_zero:.1f} hours from now to metabolize back to 0.00% BAC. "
        f"For tomorrow's '{next_morning_event}' at {event_start_time_str}, plan to be in bed early with a large bottle of water."
    )

    return {
        "status": "calculated",
        "mass_count": mass_count,
        "festbier_equivalent_standard_beers": round(mass_count * 2.8, 1),
        "estimated_current_bac_percent": round(current_bac, 3),
        "estimated_promille": round(current_bac * 10.0, 2),  # European standard (‰)
        "hours_until_sober": round(hours_to_zero, 1),
        "risk_level": risk_level,
        "curfew_and_pacing_advice": curfew_advice,
        "morning_assessment": morning_warning,
        "next_morning_event": next_morning_event,
        "event_time": event_start_time_str
    }
