# scoring_tables.py
# Tabla maestra de dominios y ponderaciones del motor.
# Se diseña para ser ajustable sin tocar app.py.

DOMAIN_MASTER = {
    "glucose": {
        "label": "Glucosa/insulina",
        "definition": (
            "Prioridad cuando el mayor potencial de mejora está en la regulación "
            "glucémica y la sensibilidad a la insulina."
        ),
        "priority_override": False,
        "variables": [
            {
                "key": "hba1c_pct",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 35,
                "notes": "Marcador más estable del eje glucémico."
            },
            {
                "key": "glucose_mg_dl",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 30,
                "notes": "Muy habitual y muy accionable."
            },
            {
                "key": "insulin_uIU_ml",
                "role": "secondary_driver",
                "effect_direction": "higher_worse",
                "weight": 20,
                "notes": "Si está disponible, mejora mucho la detección temprana."
            },
            {
                "key": "homa_ir",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 10,
                "notes": "Derivado útil si hay glucosa + insulina."
            },
            {
                "key": "tg_hdl_ratio",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 5,
                "notes": "Puente metabólico útil."
            },
            {
                "key": "waist_cm",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Contexto metabólico futuro."
            },
            {
                "key": "bmi_kg_m2",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Contexto general; menos específico que cintura."
            },
        ],
    },

    "lipids": {
        "label": "Lípidos",
        "definition": (
            "Prioridad cuando el mayor potencial de mejora está en el patrón "
            "lipídico-aterogénico, especialmente si triglicéridos y señal metabólica dominan."
        ),
        "priority_override": False,
        "variables": [
            {
                "key": "triglycerides_mg_dl",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 35,
                "notes": "Muy accionable y central en patrón metabólico-lipídico."
            },
            {
                "key": "ldl_mg_dl",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 30,
                "notes": "Driver lipídico clásico."
            },
            {
                "key": "tg_hdl_ratio",
                "role": "secondary_driver",
                "effect_direction": "higher_worse",
                "weight": 20,
                "notes": "Refina el patrón aterogénico-metabólico."
            },
            {
                "key": "hdl_mg_dl",
                "role": "modulator",
                "effect_direction": "lower_worse",
                "weight": 10,
                "notes": "Aislado pesa menos, pero modula bien el patrón."
            },
            {
                "key": "non_hdl_mg_dl",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 5,
                "notes": "Complemento útil si está calculado."
            },
            {
                "key": "chol_total_mg_dl",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Menos útil en solitario."
            },
        ],
    },

    "inflammation": {
        "label": "Inflamación",
        "definition": (
            "Prioridad cuando la carga inflamatoria sistémica parece ser el cuello "
            "de botella principal o un modulador mayor del resto."
        ),
        "priority_override": True,
        "variables": [
            {
                "key": "hscrp_mg_l",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 70,
                "notes": "Mejor marcador único del eje."
            },
            {
                "key": "nlr",
                "role": "secondary_driver",
                "effect_direction": "higher_worse",
                "weight": 20,
                "notes": "Complementa bien la PCR."
            },
            {
                "key": "neut_abs_x10_3_mm3",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 5,
                "notes": "Parte del NLR."
            },
            {
                "key": "lymph_abs_x10_3_mm3",
                "role": "modulator",
                "effect_direction": "lower_worse",
                "weight": 5,
                "notes": "Parte del NLR."
            },
            {
                "key": "fibrinogen_mg_dl",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Reservado para afinado posterior."
            },
            {
                "key": "esr_mm_h",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Más inespecífico."
            },
            {
                "key": "wbc_x10_3_mm3",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Contexto del hemograma."
            },
        ],
    },

    "hematology": {
        "label": "Hematología",
        "definition": (
            "Prioridad cuando la oxigenación, las reservas o la eritropoyesis "
            "limitan la intervención o explican una parte importante del cuadro."
        ),
        "priority_override": True,
        "variables": [
            {
                "key": "hb_g_dl",
                "role": "primary_driver",
                "effect_direction": "lower_worse",
                "weight": 35,
                "notes": "Marcador funcional central del dominio."
            },
            {
                "key": "ferritin_ng_ml",
                "role": "primary_driver",
                "effect_direction": "lower_worse",
                "weight": 30,
                "notes": "Reserva de hierro muy accionable."
            },
            {
                "key": "rdw_pct",
                "role": "secondary_driver",
                "effect_direction": "higher_worse",
                "weight": 15,
                "notes": "Muy útil para heterogeneidad eritrocitaria."
            },
            {
                "key": "mcv_fl",
                "role": "secondary_driver",
                "effect_direction": "outside_range_worse",
                "weight": 10,
                "notes": "Micro o macrocitosis afinan el patrón."
            },
            {
                "key": "vitb12_pg_ml",
                "role": "modulator",
                "effect_direction": "lower_worse",
                "weight": 5,
                "notes": "Afinador prudente."
            },
            {
                "key": "folate_ng_ml",
                "role": "modulator",
                "effect_direction": "lower_worse",
                "weight": 5,
                "notes": "Afinador prudente."
            },
            {
                "key": "transferrin_sat_pct",
                "role": "modulator",
                "effect_direction": "lower_worse",
                "weight": 0,
                "notes": "Muy útil para siguientes versiones."
            },
            {
                "key": "iron_ug_dl",
                "role": "context",
                "effect_direction": "lower_worse",
                "weight": 0,
                "notes": "Variable contextual, menos robusta aislada."
            },
            {
                "key": "transferrin_mg_dl",
                "role": "context",
                "effect_direction": "outside_range_worse",
                "weight": 0,
                "notes": "Afinador futuro."
            },
            {
                "key": "tibc_ug_dl",
                "role": "context",
                "effect_direction": "outside_range_worse",
                "weight": 0,
                "notes": "Afinador futuro."
            },
            {
                "key": "hct_pct",
                "role": "context",
                "effect_direction": "lower_worse",
                "weight": 0,
                "notes": "Apoyo al patrón hematológico."
            },
            {
                "key": "rbc_x10_6_mm3",
                "role": "context",
                "effect_direction": "lower_worse",
                "weight": 0,
                "notes": "Apoyo eritrocitario."
            },
        ],
    },

    "liver": {
        "label": "Hígado",
        "definition": (
            "Prioridad cuando la carga hepato-metabólica parece relevante para "
            "la estrategia nutricional y el seguimiento."
        ),
        "priority_override": False,
        "variables": [
            {
                "key": "ggt_u_l",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 35,
                "notes": "Muy útil para carga hepato-metabólica y alcohol."
            },
            {
                "key": "alt_u_l",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 30,
                "notes": "Driver importante del eje hepático."
            },
            {
                "key": "ast_u_l",
                "role": "secondary_driver",
                "effect_direction": "higher_worse",
                "weight": 20,
                "notes": "Complementa ALT."
            },
            {
                "key": "alp_u_l",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 10,
                "notes": "Aporta contexto."
            },
            {
                "key": "bilirubin_total_mg_dl",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 5,
                "notes": "Menos central para este caso de uso."
            },
            {
                "key": "triglycerides_mg_dl",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Puente con entorno metabólico."
            },
            {
                "key": "waist_cm",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Contexto metabólico."
            },
            {
                "key": "alcohol",
                "role": "context",
                "effect_direction": "higher_worse",
                "weight": 0,
                "notes": "Contexto conductual."
            },
        ],
    },

    "kidney": {
        "label": "Riñón",
        "definition": (
            "Prioridad cuando la seguridad renal o una reducción de función "
            "condiciona el plan y obliga a prudencia."
        ),
        "priority_override": True,
        "variables": [
            {
                "key": "egfr_ml_min_1_73m2",
                "role": "primary_driver",
                "effect_direction": "lower_worse",
                "weight": 60,
                "notes": "Mejor medida renal si está disponible."
            },
            {
                "key": "creatinine_mg_dl",
                "role": "primary_driver",
                "effect_direction": "higher_worse",
                "weight": 25,
                "notes": "Proxy renal básico."
            },
            {
                "key": "uric_acid_mg_dl",
                "role": "secondary_driver",
                "effect_direction": "higher_worse",
                "weight": 10,
                "notes": "Apoyo renal-metabólico útil."
            },
            {
                "key": "urea_mg_dl",
                "role": "modulator",
                "effect_direction": "higher_worse",
                "weight": 5,
                "notes": "Más contextual que decisiva."
            },
        ],
    },
}
