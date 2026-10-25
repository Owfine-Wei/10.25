"""4月冲击：同一模型分别求解有/无4月关税，保留3月措施。"""
from copy import deepcopy
from itertools import product

import numpy as np
import pandas as pd

from stage_1.calibration import calibrate
from stage_2.equilibrium import solve


def configured_base(root, config, profile, regime, capacity=None):
    local = deepcopy(config)
    local["model"]["base_tariff"] = deepcopy(config["april_2025"]["mfn_proxy"])
    local["model"]["base_tariff"]["USA"] += regime["legacy_us_tariff"]
    local["model"]["supply_elasticity"] = profile["supply"]
    if capacity is not None:
        local["model"]["capacity_multiplier"] = {c: capacity for c in config["countries"]}
    _, base = calibrate(root / config["clean_csv"], local)
    return base, local


def paired_stage(base, config, profile, stage, sigma=None, eta=None, scale=1):
    """两次求解使用同一基期、同一组参数，差异仅为4月新增税率。"""
    sigma = profile["sigma"] if sigma is None else sigma
    eta = profile["eta"] if eta is None else eta
    march = config["april_2025"]["march_addition"]
    counter = {"id": "no_april", "label": "无4月加税", "tariff_addition": {"USA": march}}
    shock = {"id": stage["id"], "label": stage["label"],
             "tariff_addition": {"USA": march + stage["april_addition"]}}
    reference, d0 = solve(base, config, counter, sigma, eta, scale)
    result, d1 = solve(base, config, shock, sigma, eta, scale)
    for column, prefix in [("quantity_tonnes", "quantity"), ("fob_usd_per_tonne", "price"), ("value_usd", "value")]:
        result["counterfactual_" + column] = reference[column].to_numpy()
        result["april_" + prefix + "_change_pct"] = (result[column] / reference[column] - 1) * 100
    result["april_addition_pp"] = stage["april_addition"] * 100
    result["profile"] = profile["id"]
    result["profile_label"] = profile["label"]
    result["sigma"], result["eta"], result["supply_scale"] = sigma, eta, scale
    result["max_relative_residual"] = max(d0["max_relative_residual"], d1["max_relative_residual"])
    result["capacity_tonnes"] = base.capacity_tonnes.to_numpy()
    return result


def main_comparison(root, config):
    policy, tables = config["april_2025"], []
    for profile, regime in product(policy["profiles"], policy["regimes"]):
        base, local = configured_base(root, config, profile, regime)
        for stage in policy["stages"]:
            table = paired_stage(base, local, profile, stage)
            table["regime"], table["regime_label"] = regime["id"], regime["label"]
            tables.append(table)
    return pd.concat(tables, ignore_index=True)


def robustness(root, config):
    policy = config["april_2025"]
    profile = next(p for p in policy["profiles"] if p["id"] == policy["reference_profile"])
    regime = next(r for r in policy["regimes"] if r["id"] == policy["reference_regime"])
    stage = next(s for s in policy["stages"] if s["id"] == policy["focus_stage"])
    base, local = configured_base(root, config, profile, regime)
    grid = policy["sensitivity"]
    tables = []
    for sigma, eta, scale in product(grid["sigma"], grid["eta"], grid["supply_scale"]):
        table = paired_stage(base, local, profile, stage, sigma, eta, scale)
        table["test"] = "elasticity"
        table["capacity_multiplier_test"] = np.nan
        tables.append(table)
    for capacity in policy["capacity_test"]:
        changed, local = configured_base(root, config, profile, regime, capacity)
        table = paired_stage(changed, local, profile, stage)
        table["test"], table["capacity_multiplier_test"] = "capacity", capacity
        tables.append(table)
    return pd.concat(tables, ignore_index=True)


def check_april(main, sensitivity, config):
    zero = main.loc[main.scenario.eq("no_april")]
    all_rows = pd.concat([main, sensitivity], ignore_index=True)
    checks = {
        "zero_april_shock_zero_effect": bool(np.allclose(zero.april_quantity_change_pct, 0)),
        "positive_prices_quantities": bool((all_rows[["fob_usd_per_tonne", "quantity_tonnes"]] > 0).all().all()),
        "capacity_respected": bool((all_rows.quantity_tonnes <= all_rows.capacity_tonnes * (1 + 1e-7)).all()),
        "fob_accounting": bool(np.allclose(all_rows.value_usd, all_rows.quantity_tonnes * all_rows.fob_usd_per_tonne)),
        "market_clearing": bool(all_rows.max_relative_residual.max() <= config["solver"]["residual_threshold"])}
    us = main.loc[main.country.eq("USA")]
    monotonic = [np.diff(g.sort_values("april_addition_pp").quantity_tonnes) for _, g in us.groupby(["profile", "regime"])]
    checks["us_quantity_monotonic"] = bool(all((d <= 1e-5).all() for d in monotonic))
    checks["quantity_share_sum"] = bool(np.allclose(main.groupby(["profile", "regime", "scenario"]).quantity_share.sum(), 1))
    checks["value_share_sum"] = bool(np.allclose(main.groupby(["profile", "regime", "scenario"]).value_share.sum(), 1))
    exempt = us.loc[us.regime.eq("legacy_excluded") & us.scenario.eq("april12_125")]
    full = us.loc[us.regime.eq("legacy_not_excluded") & us.scenario.eq("april12_125")]
    checks["tariff_138pct_conditional"] = bool(np.allclose(exempt.tariff, 1.38))
    checks["tariff_165_5pct_conditional"] = bool(np.allclose(full.tariff, 1.655))
    if not all(checks.values()):
        raise AssertionError(checks)
    return checks
