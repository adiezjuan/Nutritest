# lab_schema_v3.py
# Schema de captura para Aging Coach v3
# Aquí solo definimos inputs y metadatos de UI/captura.
# La lógica científica vive fuera:
# - reference_ranges.py
# - scoring_tables.py
# - priority_rules.py
# - output_rules.py

SCHEMA_V3 = [
    # =========================================================
    # CONTEXTO / ANTROPOMETRÍA
    # =========================================================
    {
        "key": "age_years",
        "label": "Edad",
        "unit": "years",
        "level": "essential",
        "input_type": "number",
        "domain": "context",
        "convert_group": None,
    },
    {
        "key": "sex",
        "label": "Sexo",
        "unit": "cat",
        "level": "essential",
        "input_type": "select",
        "domain": "context",
        "convert_group": None,
        "options": ["F", "M", "X"],
        "option_labels": {
            "F": "Mujer",
            "M": "Hombre",
            "X": "Otro",
        },
    },
    {
        "key": "bmi_kg_m2",
        "label": "BMI",
        "unit": "kg/m²",
        "level": "precision",
        "input_type": "number",
        "domain": "context",
        "convert_group": None,
    },
    {
        "key": "waist_cm",
        "label": "Cintura",
        "unit": "cm",
        "level": "precision",
        "input_type": "number",
        "domain": "context",
        "convert_group": None,
    },

    # =========================================================
    # INFLAMACIÓN
    # =========================================================
    {
        "key": "hscrp_mg_l",
        "label": "hsCRP / PCR",
        "unit": "mg/L",
        "level": "precision",
        "input_type": "number",
        "domain": "inflammation",
        "convert_group": None,
    },
    {
        "key": "esr_mm_h",
        "label": "VSG (ESR)",
        "unit": "mm/h",
        "level": "advanced",
        "input_type": "number",
        "domain": "inflammation",
        "convert_group": None,
    },
    {
        "key": "fibrinogen_mg_dl",
        "label": "Fibrinógeno",
        "unit": "mg/dL",
        "level": "advanced",
        "input_type": "number",
        "domain": "inflammation",
        "convert_group": None,
    },

    # =========================================================
    # CBC / HEMOGRAMA
    # =========================================================
    {
        "key": "wbc_x10_3_mm3",
        "label": "Leucocitos",
        "unit": "x10^3/mm³",
        "level": "advanced",
        "input_type": "number",
        "domain": "cbc",
        "convert_group": None,
    },
    {
        "key": "neut_abs_x10_3_mm3",
        "label": "Neutrófilos (abs)",
        "unit": "x10^3/mm³",
        "level": "precision",
        "input_type": "number",
        "domain": "inflammation",
        "convert_group": None,
    },
    {
        "key": "lymph_abs_x10_3_mm3",
        "label": "Linfocitos (abs)",
        "unit": "x10^3/mm³",
        "level": "precision",
        "input_type": "number",
        "domain": "inflammation",
        "convert_group": None,
    },
    {
        "key": "rbc_x10_6_mm3",
        "label": "Hematíes",
        "unit": "x10^6/mm³",
        "level": "advanced",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "hb_g_dl",
        "label": "Hemoglobina",
        "unit": "g/dL",
        "level": "essential",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "hct_pct",
        "label": "Hematocrito",
        "unit": "%",
        "level": "advanced",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "mcv_fl",
        "label": "VCM (MCV)",
        "unit": "fL",
        "level": "essential",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "rdw_pct",
        "label": "RDW",
        "unit": "%",
        "level": "essential",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },

    # =========================================================
    # HIERRO / MICRONUTRIENTES HEMATOLÓGICOS
    # =========================================================
    {
        "key": "ferritin_ng_ml",
        "label": "Ferritina",
        "unit": "ng/mL",
        "level": "essential",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "iron_ug_dl",
        "label": "Hierro",
        "unit": "µg/dL",
        "level": "advanced",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "transferrin_mg_dl",
        "label": "Transferrina",
        "unit": "mg/dL",
        "level": "advanced",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "transferrin_sat_pct",
        "label": "Sat. transferrina",
        "unit": "%",
        "level": "advanced",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "tibc_ug_dl",
        "label": "TIBC",
        "unit": "µg/dL",
        "level": "advanced",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "vitb12_pg_ml",
        "label": "Vitamina B12",
        "unit": "pg/mL",
        "level": "precision",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },
    {
        "key": "folate_ng_ml",
        "label": "Folato",
        "unit": "ng/mL",
        "level": "precision",
        "input_type": "number",
        "domain": "hematology",
        "convert_group": None,
    },

    # =========================================================
    # GLUCOSA / INSULINA
    # =========================================================
    {
        "key": "glucose_mg_dl",
        "label": "Glucosa",
        "unit": "mg/dL",
        "level": "essential",
        "input_type": "number",
        "domain": "glucose",
        "convert_group": "glucose",
    },
    {
        "key": "hba1c_pct",
        "label": "HbA1c",
        "unit": "%",
        "level": "essential",
        "input_type": "number",
        "domain": "glucose",
        "convert_group": None,
    },
    {
        "key": "insulin_uIU_ml",
        "label": "Insulina",
        "unit": "µIU/mL",
        "level": "precision",
        "input_type": "number",
        "domain": "glucose",
        "convert_group": None,
    },

    # =========================================================
    # LÍPIDOS
    # =========================================================
    {
        "key": "chol_total_mg_dl",
        "label": "Colesterol total",
        "unit": "mg/dL",
        "level": "precision",
        "input_type": "number",
        "domain": "lipids",
        "convert_group": "lipids",
    },
    {
        "key": "ldl_mg_dl",
        "label": "LDL",
        "unit": "mg/dL",
        "level": "essential",
        "input_type": "number",
        "domain": "lipids",
        "convert_group": "lipids",
    },
    {
        "key": "hdl_mg_dl",
        "label": "HDL",
        "unit": "mg/dL",
        "level": "essential",
        "input_type": "number",
        "domain": "lipids",
        "convert_group": "lipids",
    },
    {
        "key": "triglycerides_mg_dl",
        "label": "Triglicéridos",
        "unit": "mg/dL",
        "level": "essential",
        "input_type": "number",
        "domain": "lipids",
        "convert_group": "triglycerides",
    },

    # =========================================================
    # HÍGADO
    # =========================================================
    {
        "key": "alt_u_l",
        "label": "ALT",
        "unit": "U/L",
        "level": "essential",
        "input_type": "number",
        "domain": "liver",
        "convert_group": None,
    },
    {
        "key": "ast_u_l",
        "label": "AST",
        "unit": "U/L",
        "level": "essential",
        "input_type": "number",
        "domain": "liver",
        "convert_group": None,
    },
    {
        "key": "ggt_u_l",
        "label": "GGT",
        "unit": "U/L",
        "level": "precision",
        "input_type": "number",
        "domain": "liver",
        "convert_group": None,
    },
    {
        "key": "alp_u_l",
        "label": "ALP",
        "unit": "U/L",
        "level": "advanced",
        "input_type": "number",
        "domain": "liver",
        "convert_group": None,
    },
    {
        "key": "bilirubin_total_mg_dl",
        "label": "Bilirrubina total",
        "unit": "mg/dL",
        "level": "advanced",
        "input_type": "number",
        "domain": "liver",
        "convert_group": None,
    },

    # =========================================================
    # RIÑÓN
    # =========================================================
    {
        "key": "creatinine_mg_dl",
        "label": "Creatinina",
        "unit": "mg/dL",
        "level": "essential",
        "input_type": "number",
        "domain": "kidney",
        "convert_group": None,
    },
    {
        "key": "urea_mg_dl",
        "label": "Urea",
        "unit": "mg/dL",
        "level": "advanced",
        "input_type": "number",
        "domain": "kidney",
        "convert_group": None,
    },
    {
        "key": "egfr_ml_min_1_73m2",
        "label": "eGFR",
        "unit": "mL/min/1.73m²",
        "level": "precision",
        "input_type": "number",
        "domain": "kidney",
        "convert_group": None,
    },
    {
        "key": "uric_acid_mg_dl",
        "label": "Ácido úrico",
        "unit": "mg/dL",
        "level": "precision",
        "input_type": "number",
        "domain": "kidney",
        "convert_group": None,
    },
]
