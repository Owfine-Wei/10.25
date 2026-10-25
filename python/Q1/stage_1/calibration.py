"""按基期含税支出份额校准归一化 CES 系统。"""
import numpy as np
import pandas as pd


def calibrate(path, config):
    history = pd.read_csv(path)
    countries = config["countries"]
    base = history.loc[history.year.eq(config["base_year"])].set_index("country")
    if set(base.index) != set(countries) or len(base) != len(countries):
        raise ValueError("基期必须包含每个来源国且只能有一条记录")
    base = base.loc[countries].copy()
    params = config["model"]
    for key in ("base_tariff", "freight_usd_per_tonne", "supply_elasticity", "capacity_multiplier"):
        base[key] = [params[key][country] for country in countries]
    if params["substitution_elasticity"] <= 0 or params["demand_elasticity"] < 0:
        raise ValueError("替代弹性必须为正，需求弹性不能为负")
    if (base.supply_elasticity <= 0).any() or (base.capacity_multiplier < 1).any():
        raise ValueError("供给弹性必须为正，供给上限不能低于基期")
    if (base.base_tariff < 0).any() or (base.freight_usd_per_tonne < 0).any():
        raise ValueError("基准税率和运费不能为负")
    base["landed_price_base"] = (base.fob_usd_per_tonne + base.freight_usd_per_tonne) * (1 + base.base_tariff)
    expenditure = base.quantity_tonnes * base.landed_price_base
    base["ces_weight"] = expenditure / expenditure.sum()
    base["capacity_tonnes"] = base.quantity_tonnes * base.capacity_multiplier
    if not np.isclose(base.ces_weight.sum(), 1):
        raise ValueError("CES 支出权重之和必须为 1")
    return history, base
