"""
Medication Safety Guard – Python port of medicationGuard.js
adjustMedication(medications, visit) → list with warnings/contraindications
"""


def adjust_medication(medications: list, visit: dict) -> list:
    """
    medications: list of {"name": str, ...}
    visit: {"history": {"medical": [], "habits": []}, "patient": {"allergy": []}}
    Returns adjusted list with "warning" and "contraindicated" fields added where relevant.
    """
    history = visit.get("history", {})
    patient = visit.get("patient", {})

    medical = [str(m).lower().strip() for m in (history.get("medical") or [])]
    allergies = [str(a).lower().strip() for a in (patient.get("allergy") or [])]

    has_diabetes = any("diabetes" in m for m in medical)
    has_hypertension = any("hypertension" in m for m in medical)
    has_pregnancy = any("pregnancy" in m for m in medical)
    has_cardiac = any("cardiac" in m for m in medical)

    adjusted = []
    for med in medications:
        m = dict(med)
        name = (m.get("name") or "").lower()

        if has_diabetes:
            if "steroid" in name:
                m["warning"] = "Use steroid cautiously in diabetic patient"
            elif "zerodol" in name or "nsaid" in name:
                m["warning"] = "Monitor blood sugar while using NSAIDs"

        if has_hypertension:
            if any(k in name for k in ("ibuprofen", "diclofenac", "zerodol", "nsaid")):
                m["warning"] = "NSAIDs may elevate BP – monitor closely"

        if has_pregnancy:
            if any(k in name for k in ("metronidazole", "diclofenac", "aceclofenac")):
                m["contraindicated"] = True
                m["warning"] = "Contraindicated in pregnancy"

        if has_cardiac:
            if "nsaid" in name:
                m["warning"] = "Avoid prolonged NSAID use in cardiac patients"

        for allergy in allergies:
            if allergy and allergy in name:
                m["contraindicated"] = True
                m["warning"] = "Patient allergic to this drug"
                break

        adjusted.append(m)

    return adjusted
