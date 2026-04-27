"""
Master Complaint Registry – maps complaint codes to departments.
Port of MASTER_COMPLAINT_REGISTRY.js
Each entry: {"department": "DEPT_KEY", "complaint": "display label"}
"""

MASTER_COMPLAINT_REGISTRY = {
    # ENDO
    "ENDO_SPONTANEOUS_PAIN": {"department": "ENDO", "complaint": "Spontaneous tooth pain"},
    "ENDO_NIGHT_PAIN":        {"department": "ENDO", "complaint": "Night pain"},
    "ENDO_COLD_PAIN":         {"department": "ENDO", "complaint": "Sensitivity to cold"},
    "ENDO_HOT_PAIN":          {"department": "ENDO", "complaint": "Sensitivity to hot"},
    "ENDO_BITE_PAIN":         {"department": "ENDO", "complaint": "Pain on biting"},
    "ENDO_SINUS_TRACT":       {"department": "ENDO", "complaint": "Sinus tract"},
    "ENDO_SWELLING":          {"department": "ENDO", "complaint": "Swelling with pain"},

    # CONSERVATIVE
    "CONS_CARIES":            {"department": "CONSERVATIVE", "complaint": "Dental caries"},
    "CONS_FRACTURE":          {"department": "CONSERVATIVE", "complaint": "Fractured restoration"},
    "CONS_SECONDARY_CARIES":  {"department": "CONSERVATIVE", "complaint": "Secondary caries"},
    "CONS_DEFECTIVE_REST":    {"department": "CONSERVATIVE", "complaint": "Defective restoration"},
    "CONS_NCCL":              {"department": "CONSERVATIVE", "complaint": "Non-carious cervical lesion"},
    "CONS_DISCOLORATION":     {"department": "CONSERVATIVE", "complaint": "Tooth discoloration"},
    "CONS_SENSITIVITY":       {"department": "CONSERVATIVE", "complaint": "Sensitivity"},

    # PERIO
    "PERIO_BLEEDING":         {"department": "PERIO", "complaint": "Bleeding gums"},
    "PERIO_LOOSE_TOOTH":      {"department": "PERIO", "complaint": "Loose teeth"},
    "PERIO_HALITOSIS":        {"department": "PERIO", "complaint": "Bad breath"},
    "PERIO_SWELLING":         {"department": "PERIO", "complaint": "Gum swelling"},
    "PERIO_RECESSION":        {"department": "PERIO", "complaint": "Gum recession"},
    "PERIO_DEEP_POCKET":      {"department": "PERIO", "complaint": "Deep pocket"},
    "PERIO_ABSCESS":          {"department": "PERIO", "complaint": "Periodontal abscess"},

    # ORAL MEDICINE
    "ORALMED_ULCER":          {"department": "ORAL_MED", "complaint": "Ulcer"},
    "ORALMED_BURNING":        {"department": "ORAL_MED", "complaint": "Burning sensation"},
    "ORALMED_WHITE_PATCH":    {"department": "ORAL_MED", "complaint": "White patch"},
    "ORALMED_RED_PATCH":      {"department": "ORAL_MED", "complaint": "Red patch"},
    "ORALMED_PIGMENTATION":   {"department": "ORAL_MED", "complaint": "Oral pigmentation"},
    "ORALMED_DRY_MOUTH":      {"department": "ORAL_MED", "complaint": "Dry mouth"},
    "ORALMED_TMJ":            {"department": "ORAL_MED", "complaint": "TMJ pain"},
    "ORALMED_CLICKING":       {"department": "ORAL_MED", "complaint": "Clicking jaw"},
    "ORALMED_LIMITED_OPENING":{"department": "ORAL_MED", "complaint": "Limited mouth opening"},
    "ORALMED_FACIAL_PAIN":    {"department": "ORAL_MED", "complaint": "Facial pain"},
    "ORALMED_TRISMUS":        {"department": "ORAL_MED", "complaint": "Severe trismus"},
    "ORALMED_SPACE_INFECTION":{"department": "ORAL_MED", "complaint": "Space infection"},

    # ORAL SURGERY
    "SURGERY_IMPACTED":       {"department": "ORAL_SURGERY", "complaint": "Impacted tooth pain"},
    "SURGERY_SWELLING":       {"department": "ORAL_SURGERY", "complaint": "Facial swelling"},
    "SURGERY_SPACE_INFECTION":{"department": "ORAL_SURGERY", "complaint": "Space infection"},
    "SURGERY_TRAUMA":         {"department": "ORAL_SURGERY", "complaint": "Dental / facial trauma"},
    "SURGERY_NON_HEALING":    {"department": "ORAL_SURGERY", "complaint": "Non-healing extraction socket"},
    "SURGERY_TRISMUS":        {"department": "ORAL_SURGERY", "complaint": "Limited mouth opening (Trismus)"},
    "SURGERY_WISDOM":         {"department": "ORAL_SURGERY", "complaint": "Wisdom tooth problem"},

    # PROSTHODONTICS
    "PROSTHO_MISSING_TOOTH":       {"department": "PROSTHODONTICS", "complaint": "Missing tooth"},
    "PROSTHO_MULTIPLE_MISSING":    {"department": "PROSTHODONTICS", "complaint": "Multiple missing teeth"},
    "PROSTHO_COMPLETE_EDENTULISM": {"department": "PROSTHODONTICS", "complaint": "Complete edentulism"},
    "PROSTHO_BROKEN_DENTURE":      {"department": "PROSTHODONTICS", "complaint": "Broken denture"},
    "PROSTHO_LOOSE_DENTURE":       {"department": "PROSTHODONTICS", "complaint": "Loose denture"},
    "PROSTHO_IMPLANT_REQUEST":     {"department": "PROSTHODONTICS", "complaint": "Implant request"},

    # ORTHODONTICS
    "ORTHO_CROWDING":    {"department": "ORTHODONTICS", "complaint": "Crowding"},
    "ORTHO_SPACING":     {"department": "ORTHODONTICS", "complaint": "Spacing"},
    "ORTHO_PROTRUSION":  {"department": "ORTHODONTICS", "complaint": "Forwardly placed teeth"},
    "ORTHO_IRREGULAR":   {"department": "ORTHODONTICS", "complaint": "Irregular teeth"},
    "ORTHO_MALOCCLUSION":{"department": "ORTHODONTICS", "complaint": "Malocclusion"},

    # PEDODONTICS
    "PEDO_MULTIPLE_CARIES":  {"department": "PEDODONTICS", "complaint": "Multiple caries in child"},
    "PEDO_PRIMARY_TOOTH_PAIN":{"department": "PEDODONTICS", "complaint": "Pain in primary tooth"},
    "PEDO_PREMATURE_LOSS":   {"department": "PEDODONTICS", "complaint": "Premature tooth loss"},
    "PEDO_DELAYED_ERUPTION": {"department": "PEDODONTICS", "complaint": "Delayed eruption"},
    "PEDO_TRAUMA":           {"department": "PEDODONTICS", "complaint": "Trauma to tooth"},

    # IMPLANTOLOGY
    "IMPLANT_CONSULT":       {"department": "IMPLANTOLOGY", "complaint": "Implant consultation"},
    "IMPLANT_MOBILITY":      {"department": "IMPLANTOLOGY", "complaint": "Implant mobility"},
    "IMPLANT_SWELLING":      {"department": "IMPLANTOLOGY", "complaint": "Peri-implant swelling"},
    "IMPLANT_MISSING_TOOTH": {"department": "IMPLANTOLOGY", "complaint": "Missing tooth for implant"},
    "IMPLANT_EDENTULOUS":    {"department": "IMPLANTOLOGY", "complaint": "Edentulous for implant"},
}
