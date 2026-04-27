"""
Universal Multi-Department Brain – Python port of universalBrain.js
Processes per-tooth complaint + exam data, runs relevant department engines,
resolves conflict via highest scoring result.
"""
from . import (
    endo_engine,
    perio_engine,
    oral_med_engine,
    oral_surgery_engine,
    conservative_engine,
    prostho_engine,
    ortho_engine,
    pedo_engine,
    implant_engine,
)
from .master_complaint_registry import MASTER_COMPLAINT_REGISTRY
from .medication_guard import adjust_medication

ENGINE_MAP = {
    "ENDO": endo_engine,
    "PERIO": perio_engine,
    "ORAL_MED": oral_med_engine,
    "ORAL_SURGERY": oral_surgery_engine,
    "CONSERVATIVE": conservative_engine,
    "PROSTHODONTICS": prostho_engine,
    "ORTHODONTICS": ortho_engine,
    "PEDODONTICS": pedo_engine,
    "IMPLANTOLOGY": implant_engine,
}


def detect_departments(complaints: list, patient: dict) -> list:
    """Return list of department keys relevant to the given complaints."""
    detected = set()
    for c in complaints:
        code = c.get("code") if isinstance(c, dict) else c
        item = MASTER_COMPLAINT_REGISTRY.get(code)
        if item:
            detected.add(item["department"])
    try:
        age = int(patient.get("age") or 0)
    except (ValueError, TypeError):
        age = 0
    if age <= 16 and age > 0:
        detected.add("PEDODONTICS")
    if not detected:
        detected.add("ENDO")
    return list(detected)


def merge_requirements(results: list) -> dict:
    merged = {"history": set(), "exam": set(), "investigations": set()}
    for r in results:
        if not r or not r.get("requirements"):
            continue
        for key in ("history", "exam", "investigations"):
            for v in (r["requirements"].get(key) or []):
                merged[key].add(v)
    return {k: list(v) for k, v in merged.items()}


def normalize_medication(result: dict) -> list:
    for key in ("medication", "medications", "meds"):
        val = result.get(key)
        if isinstance(val, list):
            return val
        if val:
            return [val]
    return []


def resolve_conflict(results: list):
    """Return the result with the highest top-ranked score."""
    valid = [r for r in results if r and r.get("provisional")]
    if not valid:
        return None
    valid.sort(
        key=lambda r: (r.get("ranked") or [{}])[0].get("score", 0),
        reverse=True,
    )
    return valid[0]


def run_universal_brain(payload: dict) -> dict:
    """
    payload = {
        "teeth": {
            "12": {"complaints": [...], "exam": {...}},
            "17": {"complaints": [...], "exam": {...}},
        },
        "history": {"medical": [...], "habits": [...], "pastDental": [...]},
        "patient": {"age": 25, "allergy": [...]}
    }
    Returns:
    {
        "teeth": {
            "12": {diagnosis, icd, confidence, reasoning, treatment,
                   medication, redFlags, investigations, ranked},
            ...
        }
    }
    """
    teeth = payload.get("teeth", {})
    history = payload.get("history", {})
    patient = payload.get("patient", {})

    result_teeth = {}

    for tooth_no, tooth_data in teeth.items():
        complaints = tooth_data.get("complaints", [])
        exam = tooth_data.get("exam", {})

        detected_departments = detect_departments(complaints, patient)
        results = []

        for dept_key in detected_departments:
            engine = ENGINE_MAP.get(dept_key)
            if not engine or not hasattr(engine, "think"):
                continue
            try:
                output = engine.think({
                    "complaints": complaints,
                    "exam": exam,
                    "history": history,
                    "patient": patient,
                })
                if output:
                    results.append(output)
            except Exception as e:
                pass  # individual engine failure is non-fatal

        merged_requirements = merge_requirements(results)
        final_result = resolve_conflict(results)

        if not final_result:
            result_teeth[tooth_no] = {
                "diagnosis": None,
                "reasoning": {"explanation": "Insufficient diagnostic dominance.", "ranked": []},
                "requirements": merged_requirements,
                "redFlags": [],
                "treatment": [],
                "treatmentPhases": {},
                "medication": [],
                "investigations": [],
                "icd": None,
                "confidence": "VERY LOW",
                "riskModifiers": [],
                "safetyWarnings": [],
            }
            continue

        medication = normalize_medication(final_result)

        # Apply medication safety guard
        visit_context = {"history": history, "patient": patient}
        if medication:
            medication = adjust_medication(
                [{"name": m} if isinstance(m, str) else m for m in medication],
                visit_context,
            )

        reasoning_trace = final_result.get("reasoningTrace") or []
        explanation = (
            "\n".join(reasoning_trace)
            if isinstance(reasoning_trace, list)
            else reasoning_trace
        )

        result_teeth[tooth_no] = {
            "diagnosis": final_result.get("provisional"),
            "reasoning": {
                "explanation": explanation,
                "ranked": final_result.get("ranked") or [],
            },
            "requirements": merged_requirements,
            "redFlags": final_result.get("redFlags") or [],
            "treatment": final_result.get("treatment") or [],
            "treatmentPhases": {},
            "medication": medication,
            "investigations": final_result.get("investigations") or [],
            "icd": final_result.get("icd"),
            "confidence": final_result.get("confidence") or "LOW",
            "riskModifiers": [],
            "safetyWarnings": [],
        }

    return {"teeth": result_teeth}
