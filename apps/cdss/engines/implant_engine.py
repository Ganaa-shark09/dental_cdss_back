"""Implantology Engine – Python port of implantology/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]
    medical = [str(m).lower().strip() for m in (history.get("medical") or [])]
    habits = [str(h).lower().strip() for h in (history.get("habits") or [])]

    red_flags = []
    reasoning = []
    requirements = {
        "history": [],
        "exam": ["implantMobility", "periImplantPocket", "boneLossAroundImplant", "oralHygieneStatus", "bruxismHistory"],
        "investigations": [],
    }

    implant_complaint = any(c in complaint_codes for c in [
        "IMPLANT_CONSULT", "IMPLANT_MOBILITY", "IMPLANT_SWELLING",
        "IMPLANT_MISSING_TOOTH", "IMPLANT_EDENTULOUS",
    ])

    if not implant_complaint:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Implant pathway not activated"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    reasoning.append("Implant treatment planning initiated")

    diagnoses = [
        "IdealImplantCandidate", "BoneDeficiencyCase", "ImmediateLoadingCandidate",
        "DelayedLoadingCandidate", "HighFailureRisk", "PeriImplantMucositis", "PeriImplantitis",
    ]
    scores = {d: 0 for d in diagnoses}

    mobility = exam.get("implantMobility")
    pocket = exam.get("periImplantPocket")
    bone_loss = exam.get("boneLossAroundImplant")
    hygiene = exam.get("oralHygieneStatus")
    bruxism = exam.get("bruxismHistory")

    if mobility == "present":
        scores["PeriImplantitis"] += 14
        red_flags.append("Implant mobility — loss of osseointegration")
        reasoning.append("Mobility indicates implant failure risk")

    if pocket == "deep" and bone_loss == "none":
        scores["PeriImplantMucositis"] += 8
        reasoning.append("Deep pocket without bone loss → mucositis")

    if pocket == "deep" and bone_loss not in (None, "none"):
        scores["PeriImplantitis"] += 12
        reasoning.append("Pocket + bone loss → peri-implantitis")

    if bone_loss == "mild":
        scores["BoneDeficiencyCase"] += 6
    elif bone_loss == "severe":
        scores["BoneDeficiencyCase"] += 14
        red_flags.append("Severe bone loss — grafting required")

    if mobility == "none" and bone_loss == "none" and hygiene == "good":
        scores["ImmediateLoadingCandidate"] += 10
        reasoning.append("Stable bone + hygiene → immediate loading possible")
    else:
        scores["DelayedLoadingCandidate"] += 8

    if "diabetes" in medical:
        scores["HighFailureRisk"] += 8
        red_flags.append("Diabetes — delayed osseointegration risk")
    if "smoking" in habits:
        scores["HighFailureRisk"] += 10
        red_flags.append("Smoking — implant survival reduced")
    if bruxism == "yes":
        scores["HighFailureRisk"] += 8
        red_flags.append("Bruxism — occlusal overload risk")
    if hygiene == "poor":
        scores["HighFailureRisk"] += 10
        reasoning.append("Poor hygiene increases peri-implant risk")

    if mobility == "none" and bone_loss == "none" and hygiene == "good":
        scores["IdealImplantCandidate"] += 14

    missing_req = [
        f for f in requirements["exam"]
        if exam.get(f) in (None, "", "select")
    ]
    if missing_req:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Implant planning requires:"] + [f"- {m}" for m in missing_req],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)
    provisional = result.get("provisional")

    if not provisional:
        reasoning.append("No dominant implant diagnosis")

    treatment_map = {
        "IdealImplantCandidate": ["CBCT guided implant placement", "Flapless surgery", "Immediate provisional crown", "Torque ≥35 Ncm loading"],
        "BoneDeficiencyCase": ["Guided Bone Regeneration (GBR)", "Ridge augmentation", "Delayed implant placement"],
        "ImmediateLoadingCandidate": ["Immediate loading protocol", "Provisional restoration within 48 hrs"],
        "DelayedLoadingCandidate": ["Submerged healing protocol", "Loading after 3–4 months"],
        "HighFailureRisk": ["Risk factor modification", "Medical consultation", "Strict maintenance protocol"],
        "PeriImplantMucositis": ["Mechanical debridement", "Chlorhexidine irrigation", "Oral hygiene reinforcement"],
        "PeriImplantitis": ["Surgical decontamination", "Implant surface detoxification", "Regenerative therapy"],
    }

    medication = []
    if provisional in ("PeriImplantitis", "PeriImplantMucositis"):
        medication = ["Amoxicillin 500mg TID (5 days)", "Ibuprofen 400mg SOS", "Chlorhexidine mouthwash 0.12%"]

    investigations = ["CBCT scan", "Bone density analysis", "Diagnostic wax-up", "Occlusal analysis"]

    return {
        "provisional": provisional,
        "treatment": treatment_map.get(provisional, []),
        "medication": medication,
        "investigations": investigations,
        "reasoningTrace": reasoning,
        "confidence": result.get("confidence", "VERY LOW"),
        "ranked": result.get("ranked", []),
        "requirements": requirements,
        "redFlags": red_flags,
        "icd": "Z96.5",
    }
