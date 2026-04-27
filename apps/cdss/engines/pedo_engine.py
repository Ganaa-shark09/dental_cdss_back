"""Pedodontics Engine – Python port of pedodontics/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})
    patient = payload.get("patient", {})

    age = int(patient.get("age") or 0)
    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]

    red_flags = []
    reasoning = []
    requirements = {"history": [], "exam": ["cariesDepthPrimary", "vitalStatusPrimary"], "investigations": []}

    if age > 16:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Not within pediatric age range"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    reasoning.append("Pediatric diagnostic pathway activated")

    space_maintainers = [
        "Band and Loop", "Crown and Loop", "Lingual Holding Arch",
        "Nance Palatal Arch", "Transpalatal Arch", "Distal Shoe Appliance",
        "Removable Acrylic Space Maintainer",
    ]

    scores = {
        "EarlyChildhoodCaries": 0, "RampantCaries": 0, "DeepCariesPrimaryTooth": 0,
        "PrimaryReversiblePulpitis": 0, "PrimaryIrreversiblePulpitis": 0,
        "NonVitalPrimaryTooth": 0, "PrematureLossPrimaryTooth": 0,
        "SpaceLoss": 0, "DelayedEruption": 0, "EctopicEruption": 0,
        "SupernumeraryTooth": 0, "TraumaticInjuryPrimary": 0,
        "ArchLengthDiscrepancy": 0, "HighCariesRisk": 0,
    }

    if "PEDO_MULTIPLE_CARIES" in complaint_codes:
        scores["EarlyChildhoodCaries"] += 6
    if "PEDO_PRIMARY_TOOTH_PAIN" in complaint_codes:
        scores["DeepCariesPrimaryTooth"] += 4
    if "PEDO_PREMATURE_LOSS" in complaint_codes:
        scores["PrematureLossPrimaryTooth"] += 6
    if "PEDO_DELAYED_ERUPTION" in complaint_codes:
        scores["DelayedEruption"] += 6
    if "PEDO_TRAUMA" in complaint_codes:
        scores["TraumaticInjuryPrimary"] += 6

    if history.get("dietRisk") == "high":
        scores["HighCariesRisk"] += 6
        red_flags.append("High sugar exposure")
    if history.get("fluorideExposure") == "low":
        scores["HighCariesRisk"] += 4
        red_flags.append("Low fluoride exposure")

    if exam.get("multipleCaries") == "yes":
        scores["EarlyChildhoodCaries"] += 8
    if exam.get("rampantPattern") == "yes":
        scores["RampantCaries"] += 10
    if exam.get("cariesDepthPrimary") == "deep":
        scores["DeepCariesPrimaryTooth"] += 8

    vital = exam.get("vitalStatusPrimary")
    if vital == "vital":
        if exam.get("spontaneousPain") == "no":
            scores["PrimaryReversiblePulpitis"] += 6
        elif exam.get("spontaneousPain") == "yes":
            scores["PrimaryIrreversiblePulpitis"] += 9
    elif vital == "nonVital":
        scores["NonVitalPrimaryTooth"] += 10

    if exam.get("prematureLoss") == "yes":
        scores["PrematureLossPrimaryTooth"] += 10
        reasoning.append("Premature loss of primary tooth detected")
    if exam.get("spaceReduction") == "yes":
        scores["SpaceLoss"] += 8
    try:
        ald = float(exam.get("archLengthDiscrepancy") or 0)
    except (ValueError, TypeError):
        ald = 0
    if ald > 4:
        scores["ArchLengthDiscrepancy"] += 8

    if exam.get("delayedEruption") == "yes":
        scores["DelayedEruption"] += 8
    if exam.get("ectopicEruption") == "yes":
        scores["EctopicEruption"] += 8
    if exam.get("supernumeraryDetected") == "yes":
        scores["SupernumeraryTooth"] += 8

    trauma = exam.get("traumaSeverity")
    if trauma == "mild":
        scores["TraumaticInjuryPrimary"] += 6
    elif trauma == "severe":
        scores["TraumaticInjuryPrimary"] += 10
        red_flags.append("Severe trauma – immediate management required")

    if exam.get("franklBehavior") == "negative":
        red_flags.append("Negative Frankl behavior – sedation/GA consideration")
    if history.get("specialNeeds") == "yes":
        red_flags.append("Special health care needs – modified protocol required")

    missing_req = [f for f in requirements["exam"] if exam.get(f) is None]
    if missing_req:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Required pediatric inputs missing:"] + [f"- {f}" for f in missing_req],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Insufficient pediatric dominance"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    provisional = result["provisional"]
    investigations = ["IOPA (child protocol)"]
    if provisional in ("DelayedEruption", "EctopicEruption", "SupernumeraryTooth"):
        investigations.append("Panoramic radiograph")

    treatment_map = {
        "EarlyChildhoodCaries": ["Glass ionomer restorations", "Fluoride varnish", "Diet counseling"],
        "RampantCaries": ["Full mouth rehabilitation", "3-month recall", "Fluoride therapy"],
        "DeepCariesPrimaryTooth": ["Selective caries removal", "Indirect pulp therapy", "Stainless steel crown"],
        "PrimaryReversiblePulpitis": ["Indirect pulp therapy", "SSC if required"],
        "PrimaryIrreversiblePulpitis": ["Pulpotomy", "Stainless steel crown"],
        "NonVitalPrimaryTooth": ["Pulpectomy", "Resorbable obturation", "SSC"],
        "PrematureLossPrimaryTooth": ["Space maintainer placement", f"Common Types: {', '.join(space_maintainers)}"],
        "SpaceLoss": ["Space regainer", "Orthodontic consultation"],
        "DelayedEruption": ["Radiographic evaluation", "Surgical exposure if required"],
        "EctopicEruption": ["Elastic separator technique", "Extraction if severe"],
        "SupernumeraryTooth": ["Surgical removal", "Orthodontic follow-up"],
        "TraumaticInjuryPrimary": ["Clinical + radiographic assessment", "Follow-up protocol"],
        "ArchLengthDiscrepancy": ["Serial extraction planning", "Orthodontic referral"],
        "HighCariesRisk": ["Caries risk management", "Fluoride therapy", "Diet counseling"],
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
        "icd": "K02.9",
    }
