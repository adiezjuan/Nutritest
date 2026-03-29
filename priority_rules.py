# priority_rules.py
# Reglas externas de prioridad del motor.
# Se aplican después del scoring por variable y por dominio.

PRIORITY_RULES = [
    # =========================================================
    # HEMATOLOGÍA — overrides fuertes
    # =========================================================
    {
        "id": "hematology_override_low_hb",
        "domain": "hematology",
        "type": "override",
        "priority": 100,
        "conditions": [
            {"key": "hb_g_dl", "op": "<", "value": 11.5}
        ],
        "reason": "El eje hematológico fuerza prioridad por impacto funcional y seguridad.",
        "notes": "Hb claramente baja: no conviene priorizar intervenciones agresivas sin corregir esto."
    },
    {
        "id": "hematology_override_hb_ferritin_rdw",
        "domain": "hematology",
        "type": "override",
        "priority": 95,
        "conditions": [
            {"key": "hb_g_dl", "op": "<", "value": 12.0},
            {"key": "ferritin_ng_ml", "op": "<", "value": 15},
            {"key": "rdw_pct", "op": ">", "value": 14.5}
        ],
        "reason": "Combinación compatible con prioridad hematológica.",
        "notes": "Patrón compatible con anemia/ferropenia funcionalmente relevante."
    },
    {
        "id": "hematology_boost_low_ferritin",
        "domain": "hematology",
        "type": "boost",
        "boost": 12,
        "priority": 50,
        "conditions": [
            {"key": "ferritin_ng_ml", "op": "<", "value": 20}
        ],
        "reason": "Ferritina baja: el eje hematológico gana relevancia práctica.",
        "notes": "No siempre fuerza prioridad, pero sí merece subir."
    },

    # =========================================================
    # RIÑÓN — overrides por seguridad
    # =========================================================
    {
        "id": "kidney_override_low_egfr",
        "domain": "kidney",
        "type": "override",
        "priority": 100,
        "conditions": [
            {"key": "egfr_ml_min_1_73m2", "op": "<", "value": 60}
        ],
        "reason": "El eje renal fuerza prioridad por seguridad.",
        "notes": "La función renal reducida condiciona suplementos y estrategias intensas."
    },
    {
        "id": "kidney_boost_low_egfr_urate",
        "domain": "kidney",
        "type": "boost",
        "boost": 10,
        "priority": 60,
        "conditions": [
            {"key": "egfr_ml_min_1_73m2", "op": "<", "value": 75},
            {"key": "uric_acid_mg_dl", "op": ">", "value": 7.0}
        ],
        "reason": "Combinación renal-metabólica: el dominio riñón sube de relevancia.",
        "notes": "No es override total, pero sí patrón que justifica prudencia extra."
    },

    # =========================================================
    # INFLAMACIÓN — overrides / boosts
    # =========================================================
    {
        "id": "inflammation_override_high_hscrp",
        "domain": "inflammation",
        "type": "override",
        "priority": 100,
        "conditions": [
            {"key": "hscrp_mg_l", "op": ">=", "value": 10}
        ],
        "reason": "La señal inflamatoria fuerza revisión previa.",
        "notes": "hsCRP muy alta sugiere prudencia antes de interpretar todo como metabolismo."
    },
    {
        "id": "inflammation_boost_hscrp_nlr",
        "domain": "inflammation",
        "type": "boost",
        "boost": 12,
        "priority": 70,
        "conditions": [
            {"key": "hscrp_mg_l", "op": ">=", "value": 3.0},
            {"key": "nlr", "op": ">=", "value": 3.0}
        ],
        "reason": "PCR y NLR elevadas refuerzan un patrón inflamatorio consistente.",
        "notes": "Hace más sólido el dominio inflamación."
    },

    # =========================================================
    # GLUCOSA — overrides / boosts
    # =========================================================
    {
        "id": "glucose_override_diabetes_range",
        "domain": "glucose",
        "type": "override",
        "priority": 90,
        "conditions": [
            {
                "any": [
                    {"key": "hba1c_pct", "op": ">=", "value": 6.5},
                    {"key": "glucose_mg_dl", "op": ">=", "value": 126}
                ]
            }
        ],
        "reason": "El eje glucémico sube de prioridad por magnitud de alteración.",
        "notes": "Magnitud suficiente como para dominar el plan."
    },
    {
        "id": "glucose_boost_hba1c_tghdl",
        "domain": "glucose",
        "type": "boost",
        "boost": 10,
        "priority": 70,
        "conditions": [
            {"key": "hba1c_pct", "op": ">=", "value": 5.8},
            {"key": "tg_hdl_ratio", "op": ">=", "value": 2.5}
        ],
        "reason": "HbA1c y TG/HDL elevadas refuerzan un patrón metabólico-glucémico.",
        "notes": "Muy útil en perfiles de insulinorresistencia."
    },
    {
        "id": "glucose_boost_insulin_homa",
        "domain": "glucose",
        "type": "boost",
        "boost": 8,
        "priority": 65,
        "conditions": [
            {
                "any": [
                    {"key": "insulin_uIU_ml", "op": ">=", "value": 12},
                    {"key": "homa_ir", "op": ">=", "value": 2.5}
                ]
            }
        ],
        "reason": "Insulina/HOMA elevadas mejoran la señal del eje glucémico.",
        "notes": "No fuerza prioridad, pero sí sube la resolución del dominio."
    },

    # =========================================================
    # LÍPIDOS — boosts
    # =========================================================
    {
        "id": "lipids_boost_tg_ldl",
        "domain": "lipids",
        "type": "boost",
        "boost": 10,
        "priority": 60,
        "conditions": [
            {"key": "triglycerides_mg_dl", "op": ">=", "value": 200},
            {"key": "ldl_mg_dl", "op": ">=", "value": 130}
        ],
        "reason": "TG y LDL elevadas refuerzan prioridad lipídica.",
        "notes": "Patrón con carga lipídica más clara."
    },
    {
        "id": "lipids_boost_tghdl_pattern",
        "domain": "lipids",
        "type": "boost",
        "boost": 8,
        "priority": 55,
        "conditions": [
            {"key": "tg_hdl_ratio", "op": ">=", "value": 3.0}
        ],
        "reason": "TG/HDL elevada refuerza patrón lipídico-aterogénico.",
        "notes": "Especialmente útil cuando HDL acompaña mal."
    },

    # =========================================================
    # HÍGADO — boosts / pseudo override funcional
    # =========================================================
    {
        "id": "liver_boost_ggt_alt",
        "domain": "liver",
        "type": "boost",
        "boost": 12,
        "priority": 75,
        "conditions": [
            {"key": "ggt_u_l", "op": ">=", "value": 80},
            {"key": "alt_u_l", "op": ">=", "value": 60}
        ],
        "reason": "Patrón hepato-metabólico combinado.",
        "notes": "La combinación GGT + ALT es más informativa que una enzima sola."
    },
    {
        "id": "liver_boost_ast_alt_ggt",
        "domain": "liver",
        "type": "boost",
        "boost": 8,
        "priority": 65,
        "conditions": [
            {"key": "ast_u_l", "op": ">=", "value": 50},
            {"key": "alt_u_l", "op": ">=", "value": 50},
            {"key": "ggt_u_l", "op": ">=", "value": 50}
        ],
        "reason": "Patrón hepático multienzimático.",
        "notes": "No fuerza prioridad, pero sí eleva mucho la relevancia hepática."
    },

    # =========================================================
    # COMBINACIONES CRUZADAS ÚTILES
    # =========================================================
    {
        "id": "glucose_liver_metabolic_bridge",
        "domain": "glucose",
        "type": "boost",
        "boost": 6,
        "priority": 50,
        "conditions": [
            {"key": "tg_hdl_ratio", "op": ">=", "value": 2.5},
            {"key": "ggt_u_l", "op": ">=", "value": 40}
        ],
        "reason": "Patrón metabólico con posible componente hepático.",
        "notes": "Sirve para que el eje glucosa no ignore una señal hepática asociada."
    },
    {
        "id": "lipids_glucose_bridge",
        "domain": "lipids",
        "type": "boost",
        "boost": 5,
        "priority": 45,
        "conditions": [
            {"key": "triglycerides_mg_dl", "op": ">=", "value": 150},
            {"key": "hba1c_pct", "op": ">=", "value": 5.7}
        ],
        "reason": "El patrón lipídico se refuerza en contexto metabólico alterado.",
        "notes": "Útil para perfiles mixtos."
    },
]
