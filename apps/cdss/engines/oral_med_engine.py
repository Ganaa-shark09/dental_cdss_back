"""Oral Medicine Engine – Python port of oralMed/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]
    medical = [str(m).lower().strip() for m in (history.get("medical") or [])]
    habits = [str(h).lower().strip() for h in (history.get("habits") or [])]

    red_flags = []
    requirements = {"history": [], "exam": [], "investigations": []}

    # Emergency: Space infection
    if "ORALMED_SPACE_INFECTION" in complaint_codes:
        red_flags.append("Fascial space infection – airway risk")
        return {
            "provisional": "SpaceInfection",
            "treatment": ["Immediate hospital admission", "Airway monitoring", "Surgical drainage"],
            "medication": ["IV Amoxicillin-Clavulanate", "Metronidazole", "Analgesics"],
            "investigations": ["CBC", "Contrast CT"],
            "reasoningTrace": ["Emergency infection code detected", "Possible fascial space involvement"],
            "confidence": "HIGH", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": "K12.2",
        }

    diagnoses = [
        "TraumaticUlcer", "RecurrentAphthousStomatitis", "Candidiasis",
        "Leukoplakia", "Erythroplakia", "OralSquamousCellCarcinoma",
        "OralSubmucousFibrosis", "BurningMouthSyndrome", "TMJDisorder", "Xerostomia",
    ]
    scores = {d: 0 for d in diagnoses}
    reasoning = []

    lesion_related = any(c in complaint_codes for c in [
        "ORALMED_ULCER", "ORALMED_WHITE_PATCH", "ORALMED_RED_PATCH", "ORALMED_PIGMENTATION"
    ])
    tmj_related = any(c in complaint_codes for c in ["ORALMED_TMJ", "ORALMED_CLICKING"])
    dry_mouth = "ORALMED_DRY_MOUTH" in complaint_codes

    if lesion_related:
        requirements["exam"] += ["lesionType", "durationMoreThan2Weeks"]
        if exam.get("lesionType") == "ulcer":
            requirements["exam"] += ["traumaHistory", "recurrentUlcer"]
        if exam.get("lesionType") == "whitePatch":
            requirements["exam"].append("scrapable")
        if exam.get("durationMoreThan2Weeks") == "yes":
            requirements["exam"] += ["induration", "lymphNodeInvolvement"]

    if tmj_related:
        requirements["exam"].append("jointSound")
    if "ORALMED_LIMITED_OPENING" in complaint_codes:
        requirements["exam"].append("mouthOpeningRestriction")

    lesion_type = exam.get("lesionType")

    if lesion_type == "ulcer":
        reasoning.append("Ulcer diagnostic pathway activated")
        if exam.get("traumaHistory") == "present":
            scores["TraumaticUlcer"] += 10
        if exam.get("recurrentUlcer") == "yes":
            scores["RecurrentAphthousStomatitis"] += 10
        if exam.get("durationMoreThan2Weeks") == "yes":
            scores["OralSquamousCellCarcinoma"] += 12
            reasoning.append("Non-healing ulcer → malignancy suspicion")
        if exam.get("induration") == "present":
            scores["OralSquamousCellCarcinoma"] += 12
            red_flags.append("Induration present")
        if exam.get("lymphNodeInvolvement") == "present":
            scores["OralSquamousCellCarcinoma"] += 8
            red_flags.append("Regional lymphadenopathy")

    elif lesion_type == "whitePatch":
        if exam.get("scrapable") == "yes":
            scores["Candidiasis"] += 12
            reasoning.append("Scrapable lesion → fungal origin")
        elif exam.get("scrapable") == "no":
            scores["Leukoplakia"] += 10
            reasoning.append("Non-scrapable lesion → keratotic lesion")
        if any(h in habits for h in ("tobacco", "smoking")):
            scores["Leukoplakia"] += 4

    elif lesion_type == "redPatch":
        scores["Erythroplakia"] += 12
        scores["OralSquamousCellCarcinoma"] += 10
        red_flags.append("Red lesion – high malignant potential")

    # OSMF
    areca_habit = any(k in h for h in habits for k in ("areca", "gutkha", "pan masala", "supari"))
    if exam.get("mouthOpeningRestriction") == "yes" and areca_habit:
        scores["OralSubmucousFibrosis"] += 12
        reasoning.append("Restricted opening + areca nut habit")

    if tmj_related:
        scores["TMJDisorder"] += 10
        reasoning.append("TMJ functional symptoms detected")

    if dry_mouth:
        scores["Xerostomia"] += 10
        if "diabetes" in medical:
            scores["Xerostomia"] += 3

    if exam.get("burningSensation") == "yes" and not lesion_related:
        scores["BurningMouthSyndrome"] += 6

    # Requirement enforcement
    missing = [f for f in requirements["exam"] if exam.get(f) in (None, "")]
    if missing:
        reasoning.append("Awaiting additional clinical inputs")
        return {
            "provisional": "PendingClinicalData", "treatment": [], "medication": [], "investigations": [],
            "reasoningTrace": reasoning + [f"Required: {m}" for m in missing],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return {
            "provisional": "PendingClinicalData", "treatment": [], "medication": [], "investigations": [],
            "reasoningTrace": ["Insufficient diagnostic dominance"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    provisional = result["provisional"]
    investigations = []
    if provisional in ("Leukoplakia", "Erythroplakia", "OralSquamousCellCarcinoma"):
        investigations.append("Incisional biopsy")
    if provisional == "Candidiasis":
        investigations.append("Fungal smear")
    if "Induration present" in red_flags or "Regional lymphadenopathy" in red_flags:
        investigations.append("Urgent biopsy")

    return {
        "provisional": provisional,
        "treatment": [],
        "medication": [],
        "investigations": investigations,
        "reasoningTrace": reasoning,
        "confidence": result["confidence"],
        "ranked": result["ranked"],
        "requirements": requirements,
        "redFlags": red_flags,
        "icd": "K12.9",
    }
