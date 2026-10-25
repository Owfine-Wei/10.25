"""仅中国市场：CES 进口需求与有上限的对华出口供给联立。"""
import numpy as np
import pandas as pd
from scipy.optimize import least_squares


def demand(log_price_ratio, base, tariffs, sigma, eta):
    """返回实物需求与 CES 价格指数；指数基期归一化为 1。"""
    price = base.fob_usd_per_tonne.to_numpy() * np.exp(log_price_ratio)
    landed = (price + base.freight_usd_per_tonne.to_numpy()) * (1 + tariffs)
    relative = landed / base.landed_price_base.to_numpy()
    weights = base.ces_weight.to_numpy()
    if abs(sigma - 1) < 1e-8:
        index = np.exp(np.sum(weights * np.log(relative)))
    else:
        index = np.sum(weights * relative ** (1 - sigma)) ** (1 / (1 - sigma))
    quantity = base.quantity_tonnes.to_numpy() * relative ** (-sigma) * index ** (sigma - eta)
    return quantity, float(index), price, landed


def supply(log_price_ratio, base, supply_scale=1.0):
    """供给是可对华销售量，不推断全国生产或其他目的地贸易。"""
    elasticities = base.supply_elasticity.to_numpy() * supply_scale
    unconstrained = base.quantity_tonnes.to_numpy() * np.exp(elasticities * log_price_ratio)
    return np.minimum(unconstrained, base.capacity_tonnes.to_numpy())


def solve(base, config, scenario, sigma=None, eta=None, supply_scale=1.0):
    params = config["model"]
    sigma = params["substitution_elasticity"] if sigma is None else sigma
    eta = params["demand_elasticity"] if eta is None else eta
    if sigma <= 0 or eta < 0 or supply_scale <= 0:
        raise ValueError("无效弹性参数")
    additions = scenario["tariff_addition"]
    if set(additions) - set(base.index):
        raise ValueError("关税情景含未知国家")
    tariffs = base.base_tariff.to_numpy() + np.array([additions.get(c, 0) for c in base.index])
    if (tariffs < 0).any():
        raise ValueError("情景最终税率不能小于零")

    def residual(log_price_ratio):
        quantity = demand(log_price_ratio, base, tariffs, sigma, eta)[0]
        offered = supply(log_price_ratio, base, supply_scale)
        return np.log(quantity / offered)

    settings = config["solver"]
    tol = settings["tolerance"]
    fit = least_squares(residual, np.zeros(len(base)), bounds=(-10, 10),
                        xtol=tol, ftol=tol, gtol=tol, max_nfev=settings["max_nfev"])
    quantity, index, prices, landed = demand(fit.x, base, tariffs, sigma, eta)
    offered = supply(fit.x, base, supply_scale)
    error = float(np.max(np.abs(quantity / offered - 1)))
    if not fit.success or error > settings["residual_threshold"]:
        raise RuntimeError("均衡失败：{}，残差={}".format(scenario["id"], error))
    result = pd.DataFrame({"scenario": scenario["id"], "label": scenario["label"],
                           "country": base.index, "tariff": tariffs,
                           "quantity_tonnes": quantity, "fob_usd_per_tonne": prices,
                           "landed_usd_per_tonne": landed, "value_usd": quantity * prices,
                           "quantity_share": quantity / quantity.sum(),
                           "capacity_binding": np.isclose(quantity, base.capacity_tonnes, rtol=1e-7)})
    result["value_share"] = result.value_usd / result.value_usd.sum()
    result["quantity_change_pct"] = (quantity / base.quantity_tonnes.to_numpy() - 1) * 100
    result["price_change_pct"] = (prices / base.fob_usd_per_tonne.to_numpy() - 1) * 100
    result["value_change_pct"] = (result.value_usd.to_numpy() / base.value_usd.to_numpy() - 1) * 100
    diagnostics = {"scenario": scenario["id"], "price_index": index,
                   "composite_demand_ratio": index ** (-eta), "max_relative_residual": error,
                   "total_quantity_tonnes": float(quantity.sum()),
                   "total_value_usd": float(result.value_usd.sum()), "nfev": fit.nfev}
    return result, diagnostics
