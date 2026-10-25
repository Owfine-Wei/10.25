"""检查经济系统的基准复现、约束、会计关系和政策响应。"""
import numpy as np

from stage_2.equilibrium import solve


def verify(base, config, results, curve):
    baseline = results.loc[results.scenario.eq("baseline")].set_index("country").loc[base.index]
    checks = {
        "baseline_quantity_reproduced": bool(np.allclose(baseline.quantity_tonnes, base.quantity_tonnes, rtol=1e-7)),
        "baseline_price_reproduced": bool(np.allclose(baseline.fob_usd_per_tonne, base.fob_usd_per_tonne, rtol=1e-7)),
        "value_equals_fob_times_quantity": bool(np.allclose(results.value_usd, results.fob_usd_per_tonne * results.quantity_tonnes)),
        "quantity_shares_sum_to_one": bool(np.allclose(results.groupby("scenario").quantity_share.sum(), 1)),
        "value_shares_sum_to_one": bool(np.allclose(results.groupby("scenario").value_share.sum(), 1)),
        "positive_quantities_prices": bool((results[["quantity_tonnes", "fob_usd_per_tonne"]] > 0).all().all())}
    limits = results.country.map(base.capacity_tonnes)
    checks["capacity_respected"] = bool((results.quantity_tonnes <= limits * (1 + 1e-7)).all())
    us_curve = curve.loc[curve.country.eq("USA")].sort_values("tariff_addition_pp")
    checks["us_volume_nonincreasing_in_tariff"] = bool((np.diff(us_curve.quantity_tonnes) <= 1e-5).all())
    scenario = {"id": "stress", "label": "容量边界检验", "tariff_addition": {"USA": 1.0}}
    constrained = base.copy()
    constrained["capacity_tonnes"] = constrained.quantity_tonnes
    stress, _ = solve(constrained, config, scenario)
    checks["binding_capacity_case_solved"] = bool(stress.loc[stress.country.isin(["BRA", "ARG"]), "capacity_binding"].all())
    unit_sigma, _ = solve(base, config, {"id": "unit", "label": "单位替代弹性", "tariff_addition": {}}, sigma=1.0)
    checks["sigma_one_limit_reproduces_baseline"] = bool(np.allclose(unit_sigma.quantity_tonnes, base.quantity_tonnes))
    if not all(checks.values()):
        raise AssertionError("验证失败：{}".format(checks))
    return checks
