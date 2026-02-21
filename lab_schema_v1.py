# lab_schema_v1.py
# Schema v1 "Aging Labs" — Core/Plus/Optional
# Used to auto-generate Streamlit forms + drive rule-based engines.

SCHEMA_V1 = [
    # -------------------------
    # Demographics & context
    # -------------------------
    {"key": "age_years", "label": "Edad", "unit": "years", "domain": "context", "level": "core", "convert_group": None},
    {"key": "sex", "label": "Sexo (F/M)", "unit": "cat", "domain": "context", "level": "core", "convert_group": None},
    {"key": "bmi_kg_m2", "label": "BMI", "unit": "kg/m²", "domain": "context", "level": "plus", "convert_group": None},
    {"key": "waist_cm", "label": "Cintura", "unit": "cm", "domain": "context", "level": "optional", "convert_group": None},

    # -------------------------
    # Inflammation / immune
    # -------------------------
    {"key": "hscrp_mg_l", "label": "hsCRP / PCR", "unit": "mg/L", "domain": "inflammation", "level": "plus", "convert_group": None},
    {"key": "esr_mm_h", "label": "VSG (ESR)", "unit": "mm/h", "domain": "inflammation", "level": "optional", "convert_group": None},
    {"key": "fibrinogen_mg_dl", "label": "Fibrinógeno", "unit": "mg/dL", "domain": "inflammation", "level": "optional", "convert_group": None},

    # -------------------------
    # CBC / Hemogram
    # -------------------------
    {"key": "wbc_x10_3_mm3", "label": "Leucocitos", "unit": "x10^3/mm³", "domain": "cbc", "level": "core", "convert_group": None},

    {"key": "neut_abs_x10_3_mm3", "label": "Neutrófilos (abs)", "unit": "x10^3/mm³", "domain": "cbc", "level": "core", "convert_group": None},
    {"key": "lymph_abs_x10_3_mm3", "label": "Linfocitos (abs)", "unit": "x10^3/mm³", "domain": "cbc", "level": "core", "convert_group": None},
    {"key": "mono_abs_x10_3_mm3", "label": "Monocitos (abs)", "unit": "x10^3/mm³", "domain": "cbc", "level": "optional", "convert_group": None},
    {"key": "eos_abs_x10_3_mm3", "label": "Eosinófilos (abs)", "unit": "x10^3/mm³", "domain": "cbc", "level": "optional", "convert_group": None},
    {"key": "baso_abs_x10_3_mm3", "label": "Basófilos (abs)", "unit": "x10^3/mm³", "domain": "cbc", "level": "optional", "convert_group": None},

    {"key": "rbc_x10_6_mm3", "label": "Hematíes", "unit": "x10^6/mm³", "domain": "cbc", "level": "core", "convert_group": None},
    {"key": "hb_g_dl", "label": "Hemoglobina", "unit": "g/dL", "domain": "hematology", "level": "core", "convert_group": None},
    {"key": "hct_pct", "label": "Hematocrito", "unit": "%", "domain": "hematology", "level": "core", "convert_group": None},
    {"key": "mcv_fl", "label": "VCM (MCV)", "unit": "fL", "domain": "hematology", "level": "core", "convert_group": None},
    {"key": "mch_pg", "label": "HCM (MCH)", "unit": "pg", "domain": "hematology", "level": "optional", "convert_group": None},
    {"key": "mchc_g_dl", "label": "CHCM (MCHC)", "unit": "g/dL", "domain": "hematology", "level": "optional", "convert_group": None},
    {"key": "rdw_pct", "label": "RDW", "unit": "%", "domain": "hematology", "level": "core", "convert_group": None},

    {"key": "plt_x10_3_mm3", "label": "Plaquetas", "unit": "x10^3/mm³", "domain": "cbc", "level": "core", "convert_group": None},
    {"key": "mpv_fl", "label": "VPM (MPV)", "unit": "fL", "domain": "cbc", "level": "optional", "convert_group": None},

    # -------------------------
    # Iron / anemia micronutrients
    # -------------------------
    {"key": "ferritin_ng_ml", "label": "Ferritina", "unit": "ng/mL", "domain": "hematology", "level": "plus", "convert_group": None},
    {"key": "iron_ug_dl", "label": "Hierro", "unit": "µg/dL", "domain": "hematology", "level": "optional", "convert_group": None},
    {"key": "transferrin_mg_dl", "label": "Transferrina", "unit": "mg/dL", "domain": "hematology", "level": "optional", "convert_group": None},
    {"key": "transferrin_sat_pct", "label": "Sat. transferrina", "unit": "%", "domain": "hematology", "level": "optional", "convert_group": None},
    {"key": "tibc_ug_dl", "label": "TIBC / capacidad fijación", "unit": "µg/dL", "domain": "hematology", "level": "optional", "convert_group": None},

    {"key": "vitb12_pg_ml", "label": "Vitamina B12", "unit": "pg/mL", "domain": "hematology", "level": "plus", "convert_group": None},
    {"key": "folate_ng_ml", "label": "Folato", "unit": "ng/mL", "domain": "hematology", "level": "plus", "convert_group": None},

    # -------------------------
    # Glucose / insulin
    # -------------------------
    {"key": "glucose_mg_dl", "label": "Glucosa", "unit": "mg/dL", "domain": "glucose", "level": "core", "convert_group": "glucose"},
    {"key": "hba1c_pct", "label": "HbA1c", "unit": "%", "domain": "glucose", "level": "plus", "convert_group": None},
    {"key": "insulin_uIU_ml", "label": "Insulina", "unit": "µIU/mL", "domain": "glucose", "level": "optional", "convert_group": None},

    # -------------------------
    # Lipids / vascular
    # -------------------------
    {"key": "chol_total_mg_dl", "label": "Colesterol total", "unit": "mg/dL", "domain": "lipids", "level": "plus", "convert_group": "lipids"},
    {"key": "ldl_mg_dl", "label": "LDL", "unit": "mg/dL", "domain": "lipids", "level": "plus", "convert_group": "lipids"},
    {"key": "hdl_mg_dl", "label": "HDL", "unit": "mg/dL", "domain": "lipids", "level": "plus", "convert_group": "lipids"},
    {"key": "triglycerides_mg_dl", "label": "Triglicéridos", "unit": "mg/dL", "domain": "lipids", "level": "plus", "convert_group": "triglycerides"},
    {"key": "apob_mg_dl", "label": "ApoB", "unit": "mg/dL", "domain": "lipids", "level": "optional", "convert_group": None},
    {"key": "lpa_mg_dl", "label": "Lp(a)", "unit": "mg/dL", "domain": "lipids", "level": "optional", "convert_group": None},

    # -------------------------
    # Liver
    # -------------------------
    {"key": "alt_u_l", "label": "ALT", "unit": "U/L", "domain": "liver", "level": "core", "convert_group": None},
    {"key": "ast_u_l", "label": "AST", "unit": "U/L", "domain": "liver", "level": "core", "convert_group": None},
    {"key": "ggt_u_l", "label": "GGT", "unit": "U/L", "domain": "liver", "level": "plus", "convert_group": None},
    {"key": "alp_u_l", "label": "Fosfatasa alcalina (ALP)", "unit": "U/L", "domain": "liver", "level": "plus", "convert_group": None},
    {"key": "bilirubin_total_mg_dl", "label": "Bilirrubina total", "unit": "mg/dL", "domain": "liver", "level": "plus", "convert_group": None},
    {"key": "total_protein_g_l", "label": "Proteínas totales", "unit": "g/L", "domain": "liver", "level": "optional", "convert_group": None},
    {"key": "albumin_g_l", "label": "Albúmina", "unit": "g/L", "domain": "liver", "level": "optional", "convert_group": None},

    # -------------------------
    # Kidney / urate
    # -------------------------
    {"key": "creatinine_mg_dl", "label": "Creatinina", "unit": "mg/dL", "domain": "kidney", "level": "core", "convert_group": None},
    {"key": "urea_mg_dl", "label": "Urea", "unit": "mg/dL", "domain": "kidney", "level": "plus", "convert_group": None},
    {"key": "egfr_ml_min_1_73m2", "label": "eGFR", "unit": "mL/min/1.73m²", "domain": "kidney", "level": "optional", "convert_group": None},
    {"key": "uric_acid_mg_dl", "label": "Ácido úrico", "unit": "mg/dL", "domain": "kidney", "level": "plus", "convert_group": None},

    # -------------------------
    # Electrolytes / minerals
    # -------------------------
    {"key": "sodium_mmol_l", "label": "Sodio", "unit": "mmol/L", "domain": "minerals", "level": "optional", "convert_group": None},
    {"key": "potassium_mmol_l", "label": "Potasio", "unit": "mmol/L", "domain": "minerals", "level": "optional", "convert_group": None},
    {"key": "chloride_mmol_l", "label": "Cloro", "unit": "mmol/L", "domain": "minerals", "level": "optional", "convert_group": None},
    {"key": "bicarbonate_mmol_l", "label": "Bicarbonato / CO₂", "unit": "mmol/L", "domain": "minerals", "level": "optional", "convert_group": None},

    {"key": "calcium_total_mg_dl", "label": "Calcio total", "unit": "mg/dL", "domain": "minerals", "level": "plus", "convert_group": None},
    {"key": "phosphate_mg_dl", "label": "Fosfato", "unit": "mg/dL", "domain": "minerals", "level": "optional", "convert_group": None},
    {"key": "magnesium_mg_dl", "label": "Magnesio", "unit": "mg/dL", "domain": "minerals", "level": "optional", "convert_group": None},

    # -------------------------
    # Vitamins / methylation proxy
    # -------------------------
    {"key": "vitd_25oh_ng_ml", "label": "25(OH) Vitamina D", "unit": "ng/mL", "domain": "vitamins", "level": "plus", "convert_group": None},
    {"key": "homocysteine_umol_l", "label": "Homocisteína", "unit": "µmol/L", "domain": "vascular", "level": "optional", "convert_group": None},

    # -------------------------
    # Thyroid
    # -------------------------
    {"key": "tsh_mU_l", "label": "TSH", "unit": "mU/L", "domain": "thyroid", "level": "plus", "convert_group": None},
    {"key": "ft4_ng_dl", "label": "T4 libre (FT4)", "unit": "ng/dL", "domain": "thyroid", "level": "optional", "convert_group": None},
    {"key": "ft3_pg_ml", "label": "T3 libre (FT3)", "unit": "pg/mL", "domain": "thyroid", "level": "optional", "convert_group": None},

    # -------------------------
    # Optional hormones (module)
    # -------------------------
    {"key": "testosterone_total_ng_ml", "label": "Testosterona total", "unit": "ng/mL", "domain": "hormones", "level": "optional", "convert_group": None},
    {"key": "dheas_umol_l", "label": "DHEA-S", "unit": "µmol/L", "domain": "hormones", "level": "optional", "convert_group": None},
    {"key": "lh_ui_l", "label": "LH", "unit": "UI/L", "domain": "hormones", "level": "optional", "convert_group": None},
    {"key": "fsh_ui_l", "label": "FSH", "unit": "UI/L", "domain": "hormones", "level": "optional", "convert_group": None},
]