"""Prosthodontics Engine – Python port of prosthodontics/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam = payload.get("exam", {})
    history = payload.get("history", {})

    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]
    medical = [str(m).lower().strip() for m in (history.get("medical") or [])]
    habits = [str(h).lower().strip() for h in (history.get("habits") or [])]
    past_dental = [str(p).lower().strip() for p in (history.get("pastDental") or [])]

    scores = {
        "SingleCrown": 0,
        "PostEndodonticCrown": 0,
        "FixedPartialDenture": 0,
        "RemovablePartialDenture": 0,
        "CompleteDenture": 0,
        "ImplantSupportedProsthesis": 0,
    }
    reasoning = []
    red_flags = []
    requirements = {
        "history": [], "exam": ["missingTeethCount", "abutmentCondition", "ridgeCondition"], "investigations": []
    }

    # Complaint signals
    if "PROSTHO_MISSING_TOOTH" in complaint_codes:
        scores["FixedPartialDenture"] += 4
        scores["RemovablePartialDenture"] += 3
        reasoning.append("Missing tooth complaint")
    if "PROSTHO_MULTIPLE_MISSING" in complaint_codes:
        scores["RemovablePartialDenture"] += 5
        reasoning.append("Multiple missing teeth complaint")
    if "PROSTHO_COMPLETE_EDENTULISM" in complaint_codes:
        scores["CompleteDenture"] += 6
        reasoning.append("Complete denture request")
    if "PROSTHO_IMPLANT_REQUEST" in complaint_codes:
        scores["ImplantSupportedProsthesis"] += 6
        reasoning.append("Implant preference mentioned")

    if any(kw in p for p in past_dental for kw in ("rct", "root canal")):
        scores["PostEndodonticCrown"] += 8
        reasoning.append("Root treated tooth requires crown")

    # Missing teeth count
    missing_count = exam.get("missingTeethCount")
    if missing_count is not None:
        try:
            n = int(missing_count)
        except (ValueError, TypeError):
            n = 0
        if n == 1:
            scores["FixedPartialDenture"] += 5
            reasoning.append("Single missing tooth")
        elif 2 <= n <= 3:
            scores["FixedPartialDenture"] += 7
            scores["RemovablePartialDenture"] += 4
            reasoning.append("Multiple missing teeth (2–3)")
        elif n > 3:
            scores["RemovablePartialDenture"] += 8
            reasoning.append("Multiple missing teeth (>3)")
        if n >= 14:
            scores["CompleteDenture"] += 12
            reasoning.append("Near complete edentulism")

    abutment = exam.get("abutmentCondition")
    if abutment == "good":
        scores["FixedPartialDenture"] += 6
        reasoning.append("Good abutment support")
    elif abutment == "compromised":
        scores["RemovablePartialDenture"] += 6
        reasoning.append("Compromised abutment – RPD preferred")

    ridge = exam.get("ridgeCondition")
    if ridge == "adequate":
        scores["ImplantSupportedProsthesis"] += 6
        reasoning.append("Adequate ridge for implant")
    elif ridge == "moderate":
        scores["ImplantSupportedProsthesis"] += 3
        reasoning.append("Moderate ridge condition")
    elif ridge == "poor":
        red_flags.append("Severe ridge resorption – augmentation may be required")

    if exam.get("interarchSpace") == "insufficient":
        red_flags.append("Insufficient interarch space")

    kennedy = exam.get("kennedyClass")
    if kennedy in ("I", "II"):
        scores["RemovablePartialDenture"] += 6
        reasoning.append("Kennedy Class I/II")
    elif kennedy == "III":
        scores["FixedPartialDenture"] += 6
        reasoning.append("Kennedy Class III")
    elif kennedy == "IV":
        scores["FixedPartialDenture"] += 4
        reasoning.append("Kennedy Class IV")

    if exam.get("bruxism") == "yes":
        red_flags.append("Bruxism – occlusal overload risk")
    if "diabetes" in medical:
        red_flags.append("Diabetes – implant caution")
    if "smoking" in habits:
        red_flags.append("Smoking – implant failure risk")

    missing_req = [f for f in requirements["exam"] if exam.get(f) is None]
    if missing_req:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Required prosthodontic inputs missing:"] + [f"- {f}" for f in missing_req],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    if not result.get("provisional"):
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Insufficient prosthodontic dominance"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    provisional = result["provisional"]
    investigations = ["Diagnostic cast", "OPG"]
    if provisional == "ImplantSupportedProsthesis":
        investigations.append("CBCT")

    treatment_map = {
        "SingleCrown": ["Tooth preparation", "Impression", "Temporary crown", "Final cementation"],
        "PostEndodonticCrown": ["Post and core", "Full coverage crown"],
        "FixedPartialDenture": ["Abutment preparation", "Impression", "Provisional bridge", "Final cementation"],
        "RemovablePartialDenture": ["Surveying", "Framework design", "Try-in", "Insertion"],
        "CompleteDenture": ["Primary impression", "Final impression", "Jaw relation", "Try-in", "Insertion"],
        "ImplantSupportedProsthesis": ["CBCT planning", "Implant placement", "Healing", "Prosthetic loading"],
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
        "icd": "Z46.3",
    }
