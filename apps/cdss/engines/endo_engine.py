"""Endo Engine – Python port of endo/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]

    scores = {
        "ReversiblePulpitis": 0,
        "SymptomaticIrreversiblePulpitis": 0,
        "AsymptomaticIrreversiblePulpitis": 0,
        "PulpNecrosis": 0,
        "ChronicApicalPeriodontitis": 0,
        "AcuteApicalAbscess": 0,
    }
    reasoning = []
    red_flags = []
    requirements = {"history": [], "exam": ["coldResponse", "percussion"], "investigations": []}

    # Complaint correlation
    if "ENDO_COLD_PAIN" in complaint_codes:
        scores["ReversiblePulpitis"] += 2
    if any(c in complaint_codes for c in ["ENDO_NIGHT_PAIN", "ENDO_SPONTANEOUS_PAIN", "ENDO_HOT_PAIN"]):
        scores["SymptomaticIrreversiblePulpitis"] += 3
    if "CONS_DISCOLORATION" in complaint_codes:
        scores["PulpNecrosis"] += 3
    if "ENDO_SINUS_TRACT" in complaint_codes:
        scores["ChronicApicalPeriodontitis"] += 4
    if "ENDO_SWELLING" in complaint_codes:
        scores["AcuteApicalAbscess"] += 4

    reasoning.append("Complaint correlated with pulpal/periapical pathology")

    # History
    if history.get("duration") == "long":
        scores["AsymptomaticIrreversiblePulpitis"] += 4
        reasoning.append("Long-standing history → chronic pulpal inflammation")
    if history.get("spontaneousPain") is True:
        scores["SymptomaticIrreversiblePulpitis"] += 5
    if history.get("trauma") is True:
        scores["PulpNecrosis"] += 4
        reasoning.append("History of trauma → risk of pulp necrosis")
    if history.get("painReliefWithAnalgesic") is True:
        scores["SymptomaticIrreversiblePulpitis"] += 2

    # Vitality
    cold = exam.get("coldResponse")
    if cold == "normal":
        scores["ReversiblePulpitis"] += 8
        reasoning.append("Normal cold response → Vital pulp")
    elif cold == "lingering":
        scores["SymptomaticIrreversiblePulpitis"] += 10
        reasoning.append("Lingering cold response → Symptomatic irreversible pulpitis")
    elif cold == "none":
        scores["PulpNecrosis"] += 12
        reasoning.append("No cold response → Pulp necrosis")
    elif cold == "exaggerated":
        if not history.get("spontaneousPain") and exam.get("percussion") != "positive":
            scores["AsymptomaticIrreversiblePulpitis"] += 10
            reasoning.append("Exaggerated vitality without symptoms → Asymptomatic irreversible pulpitis")

    # Heat
    if exam.get("heatResponse") == "lingering":
        scores["SymptomaticIrreversiblePulpitis"] += 6
        reasoning.append("Lingering heat response → Irreversible pulpitis")

    # EPT
    ept = exam.get("eptResponse")
    if ept == "normal":
        scores["ReversiblePulpitis"] += 3
    elif ept == "delayed":
        scores["AsymptomaticIrreversiblePulpitis"] += 5
    elif ept == "none":
        scores["PulpNecrosis"] += 8
        reasoning.append("EPT non-response → Non-vital pulp")

    # Percussion & palpation
    if exam.get("percussion") == "positive" and cold == "none":
        scores["ChronicApicalPeriodontitis"] += 8
        reasoning.append("Positive percussion + non-vital → Apical periodontitis")
    if exam.get("palpation") == "positive" and cold == "none":
        scores["ChronicApicalPeriodontitis"] += 6

    # Swelling
    swelling = exam.get("swelling")
    if swelling == "localized" and cold == "none":
        scores["AcuteApicalAbscess"] += 10
        red_flags.append("Acute localized infection")
        reasoning.append("Localized swelling + non-vital → Acute apical abscess")
    elif swelling == "diffuse":
        scores["AcuteApicalAbscess"] += 15
        red_flags.append("Diffuse facial swelling – emergency management required")
        reasoning.append("Diffuse swelling → Space infection risk")

    # Sinus tract
    if exam.get("sinusTract") == "present":
        scores["ChronicApicalPeriodontitis"] += 10
        reasoning.append("Sinus tract → Chronic periapical infection")

    # Radiographic
    if exam.get("periapicalRadiolucency") == "present":
        scores["ChronicApicalPeriodontitis"] += 8
        reasoning.append("Periapical radiolucency → Apical pathology")

    # Suppression
    if scores["PulpNecrosis"] > 10:
        scores["ReversiblePulpitis"] = max(0, scores["ReversiblePulpitis"] - 6)
        scores["SymptomaticIrreversiblePulpitis"] = max(0, scores["SymptomaticIrreversiblePulpitis"] - 4)
        scores["AsymptomaticIrreversiblePulpitis"] = max(0, scores["AsymptomaticIrreversiblePulpitis"] - 4)
        reasoning.append("Necrosis dominance suppresses vital pulp diagnoses")

    # Requirement enforcement
    missing = [f for f in requirements["exam"] if exam.get(f) is None]
    if missing:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Required clinical inputs missing:"] + [f"- {f}" for f in missing],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Insufficient diagnostic dominance"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    provisional = result["provisional"]
    investigations = ["IOPA Radiograph"]
    if "Pulpitis" in provisional:
        investigations.append("Thermal vitality tests")
    if "Apical" in provisional:
        investigations.append("Periapical radiographic evaluation")

    treatment_map = {
        "ReversiblePulpitis": ["Caries removal", "Indirect pulp protection", "Definitive restoration"],
        "SymptomaticIrreversiblePulpitis": ["Root canal treatment", "Post & core", "Full coverage crown"],
        "AsymptomaticIrreversiblePulpitis": ["Root canal treatment", "Definitive restoration"],
        "PulpNecrosis": ["Root canal treatment", "Intracanal medicament", "Definitive obturation"],
        "ChronicApicalPeriodontitis": ["Root canal treatment", "Radiographic follow-up"],
        "AcuteApicalAbscess": ["Drainage", "Root canal treatment", "Systemic antibiotics if indicated"],
    }
    icd_map = {
        "ReversiblePulpitis": "K04.0",
        "SymptomaticIrreversiblePulpitis": "K04.02",
        "AsymptomaticIrreversiblePulpitis": "K04.03",
        "PulpNecrosis": "K04.1",
        "ChronicApicalPeriodontitis": "K04.5",
        "AcuteApicalAbscess": "K04.7",
    }

    return {
        "provisional": provisional,
        "treatment": treatment_map.get(provisional, []),
        "investigations": investigations,
        "medication": [],
        "reasoningTrace": reasoning,
        "confidence": result["confidence"],
        "ranked": result["ranked"],
        "requirements": requirements,
        "redFlags": red_flags,
        "icd": icd_map.get(provisional, "K04.9"),
    }
