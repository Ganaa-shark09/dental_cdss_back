"""Perio Engine – Python port of perio/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]
    medical = [str(m).lower().strip() for m in (history.get("medical") or [])]
    habits = [str(h).lower().strip() for h in (history.get("habits") or [])]

    scores = {
        "PlaqueInducedGingivitis": 0,
        "Stage1Periodontitis": 0,
        "Stage2Periodontitis": 0,
        "Stage3Periodontitis": 0,
        "PeriodontalAbscess": 0,
    }
    reasoning = []
    red_flags = []
    requirements = {
        "history": [], "exam": ["bleedingOnProbing", "pocketDepth", "mobility"], "investigations": []
    }

    # Complaint correlation
    if "PERIO_BLEEDING" in complaint_codes:
        scores["PlaqueInducedGingivitis"] += 2
    if "PERIO_LOOSE_TOOTH" in complaint_codes:
        scores["Stage3Periodontitis"] += 3
    if "PERIO_HALITOSIS" in complaint_codes:
        scores["Stage2Periodontitis"] += 2
    if "PERIO_SWELLING" in complaint_codes:
        scores["PeriodontalAbscess"] += 2

    reasoning.append("Complaint correlated with periodontal pathology")

    bop = exam.get("bleedingOnProbing")
    pocket = exam.get("pocketDepth")
    mobility = exam.get("mobility")
    recession = exam.get("gingivalRecession")
    furcation = exam.get("furcationInvolvement")
    bone_loss = exam.get("boneLossPattern")

    if bop == "present" and pocket == "<4mm":
        scores["PlaqueInducedGingivitis"] += 10
        reasoning.append("Bleeding without pocket → Gingivitis")

    if pocket == "4-6mm" and mobility == "none":
        scores["Stage1Periodontitis"] += 8
        reasoning.append("Moderate pocket without mobility → Stage 1")

    if pocket == "4-6mm" and recession in ("moderate", "severe"):
        scores["Stage2Periodontitis"] += 10
        reasoning.append("Pocket + recession → Stage 2")

    if pocket == ">6mm" or mobility in ("grade2", "grade3"):
        scores["Stage3Periodontitis"] += 12
        reasoning.append("Deep pocket or mobility → Stage 3")

    if furcation in ("grade2", "grade3"):
        scores["Stage3Periodontitis"] += 6
        reasoning.append("Advanced furcation involvement")

    if bone_loss == "vertical":
        scores["Stage3Periodontitis"] += 4

    # Abscess
    if pocket == ">6mm" and bop == "present" and "PERIO_SWELLING" in complaint_codes:
        scores["PeriodontalAbscess"] += 14
        red_flags.append("Acute periodontal abscess")
        reasoning.append("Deep pocket + swelling → Abscess")

    # Systemic
    if "diabetes" in medical:
        scores["Stage2Periodontitis"] += 2
        scores["Stage3Periodontitis"] += 3
        reasoning.append("Diabetes increases periodontal destruction risk")
    if "smoking" in habits:
        scores["Stage3Periodontitis"] += 3
        reasoning.append("Smoking worsens periodontal prognosis")

    # Requirement enforcement
    missing = [f for f in requirements["exam"] if exam.get(f) is None]
    if missing:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Required periodontal inputs missing:"] + [f"- {f}" for f in missing],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Insufficient periodontal dominance"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    provisional = result["provisional"]
    investigations = ["Full mouth periodontal charting", "IOPA / OPG radiograph"]
    if "Stage" in provisional:
        investigations.append("Clinical attachment level measurement")

    treatment_map = {
        "PlaqueInducedGingivitis": ["Scaling and polishing", "Oral hygiene reinforcement", "Review in 2 weeks"],
        "Stage1Periodontitis": ["Scaling and root planing", "Re-evaluation after 4 weeks"],
        "Stage2Periodontitis": ["Full mouth SRP", "Maintenance therapy"],
        "Stage3Periodontitis": ["SRP", "Periodontal surgery if indicated", "Maintenance phase"],
        "PeriodontalAbscess": ["Incision and drainage", "Debridement", "Systemic antibiotics if indicated"],
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
        "icd": "K05.9",
    }
