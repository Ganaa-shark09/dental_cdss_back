"""Orthodontics Engine – Python port of orthodontics/engine.js"""
from .scoring import calculate_result


def think(payload: dict) -> dict:
    complaints = payload.get("complaints", [])
    exam_raw = payload.get("exam", {})
    patient = payload.get("patient", {})

    age = int(patient.get("age") or 0)
    complaint_codes = [c.get("code") for c in complaints if isinstance(c, dict)]

    # Normalize exam
    exam = dict(exam_raw)
    if "overjet" not in exam:
        exam["overjet"] = exam_raw.get("overjetValue") or exam_raw.get("overjet_mm")
    if "spacingPresence" not in exam:
        exam["spacingPresence"] = exam_raw.get("spacing") or exam_raw.get("spacingPresent")

    diagnoses = [
        "ClassI", "ClassIIDiv1", "ClassIIDiv2", "ClassIII",
        "Crowding", "Spacing", "DeepBite", "OpenBite", "Crossbite", "OrthognathicCase",
    ]
    scores = {d: 0 for d in diagnoses}
    reasoning = []
    red_flags = []
    requirements = {"history": [], "exam": [], "investigations": []}

    ortho_complaint = any(c in complaint_codes for c in [
        "ORTHO_CROWDING", "ORTHO_SPACING", "ORTHO_MALOCCLUSION", "ORTHO_IRREGULAR", "ORTHO_PROTRUSION"
    ])

    if not ortho_complaint:
        return {
            "provisional": None, "treatment": [], "investigations": [], "medication": [],
            "reasoningTrace": ["Orthodontic pathway not activated"],
            "confidence": "VERY LOW", "ranked": [], "requirements": requirements,
            "redFlags": red_flags, "icd": None,
        }

    reasoning.append("Orthodontic diagnostic workflow initiated")
    requirements["exam"] = [
        "malocclusionClass", "overjet", "overbite", "crowdingSeverity",
        "facialProfile", "growthStatus", "incisorInclination", "spacingPresence"
    ]

    overjet = exam.get("overjet")
    overjet_increased = overjet == "increased" or (isinstance(overjet, (int, float)) and overjet > 4)

    malocclusion = exam.get("malocclusionClass")
    if malocclusion == "class1":
        scores["ClassI"] += 12
        reasoning.append("Angle Class I molar relation")
    elif malocclusion == "class2":
        if overjet_increased:
            scores["ClassIIDiv1"] += 14
            reasoning.append("Proclined incisors → Class II Division 1")
        if exam.get("overbite") == "deep" and exam.get("incisorInclination") == "retroclined":
            scores["ClassIIDiv2"] += 14
            reasoning.append("Retroclined incisors + deep bite → Class II Division 2")
    elif malocclusion == "class3":
        scores["ClassIII"] += 16
        reasoning.append("Mesial molar relation → Class III")

    crowding = exam.get("crowdingSeverity")
    if crowding == "mild":
        scores["Crowding"] += 4
    elif crowding == "moderate":
        scores["Crowding"] += 8
    elif crowding == "severe":
        scores["Crowding"] += 12

    if exam.get("spacingPresence") == "present":
        scores["Spacing"] += 10

    overbite = exam.get("overbite")
    if overbite == "deep":
        scores["DeepBite"] += 10
    elif overbite == "open":
        scores["OpenBite"] += 10

    crossbite = exam.get("crossbite")
    if crossbite and crossbite != "absent":
        scores["Crossbite"] += 10
        reasoning.append("Transverse discrepancy present")

    profile = exam.get("facialProfile")
    if profile == "convex":
        scores["ClassIIDiv1"] += 4
    elif profile == "concave":
        scores["ClassIII"] += 4

    growing = exam.get("growthStatus") == "growing" or (0 < age < 18)
    if not growing and malocclusion in ("class2", "class3"):
        scores["OrthognathicCase"] += 18
        red_flags.append("Adult skeletal discrepancy – surgery consideration")

    missing_req = [f for f in requirements["exam"] if exam.get(f) is None]
    if missing_req:
        reasoning.append("Incomplete orthodontic records detected")

    scores = {k: max(0, v) for k, v in scores.items()}
    result = calculate_result(scores)

    provisional = result.get("provisional")

    appliance_map = {
        "ClassI": ["0.022 MBT prescription fixed appliance", "NiTi alignment wires", "Elastic chain space closure", "Essix retainer"],
        "ClassIIDiv1": (
            ["Twin Block Functional Appliance", "Headgear (High pull if vertical excess)", "MBT fixed appliance", "Hawley retainer"]
            if growing else
            ["Class II Elastics with Fixed Appliance", "MBT fixed appliance", "Hawley retainer"]
        ),
        "ClassIIDiv2": ["Utility arch for incisor proclination", "Reverse curve NiTi", "Fixed appliance therapy", "Anterior bite plane"],
        "ClassIII": (
            ["Reverse Pull Facemask + RPE", "Class III elastics", "Fixed appliance finishing"]
            if growing else
            ["Orthognathic surgery preparation", "Class III elastics", "Fixed appliance finishing"]
        ),
        "Crowding": ["Arch expansion mechanics", "Interproximal reduction (IPR)", "Extraction therapy if severe"],
        "Spacing": ["Power chain mechanics", "Loop mechanics space closure"],
        "DeepBite": ["Anterior bite turbos", "Intrusion arch", "Reverse curve wire"],
        "OpenBite": ["Vertical elastics", "Habit breaking appliance", "Posterior intrusion mechanics"],
        "Crossbite": ["Rapid Palatal Expander", "Quad Helix appliance"],
        "OrthognathicCase": ["Pre-surgical orthodontics", "Orthognathic surgery referral", "Post-surgical detailing"],
    }

    treatment = []
    if provisional:
        seen = set()
        for step in appliance_map.get(provisional, []):
            if step not in seen:
                seen.add(step)
                treatment.append(step)

    investigations = ["Lateral Cephalogram", "OPG", "Study models", "Photographic records", "Cephalometric analysis"]

    return {
        "provisional": provisional,
        "treatment": treatment,
        "medication": [],
        "investigations": investigations,
        "reasoningTrace": reasoning,
        "confidence": "LOW" if missing_req else result.get("confidence", "VERY LOW"),
        "ranked": result.get("ranked", []),
        "requirements": requirements,
        "redFlags": red_flags,
        "icd": "K07.9",
    }
