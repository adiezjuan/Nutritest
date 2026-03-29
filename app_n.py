import numpy as np
import streamlit as st

from lab_schema_v3 import SCHEMA_V3, DOMAIN_MASTER, VARIABLE_RULES

st.set_page_config(page_title="Aging Coach v3", layout="wide")
st.title("Aging Coach v3 — Weighted Domain Engine")
st.caption("⚠️ Prototipo educativo/I+D. No es diagnóstico ni prescripción.")

LIPID_MGDL_TO_MMOLL = 0.02586
TG_MGDL_TO_MMOLL = 0.01129
GLU_MGDL_TO_MMOLL = 0.0555


# -----------------------------
# Utils
# -----------------------------
def clamp(x, low=0.0, high=100.0):
    return float(np.clip(x, low, high))


def is_nan(x):
    return x is None or (isinstance(x, float) and np.isnan(x))


def parse_float_or_nan(raw: str) -> float:
    raw = (raw or "").strip().replace(",", ".")
    if raw == "":
        return np.nan
    try:
        return float(raw)
    except ValueError:
        return np.nan


def bucket(score: float) -> str:
    if score < 30:
        return "Bajo"
    if score < 60:
        return "Moderado"
    return "Alto"


def mgdl_to_display(x_mgdl: float, convert_group: str, unit_mode: str) -> float:
    if is_nan(x_mgdl):
        return x_mgdl
    if unit_mode == "mg/dL":
        return x_mgdl
    if convert_group == "lipids":
        return x_mgdl * LIPID_MGDL_TO_MMOLL
    if convert_group == "triglycerides":
        return x_mgdl * TG_MGDL_TO_MMOLL
    if convert_group == "glucose":
        return x_mgdl * GLU_MGDL_TO_MMOLL
    return x_mgdl


def display_to_mgdl(x_display: float, convert_group: str, unit_mode: str) -> float:
    if is_nan(x_display):
        return x_display
    if unit_mode == "mg/dL":
        return x_display
    if convert_group == "lipids":
        return x_display / LIPID_MGDL_TO_MMOLL
    if convert_group == "triglycerides":
        return x_display / TG_MGDL_TO_MMOLL
    if convert_group == "glucose":
        return x_display / GLU_MGDL_TO_MMOLL
    return x_display


# -----------------------------
# Rule engine
# -----------------------------
def interpolate_piecewise_higher(x, points):
    if is_nan(x):
        return np.nan
    points = sorted(points, key=lambda t: t[0])
    if x <= points[0][0]:
        return float(points[0][1])
    if x >= points[-1][0]:
        return float(points[-1][1])
    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        if x0 <= x <= x1:
            if x1 == x0:
                return float(y1)
            alpha = (x - x0) / (x1 - x0)
            return float(y0 + alpha * (y1 - y0))
    return np.nan


def interpolate_piecewise_lower(x, points):
    if is_nan(x):
        return np.nan
    points = sorted(points, key=lambda t: t[0], reverse=True)
    if x >= points[0][0]:
        return float(points[0][1])
    if x <= points[-1][0]:
        return float(points[-1][1])
    for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
        if x1 <= x <= x0:
            if x0 == x1:
                return float(y1)
            alpha = (x0 - x) / (x0 - x1)
            return float(y0 + alpha * (y1 - y0))
    return np.nan


def score_piecewise_range(x, optimal_low, optimal_high, outer_low, outer_high,
                          inner_score=20, outer_score=80, extreme_score=100):
    if is_nan(x):
        return np.nan
    if optimal_low <= x <= optimal_high:
        return 0.0
    if outer_low <= x < optimal_low:
        alpha = (optimal_low - x) / (optimal_low - outer_low)
        return float(alpha * outer_score)
    if optimal_high < x <= outer_high:
        alpha = (x - optimal_high) / (outer_high - optimal_high)
        return float(alpha * outer_score)
    return float(extreme_score)


def score_variable(key, value, values):
    if is_nan(value):
        return {"score": np.nan, "value": value, "note": "sin dato"}

    if key == "hb_g_dl":
        sex = values.get("sex", "X")
        if sex == "M":
            rule = VARIABLE_RULES["hb_g_dl_male"]
        elif sex == "F":
            rule = VARIABLE_RULES["hb_g_dl_female"]
        else:
            rule = VARIABLE_RULES["hb_g_dl_other"]
    else:
        rule = VARIABLE_RULES.get(key)

    if not rule:
        return {"score": np.nan, "value": value, "note": "sin regla"}

    mode = rule["mode"]

    if mode == "piecewise_higher":
        score = interpolate_piecewise_higher(value, rule["points"])
    elif mode == "piecewise_lower":
        score = interpolate_piecewise_lower(value, rule["points"])
    elif mode == "piecewise_range":
        score = score_piecewise_range(
            value,
            rule["optimal_low"], rule["optimal_high"],
            rule["outer_low"], rule["outer_high"],
            rule.get("inner_score", 20),
            rule.get("outer_score", 80),
            rule.get("extreme_score", 100),
        )
    else:
        score = np.nan

    return {"score": clamp(score) if not is_nan(score) else np.nan, "value": value, "note": mode}


def compute_derived(values):
    tg = values.get("triglycerides_mg_dl", np.nan)
    hdl = values.get("hdl_mg_dl", np.nan)
    chol = values.get("chol_total_mg_dl", np.nan)
    glu = values.get("glucose_mg_dl", np.nan)
    ins = values.get("insulin_uIU_ml", np.nan)
    neut = values.get("neut_abs_x10_3_mm3", np.nan)
    lymph = values.get("lymph_abs_x10_3_mm3", np.nan)

    tg_hdl_ratio = np.nan
    if not is_nan(tg) and not is_nan(hdl) and hdl > 0:
        tg_hdl_ratio = tg / hdl

    non_hdl = np.nan
    if not is_nan(chol) and not is_nan(hdl):
        non_hdl = chol - hdl

    homa_ir = np.nan
    if not is_nan(glu) and not is_nan(ins):
        homa_ir = (glu * ins) / 405.0

    nlr = np.nan
    if not is_nan(neut) and not is_nan(lymph) and lymph > 0:
        nlr = neut / lymph

    return {
        "tg_hdl_ratio": tg_hdl_ratio,
        "non_hdl_mg_dl": non_hdl,
        "homa_ir": homa_ir,
        "nlr": nlr,
    }


def merge_values(values, derived):
    merged = dict(values)
    merged.update(derived)
    return merged


def score_all_variables(all_values):
    scores = {}
    for key in VARIABLE_RULES.keys():
        if key.startswith("hb_g_dl_"):
            continue
        val = all_values.get(key, np.nan)
        scores[key] = score_variable(key, val, all_values)
    return scores


def score_domain(domain_key, all_values, variable_scores):
    config = DOMAIN_MASTER[domain_key]
    weighted_sum = 0.0
    total_weight = 0.0
    used = []

    for var in config["variables"]:
        key = var["key"]
        weight = var["weight"]
        if weight <= 0:
            continue

        score_info = variable_scores.get(key, {"score": np.nan})
        score = score_info["score"]

        if not is_nan(score):
            weighted_sum += score * weight
            total_weight += weight
            used.append({
                "key": key,
                "score": score,
                "weight": weight,
                "role": var["role"],
                "value": all_values.get(key, np.nan)
            })

    if total_weight == 0:
        domain_score = np.nan
        coverage = 0.0
    else:
        domain_score = weighted_sum / total_weight
        coverage = total_weight / sum(v["weight"] for v in config["variables"] if v["weight"] > 0)

    return {
        "key": domain_key,
        "label": config["label"],
        "definition": config["definition"],
        "score": clamp(domain_score) if not is_nan(domain_score) else np.nan,
        "coverage": coverage,
        "used": used,
        "priority_override": config.get("priority_override", False),
    }


def score_domains(all_values, variable_scores):
    out = {}
    for domain_key in DOMAIN_MASTER.keys():
        out[domain_key] = score_domain(domain_key, all_values, variable_scores)
    return out


# -----------------------------
# Priority logic
# -----------------------------
def build_flags(all_values):
    flags = []

    hba1c = all_values.get("hba1c_pct", np.nan)
    hscrp = all_values.get("hscrp_mg_l", np.nan)
    egfr = all_values.get("egfr_ml_min_1_73m2", np.nan)
    hb = all_values.get("hb_g_dl", np.nan)
    ferritin = all_values.get("ferritin_ng_ml", np.nan)

    if not is_nan(hba1c) and hba1c >= 6.5:
        flags.append("HbA1c ≥ 6.5%: compatible con diabetes; requiere valoración médica.")
    if not is_nan(hscrp) and hscrp >= 10:
        flags.append("hsCRP ≥ 10 mg/L: posible inflamación aguda/infección; revisar antes de cambios agresivos.")
    if not is_nan(egfr) and egfr < 60:
        flags.append("eGFR < 60: prudencia con proteína alta y suplementos.")
    if not is_nan(hb) and hb < 10.5:
        flags.append("Hemoglobina muy baja: prioridad de revisión médica.")
    if not is_nan(ferritin) and ferritin < 15:
        flags.append("Ferritina muy baja: probable ferropenia; evitar improvisar.")

    return flags


def override_priority(domain_scores, all_values):
    # reglas forzadas iniciales
    hb = all_values.get("hb_g_dl", np.nan)
    ferritin = all_values.get("ferritin_ng_ml", np.nan)
    rdw = all_values.get("rdw_pct", np.nan)
    hba1c = all_values.get("hba1c_pct", np.nan)
    glucose = all_values.get("glucose_mg_dl", np.nan)
    egfr = all_values.get("egfr_ml_min_1_73m2", np.nan)
    hscrp = all_values.get("hscrp_mg_l", np.nan)
    ggt = all_values.get("ggt_u_l", np.nan)
    alt = all_values.get("alt_u_l", np.nan)

    # hematología fuerza prioridad
    if (not is_nan(hb) and hb < 11.5) or ((not is_nan(ferritin) and ferritin < 15) and (not is_nan(rdw) and rdw > 14.5)):
        return "hematology", "El eje hematológico fuerza prioridad por impacto funcional y seguridad."

    # riñón fuerza prioridad
    if not is_nan(egfr) and egfr < 60:
        return "kidney", "El eje renal fuerza prioridad por seguridad."

    # inflamación fuerza revisión
    if not is_nan(hscrp) and hscrp >= 10:
        return "inflammation", "La señal inflamatoria fuerza prioridad por prudencia clínica."

    # glucosa fuerza si claramente alta
    if (not is_nan(hba1c) and hba1c >= 6.5) or (not is_nan(glucose) and glucose >= 126):
        return "glucose", "El eje glucémico fuerza prioridad por magnitud de alteración."

    # hígado como patrón combinado
    if (not is_nan(ggt) and ggt >= 80) and (not is_nan(alt) and alt >= 60):
        return "liver", "El patrón hepato-metabólico combinado sube de prioridad."

    return None, None


def rank_domains(domain_scores, all_values):
    forced_key, forced_reason = override_priority(domain_scores, all_values)

    valid = [v for v in domain_scores.values() if not is_nan(v["score"])]
    valid_sorted = sorted(valid, key=lambda x: x["score"], reverse=True)

    if forced_key:
        forced = domain_scores[forced_key]
        rest = [d for d in valid_sorted if d["key"] != forced_key]
        ranked = [forced] + rest
    else:
        ranked = valid_sorted

    return ranked, forced_reason


def choose_pattern(primary_key, all_values):
    tg_hdl = all_values.get("tg_hdl_ratio", np.nan)
    hba1c = all_values.get("hba1c_pct", np.nan)
    hscrp = all_values.get("hscrp_mg_l", np.nan)

    if primary_key == "hematology":
        return "Conservadora + corregir eje hematológico primero"
    if primary_key == "glucose":
        if (not is_nan(hba1c) and hba1c >= 6.0) or (not is_nan(tg_hdl) and tg_hdl >= 2.5):
            return "Low-carb flexible"
        return "Mediterránea con control glucémico"
    if primary_key == "lipids":
        return "Mediterránea alta en fibra y calidad grasa"
    if primary_key == "inflammation":
        return "Mediterránea antiinflamatoria"
    if primary_key == "liver":
        return "Mediterránea baja en alcohol y carga glucémica"
    if primary_key == "kidney":
        return "Conservadora y prudente con suplementos/proteína"
    return "Mediterránea base"


def build_priority_now(ranked_domains, all_values):
    if not ranked_domains:
        return {
            "primary": None,
            "secondary": None,
            "profile": "Sin datos suficientes.",
            "lever": "Completar inputs esenciales.",
            "repeat": "Añadir glucosa, HbA1c, lípidos, Hb/ferritina, creatinina.",
        }

    primary = ranked_domains[0]
    secondary = ranked_domains[1] if len(ranked_domains) > 1 else None

    if primary["key"] == "glucose":
        profile = "Perfil predominantemente metabólico/glucémico."
        lever = "Reducir carga glucémica, priorizar proteína + fibra y mejorar sensibilidad a la insulina."
        repeat = "Repetir glucosa, HbA1c, TG/HDL y, si se puede, insulina en 8–12 semanas."
    elif primary["key"] == "lipids":
        profile = "Perfil predominantemente lipídico-aterogénico."
        lever = "Fibra soluble, calidad grasa, control de alcohol y cintura."
        repeat = "Repetir LDL, TG, HDL y no-HDL en 8–12 semanas."
    elif primary["key"] == "inflammation":
        profile = "Perfil predominantemente inflamatorio."
        lever = "Reducir carga fisiológica total: alcohol mínimo, comida simple, sueño y control del contexto."
        repeat = "Repetir hsCRP y hemograma diferencial en 4–8 semanas si persiste."
    elif primary["key"] == "hematology":
        profile = "Perfil con prioridad hematológica."
        lever = "Corregir primero reservas/eritropoyesis antes de intervenciones dietéticas intensas."
        repeat = "Repetir Hb, RDW, MCV, ferritina y ampliar hierro/B12/folato si procede."
    elif primary["key"] == "liver":
        profile = "Perfil hepato-metabólico."
        lever = "Alcohol mínimo, menos ultraprocesado, mejor control glucémico y reducción de cintura."
        repeat = "Repetir ALT, AST, GGT y TG en 8–12 semanas."
    elif primary["key"] == "kidney":
        profile = "Perfil con prioridad renal/seguridad."
        lever = "Prudencia con suplementos y estrategias extremas; individualizar."
        repeat = "Repetir creatinina, eGFR y ácido úrico según evolución."
    else:
        profile = "Perfil mixto."
        lever = "Intervenir sobre el eje dominante sin perder de vista el secundario."
        repeat = "Repetir ejes alterados en 8–12 semanas."

    return {
        "primary": primary,
        "secondary": secondary,
        "profile": profile,
        "lever": lever,
        "repeat": repeat,
    }


def confidence_level(domain_scores):
    weighted_coverages = []
    for d in domain_scores.values():
        if not is_nan(d["score"]):
            weighted_coverages.append(d["coverage"])
    if not weighted_coverages:
        return "Baja", 0.0
    cov = float(np.mean(weighted_coverages))
    if cov >= 0.8:
        return "Alta", cov
    if cov >= 0.5:
        return "Media", cov
    return "Baja", cov


# -----------------------------
# UI helpers
# -----------------------------
def group_by_level(schema):
    groups = {"essential": [], "precision": [], "advanced": []}
    for item in schema:
        groups[item["level"]].append(item)
    return groups


def display_unit_label(item, unit_mode):
    unit = item["unit"]
    cg = item.get("convert_group")
    if cg in ("lipids", "triglycerides", "glucose") and unit == "mg/dL" and unit_mode == "mmol/L":
        return "mmol/L"
    return unit


def input_widget(item, unit_mode, key_prefix="inp_"):
    k = item["key"]
    label = item["label"]
    unit = display_unit_label(item, unit_mode)
    cg = item.get("convert_group")

    if item.get("input_type") == "select":
        options = item["options"]
        labels = item.get("option_labels", {})
        idx = 0
        shown = [labels.get(o, o) for o in options]
        selected_label = st.selectbox(label, options=shown, index=idx, key=f"{key_prefix}{k}")
        reverse = {labels.get(o, o): o for o in options}
        return reverse[selected_label]

    raw = st.text_input(f"{label} ({unit})", value="", key=f"{key_prefix}{k}", placeholder="vacío = desconocido")
    val = parse_float_or_nan(raw)

    if cg in ("lipids", "triglycerides", "glucose"):
        val = display_to_mgdl(val, cg, unit_mode)

    return val


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Unidades")
unit_mode = st.sidebar.radio("Mostrar glucosa/lípidos en:", ["mg/dL", "mmol/L"], index=0)

st.sidebar.header("Contexto")
alcohol = st.sidebar.selectbox("Alcohol", ["No", "Ocasional", "Frecuente"], index=1)
sleep = st.sidebar.selectbox("Sueño", ["Bueno", "Irregular", "Malo"], index=0)
meds = st.sidebar.checkbox("Medicación crónica", value=False)

# -----------------------------
# Inputs
# -----------------------------
levels = group_by_level(SCHEMA_V3)
tab1, tab2, tab3 = st.tabs(["Essential", "Precision", "Advanced"])
values = {}


def render_level(tab, items, cols=3):
    with tab:
        cols_list = st.columns(cols)
        for i, item in enumerate(items):
            with cols_list[i % cols]:
                values[item["key"]] = input_widget(item, unit_mode)


render_level(tab1, levels["essential"])
render_level(tab2, levels["precision"])
render_level(tab3, levels["advanced"])

values["alcohol"] = alcohol
values["sleep"] = sleep
values["meds"] = meds

# -----------------------------
# Engine
# -----------------------------
derived = compute_derived(values)
all_values = merge_values(values, derived)
variable_scores = score_all_variables(all_values)
domain_scores = score_domains(all_values, variable_scores)
ranked_domains, forced_reason = rank_domains(domain_scores, all_values)
priority_now = build_priority_now(ranked_domains, all_values)
flags = build_flags(all_values)
conf_label, conf_value = confidence_level(domain_scores)

# -----------------------------
# Output
# -----------------------------
st.markdown("---")
st.subheader("Resumen ejecutivo")

left, right = st.columns([1.7, 1.0])

with left:
    if priority_now["primary"] is not None:
        st.markdown(f"### Prioridad principal: **{priority_now['primary']['label']}**")
        st.write(priority_now["profile"])
        st.markdown(f"**Palanca principal:** {priority_now['lever']}")
        st.markdown(f"**Patrón sugerido:** {choose_pattern(priority_now['primary']['key'], all_values)}")
        st.markdown(f"**Confianza del análisis:** {conf_label}")
    else:
        st.write("Faltan datos esenciales para generar una prioridad útil.")

with right:
    if priority_now["secondary"] is not None:
        st.info(
            f"**Secundario:** {priority_now['secondary']['label']}\n\n"
            f"**Score primario:** {priority_now['primary']['score']:.1f}\n\n"
            f"**Score secundario:** {priority_now['secondary']['score']:.1f}"
        )

if forced_reason:
    st.warning(forced_reason)

if flags:
    st.error("⚠️ Señales para revisión profesional:\n- " + "\n- ".join(flags))

st.markdown("---")
st.subheader("Ranking de dominios")

if ranked_domains:
    cols = st.columns(min(6, len(ranked_domains)))
    for col, domain in zip(cols, ranked_domains[:6]):
        with col:
            st.metric(domain["label"], f"{domain['score']:.1f}", bucket(domain["score"]))
            st.caption(f"Cobertura: {int(domain['coverage'] * 100)}%")

st.markdown("---")
st.subheader("Tu prioridad ahora")

if priority_now["primary"] is not None:
    st.markdown(f"**1. Dominio principal:** {priority_now['primary']['label']}")
    if priority_now["secondary"] is not None:
        st.markdown(f"**2. Dominio secundario:** {priority_now['secondary']['label']}")
    st.markdown(f"**3. Tipo de perfil:** {priority_now['profile']}")
    st.markdown(f"**4. Palanca principal:** {priority_now['lever']}")
    st.markdown(f"**5. Qué repetir:** {priority_now['repeat']}")

st.markdown("---")
st.subheader("Derivados")

with st.expander("Ver derivados", expanded=False):
    st.write(f"- TG/HDL: {derived['tg_hdl_ratio']:.2f}" if not is_nan(derived["tg_hdl_ratio"]) else "- TG/HDL: —")
    st.write(f"- No-HDL: {derived['non_hdl_mg_dl']:.0f} mg/dL" if not is_nan(derived["non_hdl_mg_dl"]) else "- No-HDL: —")
    st.write(f"- HOMA-IR: {derived['homa_ir']:.2f}" if not is_nan(derived["homa_ir"]) else "- HOMA-IR: —")
    st.write(f"- NLR: {derived['nlr']:.2f}" if not is_nan(derived["nlr"]) else "- NLR: —")

st.markdown("---")
st.subheader("Transparencia del motor")

with st.expander("Scores por dominio", expanded=False):
    for d in ranked_domains:
        st.write(f"**{d['label']}** → {d['score']:.1f} | cobertura {int(d['coverage']*100)}%")

with st.expander("Variables usadas por dominio", expanded=False):
    for d in ranked_domains:
        st.markdown(f"### {d['label']}")
        if not d["used"]:
            st.write("- Sin datos suficientes")
            continue
        for item in sorted(d["used"], key=lambda x: x["weight"], reverse=True):
            val = item["value"]
            val_txt = "—" if is_nan(val) else f"{val}"
            st.write(f"- {item['key']}: valor={val_txt}, score={item['score']:.1f}, peso={item['weight']}, rol={item['role']}")

with st.expander("Tabla de ponderación actual", expanded=False):
    st.json(DOMAIN_MASTER)
