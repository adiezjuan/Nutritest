from __future__ import annotations

import math
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def _to_num_or_none(x):
    if pd.isna(x):
        return None
    if isinstance(x, str):
        x = x.strip()
        if x == "":
            return None
        if x.lower() == "inf":
            return math.inf
    try:
        return float(x)
    except Exception:
        return x


def _to_bool_si_no(x) -> bool:
    if pd.isna(x):
        return False
    return str(x).strip().lower() in {"si", "sí", "true", "1", "yes"}


def _infer_target_default(vmin, vmax, tipo_umbral):
    if vmin is None and vmax is None:
        return None
    if vmax is None or vmax == math.inf:
        return vmin
    if vmin is None:
        return vmax
    if tipo_umbral == "clinical_cutoff":
        return vmin + (vmax - vmin) * 0.6
    return (vmin + vmax) / 2


def _infer_low_flag(vmin, _tipo_umbral):
    return vmin


def _infer_high_flag(vmax, _tipo_umbral):
    return None if vmax in (None, math.inf) else vmax


def _infer_critical_low(vmin, prioridad):
    if vmin is None:
        return None
    if prioridad == "alta":
        return vmin * 0.85
    if prioridad == "media":
        return vmin * 0.75
    return vmin * 0.65


def _infer_critical_high(vmax, prioridad):
    if vmax in (None, math.inf):
        return None
    if prioridad == "alta":
        return vmax * 1.15
    if prioridad == "media":
        return vmax * 1.25
    return vmax * 1.40


def _infer_direction(row):
    name = str(row["Parametro_backend"]).lower()

    lower_worse_keys = {
        "hdl_mg_dl",
        "egfr_ml_min_1_73m2",
        "hb_g_dl",
        "ferritin_ng_ml",
        "vitb12_pg_ml",
        "folate_ng_ml",
        "lymph_abs_x10_3_mm3",
        "transferrin_sat_pct",
    }
    outside_range_keys = {
        "mcv_fl",
        "wbc_x10_3_mm3",
        "transferrin_mg_dl",
        "tibc_ug_dl",
        "hct_pct",
        "rbc_x10_6_mm3",
    }

    if name in lower_worse_keys:
        return "lower_worse"
    if name in outside_range_keys:
        return "outside_range_worse"

    return "higher_worse"


def load_reference_tables(master_path: Path | None = None, overrides_path: Path | None = None):
    master_path = master_path or (DATA_DIR / "analitos_master.csv")
    overrides_path = overrides_path or (DATA_DIR / "analitos_overrides_biologicos.csv")

    master_df = pd.read_csv(master_path)
    overrides_df = pd.read_csv(overrides_path)

    reference_ranges = {}

    for _, row in master_df.iterrows():
        key = row["Parametro_backend"]

        item = {
            "label": row["Parametro_mostrar"],
            "unit": row["Unidad"],
            "tipo_dato": row["Tipo_dato"],
            "tipo_umbral": row["Tipo_umbral"],
            "base_umbral": row["Base_umbral"],
            "reference_low": _to_num_or_none(row["Valor_min"]),
            "reference_high": _to_num_or_none(row["Valor_max"]),
            "target_default": _infer_target_default(
                _to_num_or_none(row["Valor_min"]),
                _to_num_or_none(row["Valor_max"]),
                row["Tipo_umbral"],
            ),
            "low_flag": _infer_low_flag(_to_num_or_none(row["Valor_min"]), row["Tipo_umbral"]),
            "high_flag": _infer_high_flag(_to_num_or_none(row["Valor_max"]), row["Tipo_umbral"]),
            "critical_low": _infer_critical_low(_to_num_or_none(row["Valor_min"]), row["Prioridad_clinica"]),
            "critical_high": _infer_critical_high(_to_num_or_none(row["Valor_max"]), row["Prioridad_clinica"]),
            "direction": _infer_direction(row),
            "categoria_alto": row.get("Categoria_alto"),
            "categoria_bajo": row.get("Categoria_bajo"),
            "causas_alto": row.get("Causas_alto"),
            "causas_bajo": row.get("Causas_bajo"),
            "prioridad_clinica": row.get("Prioridad_clinica"),
            "dominio_principal": row.get("Dominio_principal"),
            "es_driver": _to_bool_si_no(row.get("Es_driver")),
            "es_guardrail": _to_bool_si_no(row.get("Es_guardrail")),
            "notes": row.get("Nota", ""),
            "usa_sexo_biologico": _to_bool_si_no(row.get("Usa_sexo_biologico")),
            "usa_ayuno": _to_bool_si_no(row.get("Usa_ayuno")),
        }

        reference_ranges[key] = item

    if not overrides_df.empty:
        for key, group in overrides_df.groupby("Parametro_backend"):
            if key not in reference_ranges:
                continue

            sex_specific = {}
            for _, row in group.iterrows():
                sex = str(row["Sexo_biologico"]).strip()
                sex_specific[sex] = {
                    "reference_low": _to_num_or_none(row["Valor_min"]),
                    "reference_high": _to_num_or_none(row["Valor_max"]),
                    "target_default": _infer_target_default(
                        _to_num_or_none(row["Valor_min"]),
                        _to_num_or_none(row["Valor_max"]),
                        reference_ranges[key]["tipo_umbral"],
                    ),
                    "low_flag": _infer_low_flag(
                        _to_num_or_none(row["Valor_min"]),
                        reference_ranges[key]["tipo_umbral"],
                    ),
                    "high_flag": _infer_high_flag(
                        _to_num_or_none(row["Valor_max"]),
                        reference_ranges[key]["tipo_umbral"],
                    ),
                    "critical_low": _infer_critical_low(
                        _to_num_or_none(row["Valor_min"]),
                        reference_ranges[key]["prioridad_clinica"],
                    ),
                    "critical_high": _infer_critical_high(
                        _to_num_or_none(row["Valor_max"]),
                        reference_ranges[key]["prioridad_clinica"],
                    ),
                    "categoria_alto": row.get("Categoria_alto"),
                    "categoria_bajo": row.get("Categoria_bajo"),
                    "notes": row.get("Nota_override", ""),
                }

            reference_ranges[key]["sex_specific"] = sex_specific

    return reference_ranges, master_df, overrides_df
