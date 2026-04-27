"""Conservative Engine – Python port of conservative/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]
    past_dental = [str(p).lower().strip() for p in (history.get("pastDental") or [])]

    scores = {
        "InitialEnamelCaries": 0,
        "ModerateDentinCaries": 0,
        "DeepCariesApproachingPulp": 0,
        "SecondaryCaries": 0,
        "FailedRestoration": 0,
        "FracturedRestoration": 0,
        "NonCariousCervicalLesion": 0,
        "PostEndodonticTooth": 0,
    }
    reasoning = []
    red_flags = []
    requirements = {"history": [], "exam": ["cariesDepth", "restorationStatus"], "investigations": []}

    # Complaint correlation
    if "CONS_CARIES" in complaint_codes:
        scores["ModerateDentinCaries"] += 3
    if "CONS_FRACTURE" in complaint_codes:
        scores["FracturedRestoration"] += 4
    if "CONS_SECONDARY_CARIES" in complaint_codes:
        scores["SecondaryCaries"] += 5
    if "CONS_SENSITIVITY" in complaint_codes:
        scores["InitialEnamelCaries"] += 2
        scores["NonCariousCervicalLesion"] += 2

    caries_depth = exam.get("cariesDepth")
    if caries_depth == "enamel":
        scores["InitialEnamelCaries"] += 8
        reasoning.append("Enamel involvement only → Initial caries")
    elif caries_depth == "dentin":
        scores["ModerateDentinCaries"] += 8
        reasoning.append("Dentin involvement → Moderate caries")
    elif caries_depth == "deep":
        scores["DeepCariesApproachingPulp"] += 10
        reasoning.append("Deep caries close to pulp")

    restoration = exam.get("restorationStatus")
    if restoration == "defective":
        scores["FailedRestoration"] += 8
        reasoning.append("Defective restoration detected")
    elif restoration == "secondaryCaries":
        scores["SecondaryCaries"] += 9
        reasoning.append("Secondary caries under restoration")
    elif restoration == "fractured":
        scores["FracturedRestoration"] += 8
        reasoning.append("Restoration fracture present")

    sensitivity = exam.get("sensitivityType")
    if sensitivity == "coldShort":
        scores["InitialEnamelCaries"] += 4
    elif sensitivity == "sweet":
        scores["ModerateDentinCaries"] += 4

    if exam.get("cervicalLesion") == "present":
        scores["NonCariousCervicalLesion"] += 8
        reasoning.append("Cervical lesion detected")

    if any(kw in p for p in past_dental for kw in ("previous rct", "rct", "root canal treatment")):
        scores["PostEndodonticTooth"] += 8
        reasoning.append("Previously root treated tooth")

    if exam.get("coldResponse") == "none":
        scores["DeepCariesApproachingPulp"] = max(0, scores["DeepCariesApproachingPulp"] - 5)
        red_flags.append("Possible pulpal necrosis – endodontic evaluation required")

    missing = [f for f in requirements["exam"] if exam.get(f) is None]
    if missing:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Required restorative inputs missing:"] + [f"- {f}" for f in missing],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Insufficient restorative dominance"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    provisional = result["provisional"]
    investigations = ["IOPA Radiograph"]

    treatment_map = {
        "InitialEnamelCaries": ["Preventive resin restoration", "Fluoride therapy", "Diet counselling"],
        "ModerateDentinCaries": ["Caries excavation", "Adhesive restoration", "Follow-up"],
        "DeepCariesApproachingPulp": ["Selective caries removal", "Indirect pulp capping", "Definitive restoration"],
        "SecondaryCaries": ["Remove existing restoration", "Caries excavation", "Re-restoration"],
        "FailedRestoration": ["Remove restoration", "Evaluate remaining tooth structure", "Re-restoration"],
        "FracturedRestoration": ["Replace restoration", "Occlusal adjustment"],
        "NonCariousCervicalLesion": ["Desensitizing agent", "Glass ionomer restoration"],
        "PostEndodonticTooth": ["Post and core build-up", "Full coverage crown"],
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
