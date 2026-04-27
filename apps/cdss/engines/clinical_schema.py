"""
CLINICAL_SCHEMA – single source of truth for all frontend wizard choices.

The schema is served via GET /api/v1/cdss/schema/ and consumed by the
Angular wizard to render dropdowns/chips in all 3 sections.

Structure
---------
MEDICAL_HISTORY_CHOICES  → Step 2 chip-select options
COMPLAINT_REGISTRY       → Step 3 department complaint chips (mirrors MASTER_COMPLAINT_REGISTRY)
EXAM_SCHEMA              → Step 4 per-department examination fields + their allowed values
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — Medical History choices  (Step 2)
# ─────────────────────────────────────────────────────────────────────────────

MEDICAL_HISTORY_CHOICES = {
    "systemic_conditions": [
        "Diabetes",
        "Hypertension",
        "Cardiac Disease",
        "Thyroid Disorder",
        "Asthma / Respiratory Disease",
        "Kidney Disease",
        "Liver Disease",
        "Epilepsy",
        "HIV / AIDS",
        "Blood Disorder (Anaemia / Thalassemia)",
        "Osteoporosis",
        "Autoimmune Disease",
        "Cancer / Malignancy",
        "None",
    ],
    "habits": [
        "Smoking",
        "Tobacco Chewing",
        "Alcohol Consumption",
        "Betel Nut (Areca) Chewing",
        "Pan / Gutka",
        "Nail Biting",
        "Bruxism (Teeth Grinding)",
        "Thumb Sucking",
        "Mouth Breathing",
        "None",
    ],
    "allergies": [
        "Penicillin",
        "Amoxicillin",
        "Aspirin",
        "Ibuprofen",
        "Diclofenac",
        "Metronidazole",
        "Sulfonamides",
        "Local Anaesthetic (Lignocaine)",
        "Latex",
        "None",
    ],
    "past_dental_history": [
        "Previous Root Canal Treatment",
        "Previous Extraction",
        "Previous Scaling",
        "Previous Orthodontic Treatment",
        "Previous Crown / Bridge",
        "Previous Implant",
        "Previous Denture",
        "Dental Phobia",
        "None",
    ],
    "severity_options": ["Mild", "Moderate", "Severe"],
    "duration_options": ["< 1 week", "1–2 weeks", "2–4 weeks", "1–3 months", "> 3 months"],
}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — Complaint Registry per department  (Step 3)
# ─────────────────────────────────────────────────────────────────────────────

COMPLAINT_REGISTRY = {
    "ENDO": [
        {"code": "ENDO_SPONTANEOUS_PAIN", "label": "Spontaneous tooth pain"},
        {"code": "ENDO_NIGHT_PAIN",        "label": "Night pain"},
        {"code": "ENDO_COLD_PAIN",         "label": "Sensitivity to cold"},
        {"code": "ENDO_HOT_PAIN",          "label": "Sensitivity to hot"},
        {"code": "ENDO_BITE_PAIN",         "label": "Pain on biting"},
        {"code": "ENDO_SINUS_TRACT",       "label": "Sinus tract"},
        {"code": "ENDO_SWELLING",          "label": "Swelling with pain"},
    ],
    "CONSERVATIVE": [
        {"code": "CONS_CARIES",           "label": "Dental caries"},
        {"code": "CONS_FRACTURE",         "label": "Fractured restoration"},
        {"code": "CONS_SECONDARY_CARIES", "label": "Secondary caries"},
        {"code": "CONS_DEFECTIVE_REST",   "label": "Defective restoration"},
        {"code": "CONS_NCCL",             "label": "Non-carious cervical lesion"},
        {"code": "CONS_DISCOLORATION",    "label": "Tooth discoloration"},
        {"code": "CONS_SENSITIVITY",      "label": "Sensitivity"},
    ],
    "PERIO": [
        {"code": "PERIO_BLEEDING",     "label": "Bleeding gums"},
        {"code": "PERIO_LOOSE_TOOTH",  "label": "Loose teeth"},
        {"code": "PERIO_HALITOSIS",    "label": "Bad breath"},
        {"code": "PERIO_SWELLING",     "label": "Gum swelling"},
        {"code": "PERIO_RECESSION",    "label": "Gum recession"},
        {"code": "PERIO_DEEP_POCKET",  "label": "Deep pocket"},
        {"code": "PERIO_ABSCESS",      "label": "Periodontal abscess"},
    ],
    "ORAL_MED": [
        {"code": "ORALMED_ULCER",             "label": "Ulcer"},
        {"code": "ORALMED_BURNING",           "label": "Burning sensation"},
        {"code": "ORALMED_WHITE_PATCH",       "label": "White patch"},
        {"code": "ORALMED_RED_PATCH",         "label": "Red patch"},
        {"code": "ORALMED_PIGMENTATION",      "label": "Oral pigmentation"},
        {"code": "ORALMED_DRY_MOUTH",         "label": "Dry mouth"},
        {"code": "ORALMED_TMJ",               "label": "TMJ pain"},
        {"code": "ORALMED_CLICKING",          "label": "Clicking jaw"},
        {"code": "ORALMED_LIMITED_OPENING",   "label": "Limited mouth opening"},
        {"code": "ORALMED_FACIAL_PAIN",       "label": "Facial pain"},
        {"code": "ORALMED_TRISMUS",           "label": "Severe trismus"},
        {"code": "ORALMED_SPACE_INFECTION",   "label": "Space infection"},
    ],
    "ORAL_SURGERY": [
        {"code": "SURGERY_IMPACTED",    "label": "Impacted tooth pain"},
        {"code": "SURGERY_SWELLING",    "label": "Facial swelling"},
        {"code": "SURGERY_SPACE_INFECTION", "label": "Space infection"},
        {"code": "SURGERY_TRAUMA",      "label": "Dental / facial trauma"},
        {"code": "SURGERY_NON_HEALING", "label": "Non-healing extraction socket"},
        {"code": "SURGERY_TRISMUS",     "label": "Limited mouth opening (Trismus)"},
        {"code": "SURGERY_WISDOM",      "label": "Wisdom tooth problem"},
    ],
    "PROSTHODONTICS": [
        {"code": "PROSTHO_MISSING_TOOTH",       "label": "Missing tooth"},
        {"code": "PROSTHO_MULTIPLE_MISSING",    "label": "Multiple missing teeth"},
        {"code": "PROSTHO_COMPLETE_EDENTULISM", "label": "Complete edentulism"},
        {"code": "PROSTHO_BROKEN_DENTURE",      "label": "Broken denture"},
        {"code": "PROSTHO_LOOSE_DENTURE",       "label": "Loose denture"},
        {"code": "PROSTHO_IMPLANT_REQUEST",     "label": "Implant request"},
    ],
    "ORTHODONTICS": [
        {"code": "ORTHO_CROWDING",     "label": "Crowding"},
        {"code": "ORTHO_SPACING",      "label": "Spacing"},
        {"code": "ORTHO_PROTRUSION",   "label": "Forwardly placed teeth"},
        {"code": "ORTHO_IRREGULAR",    "label": "Irregular teeth"},
        {"code": "ORTHO_MALOCCLUSION", "label": "Malocclusion"},
    ],
    "PEDODONTICS": [
        {"code": "PEDO_MULTIPLE_CARIES",   "label": "Multiple caries in child"},
        {"code": "PEDO_PRIMARY_TOOTH_PAIN","label": "Pain in primary tooth"},
        {"code": "PEDO_PREMATURE_LOSS",    "label": "Premature tooth loss"},
        {"code": "PEDO_DELAYED_ERUPTION",  "label": "Delayed eruption"},
        {"code": "PEDO_TRAUMA",            "label": "Trauma to tooth"},
    ],
    "IMPLANTOLOGY": [
        {"code": "IMPLANT_SINGLE_MISSING",   "label": "Single tooth implant"},
        {"code": "IMPLANT_MULTIPLE_MISSING", "label": "Multiple implants"},
        {"code": "IMPLANT_FULL_ARCH",        "label": "Full arch implant"},
        {"code": "IMPLANT_FAILURE",          "label": "Implant failure / pain"},
        {"code": "IMPLANT_PERI_IMPLANTITIS", "label": "Peri-implantitis"},
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — Examination schema  (Step 4)
# Each field: { key, label, type, options? }
# type: "select" | "number" | "boolean"
# ─────────────────────────────────────────────────────────────────────────────

EXAM_SCHEMA = {
    "ENDO": [
        {"key": "coldResponse",         "label": "Cold Test",              "type": "select",  "options": ["normal", "lingering", "no response"]},
        {"key": "spontaneousPain",      "label": "Spontaneous Pain",       "type": "select",  "options": ["yes", "no"]},
        {"key": "percussion",           "label": "Percussion",             "type": "select",  "options": ["positive", "negative"]},
        {"key": "heatResponse",         "label": "Heat Test",              "type": "select",  "options": ["normal", "lingering", "no response"]},
        {"key": "eptResponse",          "label": "EPT Response",           "type": "select",  "options": ["normal", "reduced", "no response"]},
        {"key": "palpation",            "label": "Palpation",              "type": "select",  "options": ["positive", "negative"]},
        {"key": "swelling",             "label": "Swelling",               "type": "select",  "options": ["absent", "localized", "diffuse"]},
        {"key": "sinusTract",           "label": "Sinus Tract",            "type": "select",  "options": ["present", "absent"]},
        {"key": "periapicalRadiolucency","label": "Periapical Radiolucency","type": "select",  "options": ["present", "absent"]},
    ],
    "CONSERVATIVE": [
        {"key": "cariesDepth",       "label": "Caries Depth",      "type": "select", "options": ["enamel", "dentin", "deep", "pulp exposure"]},
        {"key": "restorationStatus", "label": "Restoration Status","type": "select", "options": ["none", "intact", "defective", "fractured"]},
        {"key": "sensitivityType",   "label": "Sensitivity Type",  "type": "select", "options": ["none", "coldShort", "coldLingering", "hot", "sweet"]},
        {"key": "cervicalLesion",    "label": "Cervical Lesion",   "type": "select", "options": ["absent", "present"]},
        {"key": "pulpExposure",      "label": "Pulp Exposure",     "type": "select", "options": ["no", "yes"]},
    ],
    "PERIO": [
        {"key": "bleedingOnProbing", "label": "Bleeding on Probing", "type": "select",  "options": ["present", "absent"]},
        {"key": "pocketDepth",       "label": "Pocket Depth",        "type": "select",  "options": ["<4mm", "4-6mm", ">6mm"]},
        {"key": "mobility",          "label": "Mobility",            "type": "select",  "options": ["none", "grade1", "grade2", "grade3"]},
        {"key": "gingivalRecession", "label": "Gingival Recession",  "type": "select",  "options": ["none", "mild", "moderate", "severe"]},
        {"key": "furcation",         "label": "Furcation",           "type": "select",  "options": ["none", "grade1", "grade2", "grade3"]},
        {"key": "boneLossPattern",   "label": "Bone Loss Pattern",   "type": "select",  "options": ["none", "horizontal", "vertical", "mixed"]},
    ],
    "ORAL_MED": [
        {"key": "lesionType",          "label": "Lesion Type",            "type": "select",  "options": ["none", "ulcer", "whitePatch", "redPatch", "pigmentation", "swelling", "blister"]},
        {"key": "durationOver2Weeks",  "label": "Duration > 2 Weeks",     "type": "select",  "options": ["yes", "no"]},
        {"key": "scrapable",           "label": "Scrapable",              "type": "select",  "options": ["yes", "no"]},
        {"key": "induration",          "label": "Induration",             "type": "select",  "options": ["present", "absent"]},
        {"key": "lymphNodeInvolvement","label": "Lymph Node Involvement",  "type": "select",  "options": ["present", "absent"]},
        {"key": "recurrentEpisodes",   "label": "Recurrent Episodes",     "type": "select",  "options": ["yes", "no"]},
        {"key": "localTraumaHistory",  "label": "Local Trauma History",   "type": "select",  "options": ["present", "absent"]},
        {"key": "burningSensation",    "label": "Burning Sensation",      "type": "select",  "options": ["yes", "no"]},
        {"key": "restrictedMouthOpening","label": "Restricted Mouth Opening","type": "select","options": ["yes", "no"]},
        {"key": "tmjJointSound",       "label": "TMJ Joint Sound",        "type": "select",  "options": ["absent", "clicking", "crepitus"]},
        {"key": "osmf",                "label": "Oral Submucous Fibrosis","type": "select",  "options": ["absent", "present"]},
    ],
    "ORAL_SURGERY": [
        {"key": "impactionType",            "label": "Impaction Type",           "type": "select",  "options": ["none", "mesioangular", "distoangular", "vertical", "horizontal"]},
        {"key": "spaceInfection",           "label": "Space Infection",          "type": "select",  "options": ["none", "localized", "spreading"]},
        {"key": "trismus",                  "label": "Trismus",                  "type": "select",  "options": ["none", "mild", "severe"]},
        {"key": "fractureSuspected",        "label": "Fracture Suspected",       "type": "select",  "options": ["yes", "no"]},
        {"key": "postExtractionComplication","label": "Post Extraction Issue",   "type": "select",  "options": ["none", "drySocket", "infection", "bleeding"]},
        {"key": "tmjDislocation",           "label": "TMJ Dislocation",          "type": "select",  "options": ["yes", "no"]},
        {"key": "cysticLesion",             "label": "Cystic Lesion",            "type": "select",  "options": ["absent", "present"]},
    ],
    "PROSTHODONTICS": [
        {"key": "missingTeethCount",   "label": "Missing Teeth Count",     "type": "select",  "options": ["1", "2", "3", "4+", "full arch"]},
        {"key": "abutmentCondition",   "label": "Abutment Condition",      "type": "select",  "options": ["good", "compromised", "absent"]},
        {"key": "ridgeCondition",      "label": "Ridge Condition",         "type": "select",  "options": ["adequate", "resorbed", "knife-edge", "flat"]},
        {"key": "kennedyClass",        "label": "Kennedy Classification",  "type": "select",  "options": ["I", "II", "III", "IV"]},
        {"key": "interarchSpace",      "label": "Interarch Space",         "type": "select",  "options": ["adequate", "reduced", "increased"]},
        {"key": "bruxism",             "label": "Bruxism",                 "type": "select",  "options": ["yes", "no"]},
    ],
    "ORTHODONTICS": [
        {"key": "angleClassification",  "label": "Angle Classification",  "type": "select",  "options": ["class1", "class2div1", "class2div2", "class3"]},
        {"key": "crowdingSeverity",     "label": "Crowding Severity",      "type": "select",  "options": ["none", "mild", "moderate", "severe"]},
        {"key": "spacing",              "label": "Spacing",                "type": "select",  "options": ["absent", "present"]},
        {"key": "overjet",              "label": "Overjet",                "type": "select",  "options": ["normal", "increased", "reversed"]},
        {"key": "overbite",             "label": "Overbite",               "type": "select",  "options": ["normal", "deep", "open"]},
        {"key": "crossbite",            "label": "Crossbite",              "type": "select",  "options": ["none", "anterior", "posterior", "both"]},
        {"key": "facialProfile",        "label": "Facial Profile",         "type": "select",  "options": ["straight", "convex", "concave"]},
        {"key": "growthStatus",         "label": "Growth Status",          "type": "select",  "options": ["growing", "adult"]},
        {"key": "incisorInclination",   "label": "Incisor Inclination",    "type": "select",  "options": ["normal", "proclined", "retroclined"]},
        {"key": "lipCompetence",        "label": "Lip Competence",         "type": "select",  "options": ["competent", "incompetent"]},
        {"key": "tmjSymptoms",          "label": "TMJ Symptoms",           "type": "select",  "options": ["absent", "present"]},
    ],
    "PEDODONTICS": [
        {"key": "cariesDepthPrimary",      "label": "Caries Depth (Primary)",      "type": "select",  "options": ["enamel", "dentin", "pulp"]},
        {"key": "vitalStatus",             "label": "Vital Status",                "type": "select",  "options": ["vital", "non-vital"]},
        {"key": "multipleCaries",          "label": "Multiple Caries",             "type": "select",  "options": ["yes", "no"]},
        {"key": "rampantPattern",          "label": "Rampant Pattern",             "type": "select",  "options": ["yes", "no"]},
        {"key": "prematureLoss",           "label": "Premature Loss",              "type": "select",  "options": ["yes", "no"]},
        {"key": "spaceReduction",          "label": "Space Reduction",             "type": "select",  "options": ["yes", "no"]},
        {"key": "archLengthDiscrepancy",   "label": "Arch Length Discrepancy (mm)","type": "number"},
        {"key": "delayedEruption",         "label": "Delayed Eruption",            "type": "select",  "options": ["yes", "no"]},
        {"key": "ectopicEruption",         "label": "Ectopic Eruption",            "type": "select",  "options": ["yes", "no"]},
        {"key": "supernumeraryTooth",      "label": "Supernumerary Tooth",         "type": "select",  "options": ["yes", "no"]},
        {"key": "traumaSeverity",          "label": "Trauma Severity",             "type": "select",  "options": ["none", "mild", "moderate", "severe"]},
        {"key": "franklBehavior",          "label": "Frankl Behavior",             "type": "select",  "options": ["definitely negative", "negative", "positive", "definitely positive"]},
    ],
    "IMPLANTOLOGY": [
        {"key": "implantMobility",        "label": "Implant Mobility",           "type": "select",  "options": ["absent", "present"]},
        {"key": "periImplantPocket",      "label": "Peri-implant Pocket",        "type": "select",  "options": ["normal", "4-5mm", ">5mm"]},
        {"key": "boneLossAroundImplant",  "label": "Bone Loss Around Implant",   "type": "select",  "options": ["none", "mild", "moderate", "severe"]},
        {"key": "oralHygieneStatus",      "label": "Oral Hygiene Status",        "type": "select",  "options": ["good", "fair", "poor"]},
        {"key": "bruxismHistory",         "label": "Bruxism History",            "type": "select",  "options": ["yes", "no"]},
    ],
}
