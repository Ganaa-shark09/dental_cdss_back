"""Oral Surgery Engine – Python port of oralSurgery/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]
    text = " ".join(c.get("complaint", "") for c in complaints if isinstance(c, dict)).lower()

    scores = {
        "Pericoronitis": 0,
        "ImpactedThirdMolar": 0,
        "DrySocket": 0,
        "RootStump": 0,
        "DentoalveolarAbscess": 0,
        "SpaceInfection": 0,
        "ToothFracture": 0,
    }
    reasoning = []
    red_flags = []
    requirements = {"history": [], "exam": [], "investigations": []}

    # Text-based complaint signals
    if "impacted" in text:
        scores["ImpactedThirdMolar"] += 5
    if "pericoronitis" in text:
        scores["Pericoronitis"] += 6
    if "swelling" in text or "SURGERY_SWELLING" in complaint_codes:
        scores["DentoalveolarAbscess"] += 3
    if "dry socket" in text:
        scores["DrySocket"] += 6
    if "root stump" in text:
        scores["RootStump"] += 6
    if "fracture" in text or "trauma" in text or "SURGERY_TRAUMA" in complaint_codes:
        scores["ToothFracture"] += 5

    # Code-based signals
    if "SURGERY_IMPACTED" in complaint_codes or "SURGERY_WISDOM" in complaint_codes:
        scores["ImpactedThirdMolar"] += 5
    if "SURGERY_SPACE_INFECTION" in complaint_codes:
        scores["SpaceInfection"] += 8
        red_flags.append("Possible fascial space infection – emergency")
    if "SURGERY_NON_HEALING" in complaint_codes:
        scores["DrySocket"] += 6

    # Exam-based
    if exam.get("partiallyErupted") and exam.get("pericoronalFlap"):
        scores["Pericoronitis"] += 8
        reasoning.append("Operculum inflammation suggests pericoronitis")
    if exam.get("trismus"):
        scores["Pericoronitis"] += 3

    if exam.get("impactionType"):
        scores["ImpactedThirdMolar"] += 8
        reasoning.append("Impaction classification confirmed")

    if history.get("recentExtraction") and exam.get("emptySocket"):
        scores["DrySocket"] += 10
        reasoning.append("Recent extraction + empty socket")

    if exam.get("rootFragmentVisible"):
        scores["RootStump"] += 8

    if exam.get("fluctuantSwelling") and exam.get("pusDischarge"):
        scores["DentoalveolarAbscess"] += 10
        red_flags.append("Acute odontogenic abscess")

    if exam.get("diffuseSwelling") and exam.get("trismus"):
        scores["SpaceInfection"] += 12
        red_flags.append("Possible fascial space infection")

    if exam.get("mobility") and exam.get("traumaHistory"):
        scores["ToothFracture"] += 8
        reasoning.append("Trauma + mobility suggests fracture")

    # Structured exam fields from CLINICAL_SCHEMA ORAL_SURGERY
    impaction_type = exam.get("impactionType")
    if impaction_type and impaction_type != "none":
        scores["ImpactedThirdMolar"] += 6
        reasoning.append(f"Impaction type: {impaction_type}")

    space_infection = exam.get("spaceInfection")
    if space_infection in ("fascialSpace", "ludwigAngina"):
        scores["SpaceInfection"] += 12
        red_flags.append("Fascial space infection – airway risk")
    elif space_infection == "localized":
        scores["DentoalveolarAbscess"] += 6

    trismus = exam.get("trismus")
    if trismus == "severe":
        scores["SpaceInfection"] += 4
        red_flags.append("Severe trismus – surgical consideration")

    if exam.get("fractureSuspected") == "yes":
        scores["ToothFracture"] += 8
        red_flags.append("Fracture suspected – radiographic confirmation required")

    post_extraction = exam.get("postExtractionComplication")
    if post_extraction == "drySocket":
        scores["DrySocket"] += 10
        reasoning.append("Dry socket complication")
    elif post_extraction == "infection":
        scores["DentoalveolarAbscess"] += 8

    if exam.get("cysticLesion") == "present":
        scores["ImpactedThirdMolar"] += 4
        reasoning.append("Cystic lesion associated with impacted tooth")

    if exam.get("oralSubmucousFibrosis") == "present":
        red_flags.append("Oral submucous fibrosis detected")

    has_signal = any(v > 0 for v in scores.values())
    if not has_signal:
        return None

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return None

    provisional = result["provisional"]
    investigations = ["OPG"]
    if provisional == "ImpactedThirdMolar":
        investigations.append("CBCT if nerve proximity suspected")

    treatment_map = {
        "Pericoronitis": ["Irrigation under operculum", "Antibiotics if indicated", "Surgical extraction of third molar"],
        "ImpactedThirdMolar": ["Surgical removal", "Flap reflection", "Bone guttering if required"],
        "DrySocket": ["Irrigation", "Medicated dressing", "Analgesics"],
        "RootStump": ["Surgical removal of root stump"],
        "DentoalveolarAbscess": ["Incision and drainage", "Extraction or RCT", "Systemic antibiotics if systemic signs"],
        "SpaceInfection": ["Emergency referral", "IV antibiotics", "Hospital admission"],
        "ToothFracture": ["Stabilization", "Radiographic assessment", "Extraction if non-restorable"],
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
        "icd": "K10.9",
    }
