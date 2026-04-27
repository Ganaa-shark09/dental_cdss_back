"""
Universal Diagnostic Scoring Engine – V3 (Python port)
Port of scoring.js: calculateResult()
"""


def calculate_result(scores: dict) -> dict:
    """
    Takes a dict of {diagnosis_name: score} and returns
    {"provisional": str|None, "ranked": list, "confidence": str}
    """
    # 1. Sanitize
    clean = {k: max(0, float(v or 0)) for k, v in scores.items()}

    # 2. Remove zero-score diagnoses
    filtered = [(k, v) for k, v in clean.items() if v > 0]

    if not filtered:
        return {"provisional": None, "ranked": [], "confidence": "VERY LOW"}

    # 3. Sort descending (deterministic on tie)
    ranked = sorted(filtered, key=lambda x: (-x[1], x[0]))
    ranked_list = [{"diagnosis": name, "score": score} for name, score in ranked]

    top_name, top_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0

    # 4. Minimum clinical threshold
    if top_score < 3:
        return {"provisional": None, "ranked": ranked_list[:5], "confidence": "VERY LOW"}

    # 5. Ambiguity detection
    if second_score == top_score and top_score >= 5:
        return {"provisional": None, "ranked": ranked_list[:5], "confidence": "VERY LOW"}

    # 6. Dominance ratio
    difference = top_score - second_score
    ratio = top_score / second_score if second_score > 0 else top_score

    if top_score >= 10 and ratio >= 2.0 and difference >= 5:
        confidence = "HIGH"
    elif top_score >= 7 and ratio >= 1.5 and difference >= 3:
        confidence = "MODERATE"
    elif difference >= 1:
        confidence = "LOW"
    else:
        confidence = "VERY LOW"

    return {
        "provisional": top_name,
        "ranked": ranked_list[:5],
        "confidence": confidence,
    }
