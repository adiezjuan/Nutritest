import numpy as np
import streamlit as st

from lab_schema_v3 import SCHEMA_V3
from reference_ranges import REFERENCE_RANGES
from scoring_tables import DOMAIN_MASTER
from priority_rules import PRIORITY_RULES
from output_rules import DOMAIN_OUTPUT_RULES, PROFILE_COMBINATIONS


st.set_page_config(page_title="Aging Coach v3", layout="wide")
st.title("Aging Coach v3 — Weighted Domain Engine")
st.caption(
    "⚠️ Prototipo educativo/I+D. No es diagnóstico ni prescripción. "
    "Los umbrales y pesos son semillas ajustables."
)

# -----------------------------
# Unit conversions
# -----------------------------
LIPID_MGDL_TO_MMOLL = 0.02586
TG_MGDL_TO_MMOLL = 0.01129
GLU_MGDL_TO_MMOLL = 0.0555


# -----------------------------
# Generic utils
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
    if is_nan(score):
        return "—"
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

def get_default_input_value(key, current_values=None, default_sex="M"):
    current_values = current_values or {}
    sex = current_values.get("sex", default_sex)

    cfg = REFERENCE_RANGES.get(key)
    if cfg is None:
        return ""

    if "sex_specific" in cfg:
        sex_cfg = cfg["sex_specific"].get(sex, cfg["sex_specific"].get("X", {}))
        val = sex_cfg.get("target_default")
    else:
        val = cfg.get("target_default")

    if val is None:
        return ""
    return str(val)
# -----------------------------
# UI helpers
# -----------------------------
def group_by_level(schema):
    groups = {"essential": [], "precision": [], "advanced": []}
    for item in schema:
        lvl = item.get("level", "advanced")
        groups.setdefault(lvl, []).append(item)
    return groups


def display_unit_label(item, unit_mode):
    unit = item.get("unit", "")
    cg = item.get("convert_group")
    if cg in ("lipids", "triglycerides", "glucose") and unit == "mg/dL" and unit_mode == "mmol/L":
        return "mmol/L"
    return unit


def input_widget(item, unit_mode, current_values=None, key_prefix="inp_"):
    current_values = current_values or {}

    key = item["key"]
    label = item["label"]
    unit = display_unit_label(item, unit_mode)
    input_type = item.get("input_type", "number")
    convert_group = item.get("convert_group")

    if input_type == "select":
        options = item.get("options", [])
        option_labels = item.get("option_labels", {})
        shown = [option_labels.get(opt, opt) for opt in options]

        # Default inicial: Hombre
        default_value = "M" if "M" in options else options[0]
        default_index = options.index(default_value)

        selected = st.selectbox(label, shown, index=default_index, key=f"{key_prefix}{key}")
        reverse = {option_labels.get(opt, opt): opt for opt in options}
        return reverse[selected]

    default_str = get_default_input_value(key, current_values=current_values, default_sex="M")

    # Si la unidad visible está en mmol/L, convertimos también el default
    if default_str != "":
        try:
            default_numeric = float(default_str)
            if convert_group in ("lipids", "triglycerides", "glucose") and unit_mode == "mmol/L":
                default_numeric = mgdl_to_display(default_numeric, convert_group, unit_mode)
                default_str = f"{default_numeric:.2f}"
        except ValueError:
            pass

    raw = st.text_input(
        f"{label} ({unit})",
        value=default_str,
        key=f"{key_prefix}{key}",
        placeholder="vacío = desconocido",
    )
    val = parse_float_or_nan(raw)

    if convert_group in ("lipids", "triglycerides", "glucose"):
        val = display_to_mgdl(val, convert_group, unit_mode)

    return val

# -----------------------------
# Derived metrics
# -----------------------------
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


# -----------------------------
# Reference-based variable scoring
# -----------------------------
def get_reference_config(key, all_values):
    cfg = REFERENCE_RANGES.get(key)
    if cfg is None:
        return None

    sex = all_values.get("sex", "X")
    if "sex_specific" in cfg:
        sex_cfg = cfg["sex_specific"].get(sex, cfg["sex_specific"].get("X", {}))
        merged = {k: v for k, v in cfg.items() if k != "sex_specific"}
        merged.update(sex_cfg)
        return merged
    return cfg


def classify_against_reference(value, ref_cfg):
    if ref_cfg is None or is_nan(value):
        return "missing"

    direction = ref_cfg.get("direction")
    low_flag = ref_cfg.get("low_flag")
    high_flag = ref_cfg.get("high_flag")
    critical_low = ref_cfg.get("critical_low")
    critical_high = ref_cfg.get("critical_high")

    if direction == "higher_worse":
        if critical_high is not None and value >= critical_high:
            return "critical_high"
        if high_flag is not None and value >= high_flag:
            return "high"
        if critical_low is not None and value <= critical_low:
            return "critical_low"
        if low_flag is not None and value < low_flag:
            return "low"
        return "normal"

    if direction == "lower_worse":
        if critical_low is not None and value <= critical_low:
            return "critical_low"
        if low_flag is not None and value < low_flag:
            return "low"
        if critical_high is not None and value >= critical_high:
            return "critical_high"
        if high_flag is not None and value > high_flag:
            return "high"
        return "normal"

    if direction == "outside_range_worse":
        if critical_low is not None and value <= critical_low:
            return "critical_low"
        if critical_high is not None and value >= critical_high:
            return "critical_high"
        if low_flag is not None and value < low_flag:
            return "low"
        if high_flag is not None and value > high_flag:
            return "high"
        return "normal"

    return "normal"


def score_from_reference(value, ref_cfg):
    if ref_cfg is None or is_nan(value):
        return np.nan

    direction = ref_cfg.get("direction")
    target = ref_cfg.get("target_default")
    low_flag = ref_cfg.get("low_flag")
    high_flag = ref_cfg.get("high_flag")
    critical_low = ref_cfg.get("critical_low")
    critical_high = ref_cfg.get("critical_high")
    ref_low = ref_cfg.get("reference_low")
    ref_high = ref_cfg.get("reference_high")

    if direction == "higher_worse":
        if high_flag is None:
            return 0.0
        if target is None:
            target = high_flag
        if value <= target:
            return 0.0
        if critical_high is None:
            critical_high = high_flag * 1.5
        if value >= critical_high:
            return 100.0
        return clamp(100.0 * (value - target) / max(critical_high - target, 1e-9))

    if direction == "lower_worse":
        if low_flag is None:
            return 0.0
        if target is None:
            target = low_flag
        if value >= target:
            return 0.0
        if critical_low is None:
            critical_low = low_flag * 0.7
        if value <= critical_low:
            return 100.0
        return clamp(100.0 * (target - value) / max(target - critical_low, 1e-9))

    if direction == "outside_range_worse":
        if ref_low is None or ref_high is None:
            return np.nan
        if ref_low <= value <= ref_high:
            return 0.0

        if value < ref_low:
            floor = critical_low if critical_low is not None else ref_low - (ref_high - ref_low) * 0.5
            if value <= floor:
                return 100.0
            return clamp(100.0 * (ref_low - value) / max(ref_low - floor, 1e-9))

        ceil = critical_high if critical_high is not None else ref_high + (ref_high - ref_low) * 0.5
        if value >= ceil:
            return 100.0
        return clamp(100.0 * (value - ref_high) / max(ceil - ref_high, 1e-9))

    return np.nan


def score_variable(key, value, all_values):
    if is_nan(value):
        return {
            "score": np.nan,
            "value": value,
            "classification": "missing",
            "reference": None,
            "note": "sin dato",
        }

    ref_cfg = get_reference_config(key, all_values)
    if ref_cfg is None:
        return {
            "score": np.nan,
            "value": value,
            "classification": "missing",
            "reference": None,
            "note": "sin referencia",
        }

    classification = classify_against_reference(value, ref_cfg)
    score = score_from_reference(value, ref_cfg)

    return {
        "score": clamp(score) if not is_nan(score) else np.nan,
        "value": value,
        "classification": classification,
        "reference": ref_cfg,
        "note": ref_cfg.get("notes", ""),
    }


def score_all_variables(all_values):
    scores = {}
    for key in REFERENCE_RANGES.keys():
        value = all_values.get(key, np.nan)
        scores[key] = score_variable(key, value, all_values)
    return scores


# -----------------------------
# Domain scoring
# -----------------------------
def score_domain(domain_key, all_values, variable_scores):
    config = DOMAIN_MASTER[domain_key]
    active_vars = [v for v in config["variables"] if v.get("weight", 0) > 0]

    weighted_sum = 0.0
    total_weight_used = 0.0
    used_items = []

    for var in active_vars:
        key = var["key"]
        weight = float(var["weight"])
        score_info = variable_scores.get(key, {"score": np.nan})
        score = score_info["score"]

        if not is_nan(score):
            weighted_sum += score * weight
            total_weight_used += weight
            used_items.append({
                "key": key,
                "score": score,
                "weight": weight,
                "role": var.get("role", ""),
                "value": all_values.get(key, np.nan),
                "classification": score_info.get("classification", "missing"),
            })

    total_possible = sum(v["weight"] for v in active_vars)

    if total_weight_used == 0:
        domain_score = np.nan
        coverage = 0.0
    else:
        domain_score = weighted_sum / total_weight_used
        coverage = total_weight_used / total_possible if total_possible > 0 else 0.0

    return {
        "key": domain_key,
        "label": config["label"],
        "definition": config["definition"],
        "priority_override": config.get("priority_override", False),
        "score": clamp(domain_score) if not is_nan(domain_score) else np.nan,
        "coverage": coverage,
        "used": used_items,
    }


def score_domains(all_values, variable_scores):
    return {
        domain_key: score_domain(domain_key, all_values, variable_scores)
        for domain_key in DOMAIN_MASTER.keys()
    }


# -----------------------------
# Rule evaluation
# -----------------------------
def evaluate_simple_condition(cond, all_values):
    key = cond["key"]
    value = all_values.get(key, np.nan)
    if is_nan(value):
        return False

    op = cond["op"]
    target = cond["value"]

    if op == "<":
        return value < target
    if op == "<=":
        return value <= target
    if op == ">":
        return value > target
    if op == ">=":
        return value >= target
    if op == "==":
        return value == target
    return False


def evaluate_conditions(conditions, all_values):
    if not conditions:
        return False

    results = []
    for cond in conditions:
        if "any" in cond:
            any_result = any(evaluate_simple_condition(c, all_values) for c in cond["any"])
            results.append(any_result)
        else:
            results.append(evaluate_simple_condition(cond, all_values))
    return all(results)


def apply_priority_rules(domain_scores, all_values):
    applied = []

    for rule in PRIORITY_RULES:
        if evaluate_conditions(rule.get("conditions", []), all_values):
            applied.append(rule)

    applied_sorted = sorted(
        applied,
        key=lambda r: (r.get("type") == "override", r.get("priority", 0), r.get("boost", 0)),
        reverse=True
    )

    adjusted = {k: dict(v) for k, v in domain_scores.items()}
    reasons = []

    # primero boosts
    for rule in applied_sorted:
        if rule.get("type") == "boost":
            domain = rule["domain"]
            if domain in adjusted and not is_nan(adjusted[domain]["score"]):
                adjusted[domain]["score"] = clamp(adjusted[domain]["score"] + rule.get("boost", 0))
                reasons.append(rule["reason"])

    # luego override más fuerte
    override_rules = [r for r in applied_sorted if r.get("type") == "override"]
    forced_domain = None
    forced_reason = None
    if override_rules:
        strongest = max(override_rules, key=lambda r: r.get("priority", 0))
        forced_domain = strongest["domain"]
        forced_reason = strongest["reason"]

    return adjusted, forced_domain, forced_reason, reasons


def rank_domains(domain_scores, all_values):
    adjusted_scores, forced_domain, forced_reason, boost_reasons = apply_priority_rules(domain_scores, all_values)

    valid = [d for d in adjusted_scores.values() if not is_nan(d["score"])]
    ranked = sorted(valid, key=lambda x: x["score"], reverse=True)

    if forced_domain is not None:
        forced = adjusted_scores.get(forced_domain)
        if forced is not None:
            rest = [d for d in ranked if d["key"] != forced_domain]
            ranked = [forced] + rest

    return ranked, forced_domain, forced_reason, boost_reasons


# -----------------------------
# Flags / confidence
# -----------------------------
def build_flags(all_values):
    flags = []

    for key, cfg in REFERENCE_RANGES.items():
        value = all_values.get(key, np.nan)
        if is_nan(value):
            continue

        ref = get_reference_config(key, all_values)
        classification = classify_against_reference(value, ref)
        label = ref.get("label", key)

        if classification == "critical_low":
            flags.append(f"{label}: valor críticamente bajo.")
        elif classification == "critical_high":
            flags.append(f"{label}: valor críticamente alto.")

    return flags


def confidence_level(domain_scores):
    coverages = [d["coverage"] for d in domain_scores.values() if not is_nan(d["score"])]
    if not coverages:
        return "Baja", 0.0
    mean_cov = float(np.mean(coverages))
    if mean_cov >= 0.80:
        return "Alta", mean_cov
    if mean_cov >= 0.50:
        return "Media", mean_cov
    return "Baja", mean_cov


# -----------------------------
# Output building
# -----------------------------
def choose_profile_combination(primary_key, secondary_key):
    for combo in PROFILE_COMBINATIONS:
        if combo["primary"] == primary_key and combo["secondary"] == secondary_key:
            return combo
    return None


def build_priority_now(ranked_domains, all_values):
    if not ranked_domains:
        return {
            "primary": None,
            "secondary": None,
            "profile": "Sin datos suficientes.",
            "main_lever": "Completar inputs esenciales.",
            "pattern": "Sin patrón sugerido.",
            "repeat": "Añadir glucosa, HbA1c, lípidos, Hb/ferritina y creatinina.",
            "actions": [],
            "combination_label": None,
            "extra_action": None,
        }

    primary = ranked_domains[0]
    secondary = ranked_domains[1] if len(ranked_domains) > 1 else None

    output_cfg = DOMAIN_OUTPUT_RULES.get(primary["key"], {})
    profile = output_cfg.get("profile", "Perfil mixto.")
    main_lever = output_cfg.get("main_lever", "Intervenir sobre el eje dominante.")
    pattern = output_cfg.get("pattern", "Mediterránea base")
    repeat = output_cfg.get("repeat", "Repetir ejes alterados en 8–12 semanas.")
    actions = output_cfg.get("actions", [])

    combination_label = None
    extra_action = None
    if secondary is not None:
        combo = choose_profile_combination(primary["key"], secondary["key"])
        if combo:
            combination_label = combo.get("label")
            extra_action = combo.get("extra_action")

    return {
        "primary": primary,
        "secondary": secondary,
        "profile": profile,
        "main_lever": main_lever,
        "pattern": pattern,
        "repeat": repeat,
        "actions": actions,
        "combination_label": combination_label,
        "extra_action": extra_action,
    }


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Unidades")
unit_mode = st.sidebar.radio("Mostrar glucosa/lípidos en:", ["mg/dL", "mmol/L"], index=0)

st.sidebar.header("Contexto")
alcohol = st.sidebar.selectbox("Alcohol", ["No", "Ocasional", "Frecuente"], index=1)
sleep = st.sidebar.selectbox("Sueño", ["Bueno", "Irregular", "Malo"], index=0)
meds = st.sidebar.checkbox("Medicación crónica", value=False)
st.sidebar.caption("Cualquier cambio en inputs o umbrales recalcula automáticamente el output.")

# -----------------------------
# Input rendering
# -----------------------------
levels = group_by_level(SCHEMA_V3)
tab_essential, tab_precision, tab_advanced = st.tabs(["Essential", "Precision", "Advanced"])

values = {}


def render_level(tab, items, cols=3):
    with tab:
        cols_list = st.columns(cols)
        for idx, item in enumerate(items):
            with cols_list[idx % cols]:
                values[item["key"]] = input_widget(item, unit_mode)


render_level(tab_essential, levels["essential"])
render_level(tab_precision, levels["precision"])
render_level(tab_advanced, levels["advanced"])

values["alcohol"] = alcohol
values["sleep"] = sleep
values["meds"] = meds

# -----------------------------
# Engine execution
# -----------------------------
derived = compute_derived(values)
all_values = merge_values(values, derived)
variable_scores = score_all_variables(all_values)
domain_scores = score_domains(all_values, variable_scores)
ranked_domains, forced_domain, forced_reason, boost_reasons = rank_domains(domain_scores, all_values)
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
        if priority_now["combination_label"]:
            st.write(priority_now["combination_label"])
        else:
            st.write(priority_now["profile"])

        st.markdown(f"**Palanca principal:** {priority_now['main_lever']}")
        st.markdown(f"**Patrón sugerido:** {priority_now['pattern']}")
        st.markdown(f"**Confianza del análisis:** {conf_label}")
        st.caption(f"Cobertura media del motor: {int(conf_value * 100)}%")
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

if boost_reasons:
    st.info("Ajustes de prioridad aplicados:\n- " + "\n- ".join(boost_reasons))

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
    st.markdown(f"**4. Palanca principal:** {priority_now['main_lever']}")
    if priority_now["extra_action"]:
        st.markdown(f"**5. Ajuste por combinación:** {priority_now['extra_action']}")
        st.markdown(f"**6. Qué repetir:** {priority_now['repeat']}")
    else:
        st.markdown(f"**5. Qué repetir:** {priority_now['repeat']}")

st.markdown("### Acciones sugeridas")
if priority_now["actions"]:
    for action in priority_now["actions"]:
        st.write(f"- {action}")
else:
    st.write("- Sin acciones específicas por falta de datos.")

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
        st.write(f"**{d['label']}** → {d['score']:.1f} | cobertura {int(d['coverage'] * 100)}%")

with st.expander("Variables usadas por dominio", expanded=False):
    for d in ranked_domains:
        st.markdown(f"### {d['label']}")
        if not d["used"]:
            st.write("- Sin datos suficientes")
            continue
        for item in sorted(d["used"], key=lambda x: x["weight"], reverse=True):
            val = item["value"]
            val_txt = "—" if is_nan(val) else f"{val}"
            st.write(
                f"- {item['key']}: valor={val_txt}, "
                f"score={item['score']:.1f}, "
                f"peso={item['weight']}, "
                f"rol={item['role']}, "
                f"clasificación={item['classification']}"
            )

with st.expander("Tabla de ponderación actual", expanded=False):
    st.json(DOMAIN_MASTER)

st.markdown("---")
st.subheader("Tabla de referencia por defecto")

with st.expander("Ver rangos, objetivos y umbrales", expanded=False):
    for key, cfg in REFERENCE_RANGES.items():
        st.markdown(f"### {cfg.get('label', key)}")
        if "sex_specific" in cfg:
            for sex_code, sex_cfg in cfg["sex_specific"].items():
                st.write(
                    f"- {sex_code}: "
                    f"ref_low={sex_cfg.get('reference_low')}, "
                    f"ref_high={sex_cfg.get('reference_high')}, "
                    f"target={sex_cfg.get('target_default')}, "
                    f"low_flag={sex_cfg.get('low_flag')}, "
                    f"high_flag={sex_cfg.get('high_flag')}, "
                    f"critical_low={sex_cfg.get('critical_low')}, "
                    f"critical_high={sex_cfg.get('critical_high')}"
                )
        else:
            st.write(
                f"- unidad={cfg.get('unit')}, "
                f"dirección={cfg.get('direction')}, "
                f"ref_low={cfg.get('reference_low')}, "
                f"ref_high={cfg.get('reference_high')}, "
                f"target={cfg.get('target_default')}, "
                f"low_flag={cfg.get('low_flag')}, "
                f"high_flag={cfg.get('high_flag')}, "
                f"critical_low={cfg.get('critical_low')}, "
                f"critical_high={cfg.get('critical_high')}"
            )
