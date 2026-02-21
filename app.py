# app.py
import numpy as np
import streamlit as st
from lab_schema_v1 import SCHEMA_V1

st.set_page_config(page_title="Aging Coach v1 (Schema-driven)", layout="wide")
st.title("Aging Coach v1 — Schema-driven (Labs → Diet Pattern + Supplements)")
st.caption("⚠️ Prototipo educativo/I+D. No es diagnóstico ni prescripción. Si hay valores muy alterados, consulta con un profesional.")

# -----------------------------
# Unit conversions
# -----------------------------
LIPID_MGDL_TO_MMOLL = 0.02586   # Chol/LDL/HDL
TG_MGDL_TO_MMOLL = 0.01129
GLU_MGDL_TO_MMOLL = 0.0555

def clamp01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))

def bucket(score: float) -> str:
    if score < 30: return "Bajo"
    if score < 60: return "Moderado"
    return "Alto"

def is_nan(x) -> bool:
    return x is None or (isinstance(x, float) and np.isnan(x))

def parse_float_or_nan(raw: str) -> float:
    raw = (raw or "").strip().replace(",", ".")
    if raw == "":
        return np.nan
    try:
        return float(raw)
    except ValueError:
        return np.nan

def mgdl_to_display(x_mgdl: float, convert_group: str, unit_mode: str) -> float:
    if is_nan(x_mgdl): return x_mgdl
    if unit_mode == "mg/dL": return x_mgdl
    if convert_group == "lipids": return x_mgdl * LIPID_MGDL_TO_MMOLL
    if convert_group == "triglycerides": return x_mgdl * TG_MGDL_TO_MMOLL
    if convert_group == "glucose": return x_mgdl * GLU_MGDL_TO_MMOLL
    return x_mgdl

def display_to_mgdl(x_display: float, convert_group: str, unit_mode: str) -> float:
    if is_nan(x_display): return x_display
    if unit_mode == "mg/dL": return x_display
    if convert_group == "lipids": return x_display / LIPID_MGDL_TO_MMOLL
    if convert_group == "triglycerides": return x_display / TG_MGDL_TO_MMOLL
    if convert_group == "glucose": return x_display / GLU_MGDL_TO_MMOLL
    return x_display

# -----------------------------
# Rule-based domain scoring (0 best → 100 worst)
# -----------------------------
def score_inflammation(age, hscrp, nlr=None):
    if is_nan(hscrp):
        crp_r = 0.35
    else:
        crp_r = clamp01((hscrp - 1.0) / 4.0)  # 1→0, 5→1

    age_r = clamp01((age - 40) / 40.0)
    base = 100.0 * (0.85 * crp_r + 0.15 * age_r)

    drivers = []
    if not is_nan(hscrp): drivers.append(f"hsCRP {hscrp:.2f} mg/L")

    if nlr is not None and not is_nan(nlr):
        nlr_r = clamp01((nlr - 2.0) / 3.0)
        base = 0.75 * base + 25.0 * nlr_r
        drivers.append(f"NLR {nlr:.2f}")

    return float(np.clip(base, 0, 100)), drivers

def score_lipids(ldl_mgdl, hdl_mgdl, tg_mgdl):
    if is_nan(ldl_mgdl):
        ldl_r = 0.35
    else:
        ldl_r = clamp01((ldl_mgdl - 100.0) / 70.0)  # 100→0, 170→1

    tg_hdl = np.nan
    if (not is_nan(hdl_mgdl)) and (not is_nan(tg_mgdl)) and hdl_mgdl > 0:
        tg_hdl = tg_mgdl / hdl_mgdl
        tg_hdl_r = clamp01((tg_hdl - 2.0) / 3.0)
    else:
        tg_hdl_r = 0.35

    score = 100.0 * (0.65 * ldl_r + 0.35 * tg_hdl_r)

    drivers = []
    if not is_nan(ldl_mgdl): drivers.append(f"LDL {ldl_mgdl:.0f} mg/dL")
    if not is_nan(tg_hdl): drivers.append(f"TG/HDL {tg_hdl:.2f}")

    return float(np.clip(score, 0, 100)), drivers, tg_hdl

def score_glucose(hba1c, glucose_mgdl, insulin_uIU_ml=None):
    if is_nan(hba1c):
        a1c_r = 0.35
    else:
        a1c_r = clamp01((hba1c - 5.3) / 1.2)  # 5.3→0, 6.5→1

    if is_nan(glucose_mgdl):
        glu_r = 0.35
    else:
        glu_r = clamp01((glucose_mgdl - 90.0) / 50.0)  # 90→0, 140→1

    base = 100.0 * (0.75 * a1c_r + 0.25 * glu_r)

    homa = np.nan
    drivers = []
    if not is_nan(hba1c): drivers.append(f"HbA1c {hba1c:.2f}%")
    if not is_nan(glucose_mgdl): drivers.append(f"Glucosa {glucose_mgdl:.0f} mg/dL")

    if insulin_uIU_ml is not None and (not is_nan(insulin_uIU_ml)) and (not is_nan(glucose_mgdl)):
        homa = (glucose_mgdl * insulin_uIU_ml) / 405.0
        homa_r = clamp01((homa - 1.5) / 2.5)  # 1.5→0, 4→1
        base = 0.80 * base + 20.0 * homa_r
        drivers.append(f"HOMA-IR {homa:.2f}")

    return float(np.clip(base, 0, 100)), drivers, homa

def score_hematology(sex_code, hb, mcv, rdw, ferritin, vitb12=None, folate=None):
    # Sex thresholds: conservative and transparent.
    # For X/Other, use a midpoint to avoid bias.
    if sex_code == "M":
        hb_thr = 13.0
    elif sex_code == "F":
        hb_thr = 12.0
    else:
        hb_thr = 12.5

    hb_r = 0.35 if is_nan(hb) else clamp01((hb_thr - hb) / 2.0)
    rdw_r = 0.35 if is_nan(rdw) else clamp01((rdw - 13.5) / 2.5)
    mcv_r = 0.0 if is_nan(mcv) else clamp01((90.0 - mcv) / 15.0)

    fer_low_r = 0.35 if is_nan(ferritin) else (clamp01((30.0 - ferritin) / 25.0) if ferritin < 30 else 0.0)

    # B12/folate: only gently influence in v1 (avoid over-interpretation)
    b12_r = 0.0
    if vitb12 is not None and (not is_nan(vitb12)):
        b12_r = clamp01((350.0 - vitb12) / 200.0)  # soft
    fol_r = 0.0
    if folate is not None and (not is_nan(folate)):
        fol_r = clamp01((6.0 - folate) / 3.0)      # soft

    score = 100.0 * (0.40 * hb_r + 0.28 * rdw_r + 0.14 * fer_low_r + 0.10 * mcv_r + 0.04 * b12_r + 0.04 * fol_r)

    drivers = []
    if not is_nan(hb): drivers.append(f"Hb {hb:.2f} g/dL (umbral {hb_thr:.1f})")
    if not is_nan(rdw): drivers.append(f"RDW {rdw:.2f}%")
    if not is_nan(mcv): drivers.append(f"MCV {mcv:.1f} fL")
    if not is_nan(ferritin): drivers.append(f"Ferritina {ferritin:.0f} ng/mL")
    if vitb12 is not None and not is_nan(vitb12): drivers.append(f"B12 {vitb12:.0f} pg/mL")
    if folate is not None and not is_nan(folate): drivers.append(f"Folato {folate:.1f} ng/mL")

    return float(np.clip(score, 0, 100)), drivers

def score_liver(ast, alt, ggt=None, alp=None, bili=None):
    def enz_r(x, thr):
        return 0.35 if is_nan(x) else clamp01((x - thr) / thr)

    alt_r = enz_r(alt, 40.0)
    ast_r = enz_r(ast, 35.0)
    ggt_r = 0.35 if (ggt is None or is_nan(ggt)) else clamp01((ggt - 55.0) / 55.0)
    alp_r = 0.35 if (alp is None or is_nan(alp)) else clamp01((alp - 120.0) / 120.0)
    bili_r = 0.35 if (bili is None or is_nan(bili)) else clamp01((bili - 1.0) / 1.0)

    score = 100.0 * (0.35 * alt_r + 0.25 * ast_r + 0.15 * ggt_r + 0.15 * alp_r + 0.10 * bili_r)

    drivers = []
    if not is_nan(alt): drivers.append(f"ALT {alt:.0f} U/L")
    if not is_nan(ast): drivers.append(f"AST {ast:.0f} U/L")
    if ggt is not None and not is_nan(ggt): drivers.append(f"GGT {ggt:.0f} U/L")
    if alp is not None and not is_nan(alp): drivers.append(f"ALP {alp:.0f} U/L")
    if bili is not None and not is_nan(bili): drivers.append(f"Bilirrubina {bili:.2f} mg/dL")

    return float(np.clip(score, 0, 100)), drivers

def score_kidney(creatinine, egfr=None, urate=None):
    drivers = []
    if egfr is not None and not is_nan(egfr):
        egfr_r = clamp01((90.0 - egfr) / 40.0)  # 90→0, 50→1
        score = 100.0 * egfr_r
        drivers.append(f"eGFR {egfr:.0f}")
    else:
        cr_r = 0.35 if is_nan(creatinine) else clamp01((creatinine - 0.9) / 0.7)
        score = 100.0 * cr_r
        if not is_nan(creatinine):
            drivers.append(f"Creatinina {creatinine:.2f} mg/dL")

    if urate is not None and not is_nan(urate):
        # mild contribution
        ur_r = clamp01((urate - 6.0) / 3.0)
        score = float(np.clip(0.85 * score + 15.0 * ur_r, 0, 100))
        drivers.append(f"Ácido úrico {urate:.1f} mg/dL")

    return float(np.clip(score, 0, 100)), drivers

# -----------------------------
# Decision engine (diet + supplements)
# -----------------------------
def choose_diet(scores, ctx, derived):
    infl, lip, glu, hem, liv, ren = scores
    flags = []

    hscrp = ctx.get("hscrp_mg_l", np.nan)
    hba1c = ctx.get("hba1c_pct", np.nan)
    egfr = ctx.get("egfr_ml_min_1_73m2", np.nan)
    hb = ctx.get("hb_g_dl", np.nan)
    ferritin = ctx.get("ferritin_ng_ml", np.nan)

    tg_hdl = derived.get("tg_hdl_ratio", np.nan)
    homa = derived.get("homa_ir", np.nan)

    # guardrails
    if not is_nan(hscrp) and hscrp >= 10:
        flags.append("hsCRP/PCR ≥10 mg/L: posible inflamación/infección activa → revisar antes de cambios agresivos.")
    if not is_nan(hba1c) and hba1c >= 6.5:
        flags.append("HbA1c ≥6.5%: compatible con diabetes → evaluación médica.")
    if not is_nan(egfr) and egfr < 60:
        flags.append("eGFR <60: precaución con proteína/suplementos; individualizar con profesional.")
    if not is_nan(hb) and hb < 10.5:
        flags.append("Hemoglobina muy baja: requiere evaluación médica.")
    if not is_nan(ferritin) and ferritin < 15:
        flags.append("Ferritina muy baja: probable ferropenia → no improvisar; revisar con pauta profesional.")

    anemia_priority = hem >= 70

    lowcarb_trigger = (glu >= 60) or ((not is_nan(tg_hdl)) and tg_hdl >= 2.5) or ((not is_nan(homa)) and homa >= 2.5)
    mediterr_trigger = (infl >= 60 and glu < 55)
    goal = ctx.get("goal", "Optimización")
    paleo_trigger = (goal == "Optimización" and max(scores) < 60)

    if anemia_priority:
        diet = "Conservadora + corregir eje hematológico primero"
        rationale = ["Hematología domina: priorizar causas (hierro/B12/folato/inflamación) antes de dietas agresivas."]
    elif lowcarb_trigger:
        diet = "Low-carb flexible"
        rationale = ["Eje glucémico/insulina o TG/HDL elevado → reducir carga glucémica suele ser la palanca principal."]
        if glu >= 75 or ((not is_nan(hba1c)) and hba1c >= 6.0):
            rationale.append("Low-carb más estricto (incluso keto) puede ser herramienta temporal si se tolera y no hay contraindicaciones.")
    elif mediterr_trigger:
        diet = "Mediterránea antiinflamatoria (alta en fibra y polifenoles)"
        rationale = ["Inflamación domina con glucosa relativamente estable: priorizar fibra, polifenoles, AOVE, legumbres y pescado."]
    elif paleo_trigger:
        diet = "Paleo limpia (densidad nutricional alta)"
        rationale = ["Ejes alineados: una fase de comida mínimamente procesada y alta en micronutrientes puede optimizar señal fisiológica."]
    else:
        diet = "Mediterránea base con ajustes por dominio"
        rationale = ["Patrón robusto por defecto; se ajusta el énfasis (fibra/low-carb/antiinflamatorio) según el dominio limitante."]

    return diet, rationale, flags

def choose_supplements(scores, ctx, derived):
    infl, lip, glu, hem, liv, ren = scores
    sups = []
    cautions = []

    tg = ctx.get("triglycerides_mg_dl", np.nan)
    ferritin = ctx.get("ferritin_ng_ml", np.nan)
    meds = ctx.get("meds", False)
    egfr = ctx.get("egfr_ml_min_1_73m2", np.nan)
    vitd = ctx.get("vitd_25oh_ng_ml", np.nan)
    b12 = ctx.get("vitb12_pg_ml", np.nan)
    fol = ctx.get("folate_ng_ml", np.nan)

    # Fiber
    if lip >= 60 or glu >= 60:
        sups.append(("Fibra soluble (psyllium o equivalente)", [
            "Útil si LDL/TG/Glucosa están altos o la dieta es baja en fibra.",
            "Prioriza comida (legumbres/avena/verduras). Usa suplemento si no llegas."
        ]))

    # Omega-3 (conditional)
    if (not is_nan(tg) and tg >= 150) or infl >= 60:
        sups.append(("Omega-3 (si no comes pescado azul con regularidad)", [
            "Suele ser razonable cuando TG o inflamación están elevados.",
            "Si tomas anticoagulantes/antiagregantes o tienes cirugía próxima: consulta."
        ]))

    # Magnesium (general support)
    if glu >= 60 or ctx.get("sleep") in ("Malo", "Irregular"):
        sups.append(("Magnesio (soporte general)", [
            "Frecuentemente bajo en dietas modernas; puede apoyar descanso/estrés.",
            "Si hay enfermedad renal, precaución."
        ]))

    # Vitamin D (only if measured low-ish or unknown)
    if not is_nan(vitd) and vitd < 25:
        sups.append(("Vitamina D (solo porque hay analítica baja)", [
            "Como regla de calidad: mejor ajustar si hay medida baja.",
            "Si hay condiciones médicas específicas, individualizar."
        ]))

    # B12/folate cautions
    if (not is_nan(b12) and b12 < 300) or (not is_nan(fol) and fol < 5):
        cautions.append("B12/folato bajos o borderline: priorizar corrección dietética/suplementación prudente y re-chequeo.")

    # Iron caution
    if (not is_nan(ferritin)) and ferritin < 30 and hem >= 60:
        cautions.append("Evitar iniciar hierro a ciegas: confirmar patrón y pautar con profesional.")
    if meds:
        cautions.append("Si hay medicación crónica: revisar interacciones antes de suplementos.")
    if (not is_nan(egfr)) and egfr < 60:
        cautions.append("Con eGFR bajo: precaución con suplementos (magnesio, creatina, etc.).")

    return sups[:3], cautions

def main_actions(scores, derived):
    infl, lip, glu, hem, liv, ren = scores
    tg_hdl = derived.get("tg_hdl_ratio", np.nan)

    actions = [
        "Comida real 80–90% + minimizar ultraprocesados; consistencia > novedad.",
        "Fuerza 2–3x/semana + caminata diaria; si glucosa/TG/HDL altos, caminar 10–20 min postcomida."
    ]

    if glu >= 60 or ((not is_nan(tg_hdl)) and tg_hdl >= 2.5):
        actions.append("Reducir carbohidrato de alta carga (harinas/dulces/bebidas) y priorizar proteína+fibra en cada comida.")
    elif infl >= 60:
        actions.append("Énfasis antiinflamatorio: polifenoles, AOVE, legumbres, pescado; alcohol mínimo.")
    elif lip >= 60:
        actions.append("Fibra soluble diaria + grasas de calidad; alcohol mínimo si TG altos.")
    elif hem >= 60:
        actions.append("Priorizar eje hematológico: hierro/B12/folato según analítica; evitar intervenciones agresivas sin corregirlo.")
    else:
        actions.append("Mantener patrón elegido 8 semanas y medir adherencia; luego repetir analítica de los ejes alterados.")

    return actions

# -----------------------------
# UI helpers: schema-driven input
# -----------------------------
def group_by_level(schema):
    levels = {"core": [], "plus": [], "optional": []}
    for item in schema:
        lvl = item.get("level", "optional")
        if lvl not in levels:
            levels[lvl] = []
        levels[lvl].append(item)
    return levels

def display_unit_label(item, unit_mode):
    unit = item["unit"]
    cg = item.get("convert_group")
    # show mmol/L when converted
    if cg in ("lipids", "triglycerides", "glucose") and unit == "mg/dL" and unit_mode == "mmol/L":
        return "mmol/L"
    return unit

def input_widget(item, unit_mode, key_prefix="inp_"):
    k = item["key"]
    label = item["label"]
    unit = display_unit_label(item, unit_mode)
    cg = item.get("convert_group")

    # Special handling for sex (3 categories)
    if k == "sex":
        choice = st.selectbox(
            f"{label}",
            options=["Mujer", "Hombre", "Otro"],
            index=0
        )
        return {"Mujer": "F", "Hombre": "M", "Otro": "X"}[choice]

    # numeric or text
    # To allow missing: use text_input and parse
    raw = st.text_input(f"{label} ({unit})", value="", key=f"{key_prefix}{k}", placeholder="vacío = desconocido")
    val = parse_float_or_nan(raw)

    # convert to mg/dL internal when needed
    if cg in ("lipids", "triglycerides", "glucose"):
        val = display_to_mgdl(val, cg, unit_mode)

    return val

# -----------------------------
# Sidebar settings/context
# -----------------------------
st.sidebar.header("Unidades")
unit_mode = st.sidebar.radio("Mostrar (solo glucosa/lípidos):", ["mg/dL", "mmol/L"], index=0)

st.sidebar.header("Contexto")
goal = st.sidebar.selectbox("Objetivo", ["Optimización", "Mejorar marcadores", "Energía/Composición corporal"], index=0)
sleep = st.sidebar.selectbox("Sueño", ["Bueno", "Irregular", "Malo"], index=0)
alcohol = st.sidebar.selectbox("Alcohol", ["No", "Ocasional", "Frecuente"], index=1)
meds = st.sidebar.checkbox("Hay medicación crónica (sí/no)", value=False)

st.sidebar.caption("Tip: deja campos vacíos si no los tienes; el motor ajusta su confianza.")

# -----------------------------
# Build tabs & collect inputs
# -----------------------------
levels = group_by_level(SCHEMA_V1)

tab_core, tab_plus, tab_opt = st.tabs(["Core", "Plus", "Optional"])
values = {}

def render_level(tab, items, cols=3):
    with tab:
        cols_list = st.columns(cols)
        for i, item in enumerate(items):
            col = cols_list[i % cols]
            with col:
                values[item["key"]] = input_widget(item, unit_mode)

render_level(tab_core, levels["core"])
render_level(tab_plus, levels["plus"])
render_level(tab_opt, levels["optional"])

# add context into values (not part of schema)
values["goal"] = goal
values["sleep"] = sleep
values["alcohol"] = alcohol
values["meds"] = meds

# -----------------------------
# Derived metrics
# -----------------------------
neut = values.get("neut_abs_x10_3_mm3", np.nan)
lymph = values.get("lymph_abs_x10_3_mm3", np.nan)
nlr = np.nan
if (not is_nan(neut)) and (not is_nan(lymph)) and lymph > 0:
    nlr = neut / lymph

tg = values.get("triglycerides_mg_dl", np.nan)
hdl = values.get("hdl_mg_dl", np.nan)
tg_hdl_ratio = np.nan
if (not is_nan(tg)) and (not is_nan(hdl)) and hdl > 0:
    tg_hdl_ratio = tg / hdl

chol = values.get("chol_total_mg_dl", np.nan)
non_hdl = np.nan
if (not is_nan(chol)) and (not is_nan(hdl)):
    non_hdl = chol - hdl

glu = values.get("glucose_mg_dl", np.nan)
ins = values.get("insulin_uIU_ml", np.nan)
homa_ir = np.nan
if (not is_nan(glu)) and (not is_nan(ins)):
    homa_ir = (glu * ins) / 405.0

derived = {
    "nlr": nlr,
    "tg_hdl_ratio": tg_hdl_ratio,
    "non_hdl_mg_dl": non_hdl,
    "homa_ir": homa_ir
}

# -----------------------------
# Score computation
# -----------------------------
age = values.get("age_years", np.nan)
sex_code = values.get("sex", "X")

infl_score, infl_dr = score_inflammation(
    age=age if not is_nan(age) else 50,
    hscrp=values.get("hscrp_mg_l", np.nan),
    nlr=nlr
)

lip_score, lip_dr, _ = score_lipids(
    ldl_mgdl=values.get("ldl_mg_dl", np.nan),
    hdl_mgdl=values.get("hdl_mg_dl", np.nan),
    tg_mgdl=values.get("triglycerides_mg_dl", np.nan)
)

glu_score, glu_dr, _homa = score_glucose(
    hba1c=values.get("hba1c_pct", np.nan),
    glucose_mgdl=values.get("glucose_mg_dl", np.nan),
    insulin_uIU_ml=values.get("insulin_uIU_ml", np.nan)
)

hem_score, hem_dr = score_hematology(
    sex_code=sex_code,
    hb=values.get("hb_g_dl", np.nan),
    mcv=values.get("mcv_fl", np.nan),
    rdw=values.get("rdw_pct", np.nan),
    ferritin=values.get("ferritin_ng_ml", np.nan),
    vitb12=values.get("vitb12_pg_ml", np.nan),
    folate=values.get("folate_ng_ml", np.nan),
)

liv_score, liv_dr = score_liver(
    ast=values.get("ast_u_l", np.nan),
    alt=values.get("alt_u_l", np.nan),
    ggt=values.get("ggt_u_l", np.nan),
    alp=values.get("alp_u_l", np.nan),
    bili=values.get("bilirubin_total_mg_dl", np.nan)
)

ren_score, ren_dr = score_kidney(
    creatinine=values.get("creatinine_mg_dl", np.nan),
    egfr=values.get("egfr_ml_min_1_73m2", np.nan),
    urate=values.get("uric_acid_mg_dl", np.nan)
)

scores = (infl_score, lip_score, glu_score, hem_score, liv_score, ren_score)
decouple = float(np.std([infl_score, lip_score, glu_score, hem_score]))

# -----------------------------
# Decisions
# -----------------------------
diet, diet_rationale, flags = choose_diet(scores, values, derived)
sups, cautions = choose_supplements(scores, values, derived)
actions = main_actions(scores, derived)

# -----------------------------
# Output
# -----------------------------
st.markdown("---")
st.subheader("Resultados (scores 0 mejor → 100 peor)")

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Inflamación", f"{infl_score:.1f}", bucket(infl_score))
m2.metric("Lípidos", f"{lip_score:.1f}", bucket(lip_score))
m3.metric("Glucosa/insulina", f"{glu_score:.1f}", bucket(glu_score))
m4.metric("Hematología", f"{hem_score:.1f}", bucket(hem_score))
m5.metric("Hígado", f"{liv_score:.1f}", bucket(liv_score))
m6.metric("Riñón", f"{ren_score:.1f}", bucket(ren_score))

st.caption(f"Índice de desacople (desviación entre ejes principales): **{decouple:.1f}** (más alto = ejes menos alineados).")

with st.expander("Derivados calculados", expanded=False):
    st.write(f"- NLR: {nlr:.2f}" if not is_nan(nlr) else "- NLR: —")
    st.write(f"- TG/HDL: {tg_hdl_ratio:.2f}" if not is_nan(tg_hdl_ratio) else "- TG/HDL: —")
    st.write(f"- No-HDL: {non_hdl:.0f} mg/dL" if not is_nan(non_hdl) else "- No-HDL: —")
    st.write(f"- HOMA-IR: {homa_ir:.2f}" if not is_nan(homa_ir) else "- HOMA-IR: —")

with st.expander("Drivers (por qué sale así)", expanded=False):
    st.write("**Inflamación:** " + (", ".join(infl_dr) if infl_dr else "—"))
    st.write("**Lípidos:** " + (", ".join(lip_dr) if lip_dr else "—"))
    st.write("**Glucosa/insulina:** " + (", ".join(glu_dr) if glu_dr else "—"))
    st.write("**Hematología:** " + (", ".join(hem_dr) if hem_dr else "—"))
    st.write("**Hígado:** " + (", ".join(liv_dr) if liv_dr else "—"))
    st.write("**Riñón:** " + (", ".join(ren_dr) if ren_dr else "—"))

st.markdown("---")
st.subheader("Plan v1 (selección adaptativa)")

if flags:
    st.error("⚠️ Señales para revisión profesional:\n- " + "\n- ".join(flags))

st.markdown(f"### Dieta sugerida: **{diet}**")
for r in diet_rationale:
    st.write(f"- {r}")

st.markdown("### Acciones principales (8 semanas)")
for a in actions:
    st.write(f"- {a}")

st.markdown("### Suplementos (mínimos, sin dosis)")
if sups:
    for name, bullets in sups:
        with st.expander(name, expanded=True):
            for b in bullets:
                st.write(f"- {b}")
else:
    st.write("- No se sugiere ningún suplemento específico con los datos actuales; prioriza comida y hábitos.")

if cautions:
    st.warning("Precauciones:\n- " + "\n- ".join(cautions))

st.markdown("---")
st.subheader("Qué repetir y cuándo")
st.write("- Repetir analítica en **8–12 semanas** si hay cambios consistentes.")
st.write("- Repetir ejes alterados: lípidos, HbA1c (si procede), hsCRP, hemograma (Hb/RDW) y función hepato-renal si estaba alterada.")
st.caption("Objetivo v1: mover marcadores en dirección coherente con el dominio limitante, con mínima complejidad y máxima adherencia.")