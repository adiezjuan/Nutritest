# output_rules.py
# Reglas narrativas y de acciones sugeridas para construir outputs.
# Se usan después del ranking de dominios.

DOMAIN_OUTPUT_RULES = {
    "glucose": {
        "profile": "Perfil predominantemente metabólico/glucémico.",
        "main_lever": (
            "Reducir carga glucémica, priorizar proteína + fibra y mejorar "
            "sensibilidad a la insulina."
        ),
        "pattern": "Low-carb flexible",
        "repeat": (
            "Repetir glucosa, HbA1c, TG/HDL y, si se puede, insulina "
            "en 8–12 semanas."
        ),
        "actions": [
            "Reducir harinas, dulces y bebidas calóricas.",
            "Asegurar proteína + fibra en cada comida principal.",
            "Caminar 10–20 minutos después de las comidas principales.",
            "Mantener consistencia 8 semanas antes de reevaluar."
        ],
        "cautions": [
            "Si HbA1c o glucosa están en rango claramente alto, priorizar revisión médica.",
            "No hace falta ir a keto estricta por defecto; la intensidad depende de magnitud y adherencia."
        ],
    },

    "lipids": {
        "profile": "Perfil predominantemente lipídico-aterogénico.",
        "main_lever": (
            "Subir fibra soluble, mejorar calidad de grasa y reducir el contexto "
            "que empuja triglicéridos y LDL."
        ),
        "pattern": "Mediterránea alta en fibra y calidad grasa",
        "repeat": (
            "Repetir LDL, TG, HDL y no-HDL en 8–12 semanas."
        ),
        "actions": [
            "Aumentar fibra soluble diaria (legumbres, avena, psyllium si hace falta).",
            "Reducir alcohol si triglicéridos están altos.",
            "Priorizar AOVE, frutos secos y pescado frente a ultraprocesados.",
            "Mantener patrón alimentario simple y consistente."
        ],
        "cautions": [
            "Si triglicéridos son muy altos, el alcohol y la carga glucémica pesan mucho.",
            "No interpretar colesterol total aislado como eje principal si el resto del patrón no acompaña."
        ],
    },

    "inflammation": {
        "profile": "Perfil predominantemente inflamatorio.",
        "main_lever": (
            "Reducir carga fisiológica total: alcohol mínimo, comida simple, "
            "mejor sueño y menos fricción inflamatoria."
        ),
        "pattern": "Mediterránea antiinflamatoria",
        "repeat": (
            "Repetir hsCRP y hemograma diferencial en 4–8 semanas si persiste."
        ),
        "actions": [
            "Alcohol mínimo o cero mientras la señal inflamatoria siga alta.",
            "Comida poco procesada y sencilla durante varias semanas.",
            "Cuidar sueño, regularidad y estrés fisiológico.",
            "Evitar sacar conclusiones metabólicas agresivas si la inflamación domina."
        ],
        "cautions": [
            "hsCRP muy alta puede reflejar un proceso agudo y distorsionar el resto del perfil.",
            "Si la señal persiste, conviene ampliar contexto clínico."
        ],
    },

    "hematology": {
        "profile": "Perfil con prioridad hematológica.",
        "main_lever": (
            "Corregir primero reservas/eritropoyesis antes de intervenciones "
            "dietéticas intensas."
        ),
        "pattern": "Conservadora + corregir eje hematológico primero",
        "repeat": (
            "Repetir Hb, RDW, MCV, ferritina y ampliar hierro/B12/folato si procede."
        ),
        "actions": [
            "No priorizar dietas agresivas mientras el eje hematológico siga dominando.",
            "Revisar hierro, ferritina, B12 y folato según el patrón.",
            "Valorar causas de ferropenia o anemia antes de asumir que todo es dieta.",
            "Asegurar una estrategia de corrección y control antes de optimizar otros ejes."
        ],
        "cautions": [
            "Ferritina baja o Hb baja pueden cambiar por completo la tolerancia a la intervención.",
            "Evitar iniciar hierro a ciegas si no está claro el patrón."
        ],
    },

    "liver": {
        "profile": "Perfil hepato-metabólico.",
        "main_lever": (
            "Reducir alcohol, ultraprocesado y carga glucémica, con foco en "
            "cintura y consistencia."
        ),
        "pattern": "Mediterránea baja en alcohol y carga glucémica",
        "repeat": (
            "Repetir ALT, AST, GGT y TG en 8–12 semanas."
        ),
        "actions": [
            "Alcohol mínimo o cero mientras persistan enzimas elevadas.",
            "Reducir carga glucémica y ultraprocesados.",
            "Enfocar el plan a cintura y entorno metabólico, no solo a calorías.",
            "Mantener patrón simple durante varias semanas antes de reevaluar."
        ],
        "cautions": [
            "La combinación GGT + ALT suele ser más informativa que una enzima sola.",
            "Si la elevación es clara o sostenida, ampliar estudio y contexto."
        ],
    },

    "kidney": {
        "profile": "Perfil con prioridad renal/seguridad.",
        "main_lever": (
            "Prudencia con suplementos, proteína alta y estrategias extremas; "
            "individualizar el plan."
        ),
        "pattern": "Conservadora y prudente con suplementos/proteína",
        "repeat": (
            "Repetir creatinina, eGFR y ácido úrico según evolución."
        ),
        "actions": [
            "Evitar introducir suplementos innecesarios mientras el eje renal no esté claro.",
            "No usar estrategias extremas por defecto.",
            "Revisar hidratación, contexto clínico y medicación si procede.",
            "Construir una intervención simple y prudente."
        ],
        "cautions": [
            "La función renal condiciona seguridad más que estética o velocidad de cambio.",
            "Si eGFR está baja, el margen para improvisar es menor."
        ],
    },
}


PROFILE_COMBINATIONS = [
    {
        "primary": "glucose",
        "secondary": "lipids",
        "label": "Perfil metabólico-lipídico.",
        "extra_action": (
            "Además del control glucémico, insistir en fibra soluble y triglicéridos."
        ),
    },
    {
        "primary": "glucose",
        "secondary": "liver",
        "label": "Perfil metabólico con componente hepático.",
        "extra_action": (
            "Alcohol mínimo y foco fuerte en cintura/carga glucémica."
        ),
    },
    {
        "primary": "glucose",
        "secondary": "inflammation",
        "label": "Perfil metabólico con componente inflamatorio.",
        "extra_action": (
            "No basta con glucosa: conviene reducir también fricción inflamatoria total."
        ),
    },
    {
        "primary": "lipids",
        "secondary": "glucose",
        "label": "Perfil lipídico sobre base metabólica.",
        "extra_action": (
            "La mejora de triglicéridos probablemente dependa también del control glucémico."
        ),
    },
    {
        "primary": "lipids",
        "secondary": "liver",
        "label": "Perfil lipídico con componente hepato-metabólico.",
        "extra_action": (
            "Conviene trabajar triglicéridos, alcohol y cintura a la vez."
        ),
    },
    {
        "primary": "inflammation",
        "secondary": "hematology",
        "label": "Perfil inflamatorio con posible distorsión hematológica.",
        "extra_action": (
            "Conviene revisar si la inflamación está alterando la lectura del eje hematológico."
        ),
    },
    {
        "primary": "inflammation",
        "secondary": "glucose",
        "label": "Perfil inflamatorio sobre base metabólica.",
        "extra_action": (
            "La señal inflamatoria puede estar amplificando un problema metabólico subyacente."
        ),
    },
    {
        "primary": "hematology",
        "secondary": "inflammation",
        "label": "Perfil hematológico con posible componente inflamatorio.",
        "extra_action": (
            "Corregir reservas y revisar si hay inflamación distorsionando ferritina o hemograma."
        ),
    },
    {
        "primary": "hematology",
        "secondary": "glucose",
        "label": "Perfil hematológico en contexto metabólico.",
        "extra_action": (
            "Primero conviene estabilizar el eje hematológico antes de empujar estrategias metabólicas más intensas."
        ),
    },
    {
        "primary": "liver",
        "secondary": "glucose",
        "label": "Perfil hepato-metabólico con componente glucémico.",
        "extra_action": (
            "La carga glucémica probablemente esté participando en la señal hepática."
        ),
    },
    {
        "primary": "liver",
        "secondary": "lipids",
        "label": "Perfil hepático con componente lipídico.",
        "extra_action": (
            "Conviene trabajar triglicéridos, alcohol y entorno metabólico de forma conjunta."
        ),
    },
    {
        "primary": "kidney",
        "secondary": "glucose",
        "label": "Perfil renal con componente metabólico.",
        "extra_action": (
            "La estrategia debe mejorar metabolismo sin perder prudencia renal."
        ),
    },
    {
        "primary": "kidney",
        "secondary": "lipids",
        "label": "Perfil renal con componente lipídico.",
        "extra_action": (
            "Las mejoras lipídicas deben plantearse desde una estrategia segura y no agresiva."
        ),
    },
]


GLOBAL_OUTPUT_RULES = {
    "default_repeat_window_weeks": "8–12",
    "inflammation_repeat_window_weeks": "4–8",
    "consistency_message": (
        "Lo importante no es hacer un plan perfecto, sino sostener una palanca clara "
        "durante varias semanas y luego repetir los ejes alterados."
    ),
    "missing_data_message": (
        "Faltan datos para una lectura más robusta; completar los inputs esenciales "
        "mejorará mucho la confianza del motor."
    ),
}
