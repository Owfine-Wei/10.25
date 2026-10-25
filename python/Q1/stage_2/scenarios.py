"""固定数量的情景与敏感性计算，不为每次求解生成文件。"""
from itertools import product

import pandas as pd

from stage_2.equilibrium import solve


def run_scenarios(base, config):
    tables, diagnostics = [], []
    for scenario in config["scenarios"]:
        table, diagnostic = solve(base, config, scenario)
        tables.append(table)
        diagnostics.append(diagnostic)
    return pd.concat(tables, ignore_index=True), diagnostics


def run_sensitivity(base, config):
    focus = next(s for s in config["scenarios"] if s["id"] == config["focus_scenario"])
    grid = config["sensitivity"]
    tables = []
    combinations = product(grid["substitution_elasticity"], grid["demand_elasticity"], grid["supply_scale"])
    for sigma, eta, scale in combinations:
        table, diagnostic = solve(base, config, focus, sigma, eta, scale)
        table["sigma"], table["eta"], table["supply_scale"] = sigma, eta, scale
        table["max_relative_residual"] = diagnostic["max_relative_residual"]
        tables.append(table)
    return pd.concat(tables, ignore_index=True)


def run_tariff_curve(base, config):
    tables = []
    for addition in config["sensitivity"]["tariff_grid"]:
        scenario = {"id": "sweep", "label": "税率扫描", "tariff_addition": {"USA": addition}}
        table, diagnostic = solve(base, config, scenario)
        table["tariff_addition_pp"] = addition * 100
        table["max_relative_residual"] = diagnostic["max_relative_residual"]
        tables.append(table)
    return pd.concat(tables, ignore_index=True)
