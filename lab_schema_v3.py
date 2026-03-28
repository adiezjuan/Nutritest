# lab_schema_v3.py
# Schema + domain master + variable rules for Aging Coach v3

SCHEMA_V3 = [
    # -------------------------
    # Contexto / antropometría
    # -------------------------
    {"key": "age_years", "label": "Edad", "unit": "years", "level": "essential", "input_type": "number", "domain": "context"},
    {"key": "sex", "label": "Sexo", "unit": "cat", "level": "essential", "input_type": "select", "domain": "context",
     "options": ["F", "M", "X"], "option_labels": {"F": "Mujer", "M": "Hombre", "X": "Otro"}},
    {"key": "bmi_kg_m2", "label": "BMI", "unit": "kg/m²", "level": "precision", "input_type": "number", "domain": "context"},
    {"key": "waist_cm", "label": "Cintura", "unit": "cm", "level": "precision", "input_type": "number", "domain": "context"},

    # -------------------------
    # Inflamación
    # -------------------------
    {"key": "hscrp_mg_l", "label": "hsCRP / PCR", "unit": "mg/L", "level": "precision", "input_type": "number", "domain": "inflammation"},
    {"key": "esr_mm_h", "label": "VSG (ESR)", "unit": "mm/h", "level": "advanced", "input_type": "number", "domain": "inflammation"},
    {"key": "fibrinogen_mg_dl", "label": "Fibrinógeno", "unit": "mg/dL", "level": "advanced", "input_type": "number", "domain": "inflammation"},

    # -------------------------
    # Hemograma / CBC
    # -------------------------
    {"key": "wbc_x10_3_mm3", "label": "Leucocitos", "unit": "x10^3/mm³", "level": "advanced", "input_type": "number", "domain": "cbc"},
    {"key": "neut_abs_x10_3_mm3", "label": "Neutrófilos (abs)", "unit": "x10^3/mm³", "level": "precision", "input_type": "number", "domain": "inflammation"},
    {"key": "lymph_abs_x10_3_mm3", "label": "Linfocitos (abs)", "unit": "x10^3/mm³", "level": "precision", "input_type": "number", "domain": "inflammation"},
    {"key": "rbc_x10_6_mm3", "label": "Hematíes", "unit": "x10^6/mm³", "level": "advanced", "input_type": "number", "domain": "hematology"},
    {"key": "hb_g_dl", "label": "Hemoglobina", "unit": "g/dL", "level": "essential", "input_type": "number", "domain": "hematology"},
    {"key": "hct_pct", "label": "Hematocrito", "unit": "%", "level": "advanced", "input_type": "number", "domain": "hematology"},
    {"key": "mcv_fl", "label": "VCM (MCV)", "unit": "fL", "level": "essential", "input_type": "number", "domain": "hematology"},
    {"key": "rdw_pct", "label": "RDW", "unit": "%", "level": "essential", "input_type": "number", "domain": "hematology"},

    # -------------------------
    # Hierro / micronutrientes
    # -------------------------
    {"key": "ferritin_ng_ml", "label": "Ferritina", "unit": "ng/mL", "level": "essential", "input_type": "number", "domain": "hematology"},
    {"key": "iron_ug_dl", "label": "Hierro", "unit": "µg/dL", "level": "advanced", "input_type": "number", "domain": "hematology"},
    {"key": "transferrin_mg_dl", "label": "Transferrina", "unit": "mg/dL", "level": "advanced", "input_type": "number", "domain": "hematology"},
    {"key": "transferrin_sat_pct", "label": "Sat. transferrina", "unit": "%", "level": "advanced", "input_type": "number", "domain": "hematology"},
    {"key": "tibc_ug_dl", "label": "TIBC", "unit": "µg/dL", "level": "advanced", "input_type": "number", "domain": "hematology"},
    {"key": "vitb12_pg_ml", "label": "Vitamina B12", "unit": "pg/mL", "level": "precision", "input_type": "number", "domain": "hematology"},
    {"key": "folate_ng_ml", "label": "Folato", "unit": "ng/mL", "level": "precision", "input_type": "number", "domain": "hematology"},

    # -------------------------
    # Glucosa / insulina
    # -------------------------
    {"key": "glucose_mg_dl", "label": "Glucosa", "unit": "mg/dL", "level": "essential", "input_type": "number", "domain": "glucose", "convert_group": "glucose"},
    {"key": "hba1c_pct", "label": "HbA1c", "unit": "%", "level": "essential", "input_type": "number", "domain": "glucose"},
    {"key": "insulin_uIU_ml", "label": "Insulina", "unit": "µIU/mL", "level": "precision", "input_type": "number", "domain": "glucose"},

    # -------------------------
    # Lípidos
    # -------------------------
    {"key": "chol_total_mg_dl", "label": "Colesterol total", "unit": "mg/dL", "level": "precision", "input_type": "number", "domain": "lipids", "convert_group": "lipids"},
    {"key": "ldl_mg_dl", "label": "LDL", "unit": "mg/dL", "level": "essential", "input_type": "number", "domain": "lipids", "convert_group": "lipids"},
    {"key": "hdl_mg_dl", "label": "HDL", "unit": "mg/dL", "level": "essential", "input_type": "number", "domain": "lipids", "convert_group": "lipids"},
    {"key": "triglycerides_mg_dl", "label": "Triglicéridos", "unit": "mg/dL", "level": "essential", "input_type": "number", "domain": "lipids", "convert_group": "triglycerides"},

    # -------------------------
    # Hígado
    # -------------------------
    {"key": "alt_u_l", "label": "ALT", "unit": "U/L", "level": "essential", "input_type": "number", "domain": "liver"},
    {"key": "ast_u_l", "label": "AST", "unit": "U/L", "level": "essential", "input_type": "number", "domain": "liver"},
    {"key": "ggt_u_l", "label": "GGT", "unit": "U/L", "level": "precision", "input_type": "number", "domain": "liver"},
    {"key": "alp_u_l", "label": "ALP", "unit": "U/L", "level": "advanced", "input_type": "number", "domain": "liver"},
    {"key": "bilirubin_total_mg_dl", "label": "Bilirrubina total", "unit": "mg/dL", "level": "advanced", "input_type": "number", "domain": "liver"},

    # -------------------------
    # Riñón
    # -------------------------
    {"key": "creatinine_mg_dl", "label": "Creatinina", "unit": "mg/dL", "level": "essential", "input_type": "number", "domain": "kidney"},
    {"key": "urea_mg_dl", "label": "Urea", "unit": "mg/dL", "level": "advanced", "input_type": "number", "domain": "kidney"},
    {"key": "egfr_ml_min_1_73m2", "label": "eGFR", "unit": "mL/min/1.73m²", "level": "precision", "input_type": "number", "domain": "kidney"},
    {"key": "uric_acid_mg_dl", "label": "Ácido úrico", "unit": "mg/dL", "level": "precision", "input_type": "number", "domain": "kidney"},
]

DOMAIN_MASTER = {
    "glucose": {
        "label": "Glucosa/insulina",
        "definition": "Prioridad cuando el mayor potencial de mejora está en la regulación glucémica y la sensibilidad a la insulina.",
        "priority_override": False,
        "variables": [
            {"key": "hba1c_pct", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 35},
            {"key": "glucose_mg_dl", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 30},
            {"key": "insulin_uIU_ml", "role": "secondary_driver", "effect_direction": "higher_worse", "weight": 20},
            {"key": "homa_ir", "role": "modulator", "effect_direction": "higher_worse", "weight": 10},
            {"key": "tg_hdl_ratio", "role": "modulator", "effect_direction": "higher_worse", "weight": 5},
        ],
    },
    "lipids": {
        "label": "Lípidos",
        "definition": "Prioridad cuando el mayor potencial de mejora está en el patrón lipídico-aterogénico, especialmente si triglicéridos y señal metabólica dominan.",
        "priority_override": False,
        "variables": [
            {"key": "triglycerides_mg_dl", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 35},
            {"key": "ldl_mg_dl", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 30},
            {"key": "tg_hdl_ratio", "role": "secondary_driver", "effect_direction": "higher_worse", "weight": 20},
            {"key": "hdl_mg_dl", "role": "modulator", "effect_direction": "lower_worse", "weight": 10},
            {"key": "non_hdl_mg_dl", "role": "modulator", "effect_direction": "higher_worse", "weight": 5},
        ],
    },
    "inflammation": {
        "label": "Inflamación",
        "definition": "Prioridad cuando la carga inflamatoria sistémica parece ser el cuello de botella principal o un modulador mayor del resto.",
        "priority_override": True,
        "variables": [
            {"key": "hscrp_mg_l", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 70},
            {"key": "nlr", "role": "secondary_driver", "effect_direction": "higher_worse", "weight": 20},
            {"key": "neut_abs_x10_3_mm3", "role": "modulator", "effect_direction": "higher_worse", "weight": 5},
            {"key": "lymph_abs_x10_3_mm3", "role": "modulator", "effect_direction": "lower_worse", "weight": 5},
        ],
    },
    "hematology": {
        "label": "Hematología",
        "definition": "Prioridad cuando la oxigenación, las reservas o la eritropoyesis limitan la intervención o explican una parte importante del cuadro.",
        "priority_override": True,
        "variables": [
            {"key": "hb_g_dl", "role": "primary_driver", "effect_direction": "lower_worse", "weight": 35},
            {"key": "ferritin_ng_ml", "role": "primary_driver", "effect_direction": "lower_worse", "weight": 30},
            {"key": "rdw_pct", "role": "secondary_driver", "effect_direction": "higher_worse", "weight": 15},
            {"key": "mcv_fl", "role": "secondary_driver", "effect_direction": "outside_range_worse", "weight": 10},
            {"key": "vitb12_pg_ml", "role": "modulator", "effect_direction": "lower_worse", "weight": 5},
            {"key": "folate_ng_ml", "role": "modulator", "effect_direction": "lower_worse", "weight": 5},
        ],
    },
    "liver": {
        "label": "Hígado",
        "definition": "Prioridad cuando la carga hepato-metabólica parece relevante para la estrategia nutricional y el seguimiento.",
        "priority_override": False,
        "variables": [
            {"key": "ggt_u_l", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 35},
            {"key": "alt_u_l", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 30},
            {"key": "ast_u_l", "role": "secondary_driver", "effect_direction": "higher_worse", "weight": 20},
            {"key": "alp_u_l", "role": "modulator", "effect_direction": "higher_worse", "weight": 10},
            {"key": "bilirubin_total_mg_dl", "role": "modulator", "effect_direction": "higher_worse", "weight": 5},
        ],
    },
    "kidney": {
        "label": "Riñón",
        "definition": "Prioridad cuando la seguridad renal o una reducción de función condiciona el plan y obliga a prudencia.",
        "priority_override": True,
        "variables": [
            {"key": "egfr_ml_min_1_73m2", "role": "primary_driver", "effect_direction": "lower_worse", "weight": 60},
            {"key": "creatinine_mg_dl", "role": "primary_driver", "effect_direction": "higher_worse", "weight": 25},
            {"key": "uric_acid_mg_dl", "role": "secondary_driver", "effect_direction": "higher_worse", "weight": 10},
            {"key": "urea_mg_dl", "role": "modulator", "effect_direction": "higher_worse", "weight": 5},
        ],
    },
}

# Reglas semilla: se ajustarán con aprendizaje del producto
# Cada regla devuelve score 0-100 según tramos
VARIABLE_RULES = {
    "hba1c_pct": {"mode": "piecewise_higher", "points": [(5.3, 0), (5.6, 20), (5.9, 50), (6.4, 80), (6.5, 95), (7.5, 100)]},
    "glucose_mg_dl": {"mode": "piecewise_higher", "points": [(90, 0), (99, 20), (109, 50), (125, 80), (126, 95), (160, 100)]},
    "insulin_uIU_ml": {"mode": "piecewise_higher", "points": [(8, 0), (12, 25), (18, 55), (25, 80), (35, 100)]},
    "homa_ir": {"mode": "piecewise_higher", "points": [(1.5, 0), (2.0, 20), (2.9, 50), (4.0, 80), (6.0, 100)]},
    "tg_hdl_ratio": {"mode": "piecewise_higher", "points": [(1.5, 0), (2.0, 20), (2.5, 40), (3.5, 70), (5.0, 100)]},

    "triglycerides_mg_dl": {"mode": "piecewise_higher", "points": [(100, 0), (149, 20), (199, 50), (299, 80), (500, 100)]},
    "ldl_mg_dl": {"mode": "piecewise_higher", "points": [(100, 0), (129, 25), (159, 55), (189, 80), (190, 100)]},
    "hdl_mg_dl": {"mode": "piecewise_lower", "points": [(60, 0), (50, 20), (40, 60), (30, 100)]},
    "non_hdl_mg_dl": {"mode": "piecewise_higher", "points": [(130, 0), (159, 25), (189, 55), (219, 80), (220, 100)]},

    "hscrp_mg_l": {"mode": "piecewise_higher", "points": [(1.0, 0), (2.0, 20), (3.0, 40), (5.0, 65), (10.0, 85), (15.0, 100)]},
    "nlr": {"mode": "piecewise_higher", "points": [(2.0, 0), (2.5, 20), (3.0, 40), (4.0, 70), (6.0, 100)]},
    "neut_abs_x10_3_mm3": {"mode": "piecewise_higher", "points": [(4.5, 0), (6.0, 20), (7.5, 50), (10.0, 100)]},
    "lymph_abs_x10_3_mm3": {"mode": "piecewise_lower", "points": [(2.0, 0), (1.5, 20), (1.0, 60), (0.7, 100)]},

    "hb_g_dl_male": {"mode": "piecewise_lower", "points": [(13.5, 0), (13.0, 20), (12.0, 50), (11.0, 80), (10.0, 100)]},
    "hb_g_dl_female": {"mode": "piecewise_lower", "points": [(12.5, 0), (12.0, 20), (11.0, 50), (10.0, 80), (9.0, 100)]},
    "hb_g_dl_other": {"mode": "piecewise_lower", "points": [(13.0, 0), (12.5, 20), (11.5, 50), (10.5, 80), (9.5, 100)]},
    "ferritin_ng_ml": {"mode": "piecewise_lower", "points": [(50, 0), (30, 20), (15, 65), (8, 100)]},
    "rdw_pct": {"mode": "piecewise_higher", "points": [(13.5, 0), (14.2, 20), (15.0, 50), (16.5, 100)]},
    "mcv_fl": {"mode": "piecewise_range", "optimal_low": 85, "optimal_high": 95,
               "outer_low": 75, "outer_high": 105, "inner_score": 20, "outer_score": 80, "extreme_score": 100},
    "vitb12_pg_ml": {"mode": "piecewise_lower", "points": [(350, 0), (300, 20), (200, 60), (150, 100)]},
    "folate_ng_ml": {"mode": "piecewise_lower", "points": [(6.0, 0), (5.0, 20), (3.5, 60), (2.0, 100)]},

    "ggt_u_l": {"mode": "piecewise_higher", "points": [(30, 0), (55, 30), (90, 65), (150, 100)]},
    "alt_u_l": {"mode": "piecewise_higher", "points": [(30, 0), (40, 20), (60, 55), (100, 85), (150, 100)]},
    "ast_u_l": {"mode": "piecewise_higher", "points": [(30, 0), (35, 20), (50, 50), (80, 85), (120, 100)]},
    "alp_u_l": {"mode": "piecewise_higher", "points": [(120, 0), (150, 30), (220, 70), (350, 100)]},
    "bilirubin_total_mg_dl": {"mode": "piecewise_higher", "points": [(1.0, 0), (1.3, 25), (2.0, 60), (3.0, 100)]},

    "egfr_ml_min_1_73m2": {"mode": "piecewise_lower", "points": [(90, 0), (75, 20), (60, 45), (45, 75), (30, 95), (15, 100)]},
    "creatinine_mg_dl": {"mode": "piecewise_higher", "points": [(0.9, 0), (1.1, 20), (1.3, 50), (1.6, 80), (2.0, 100)]},
    "uric_acid_mg_dl": {"mode": "piecewise_higher", "points": [(6.0, 0), (7.0, 25), (8.0, 60), (10.0, 100)]},
    "urea_mg_dl": {"mode": "piecewise_higher", "points": [(40, 0), (50, 20), (70, 60), (100, 100)]},
}
