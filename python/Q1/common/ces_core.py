"""Armington CES 核心计算：校准、份额、量额。"""
from __future__ import annotations


def calibrate_alpha(base_share: dict, base_price: dict, base_tariff: dict,
                    sigma: float, countries: list[str]) -> dict:
    """由基准年份额与含税价反推偏好参数 alpha_i（校准）。

    令情景关税等于 base_tariff 时模型精确还原基准年份额，要求：
        alpha_i = s_i0^(1/sigma) * P_i0^((sigma-1)/sigma)，
    其中 P_i0 = p_i*(1+base_tariff_i)。（指数 (sigma-1)/sigma 保证 tau=0 时
    s_i = s_i0 精确成立；若误写为 *P_i0 则只能近似。）
    """
    alpha = {}
    for c in countries:
        p0 = base_price[c] * (1.0 + base_tariff.get(c, 0.0))
        alpha[c] = (base_share[c] ** (1.0 / sigma)) * (p0 ** ((sigma - 1.0) / sigma))
    return alpha


def compute_shares(alpha: dict, price: dict, tariff: dict,
                   sigma: float, countries: list[str]) -> dict:
    """CES 需求份额：s_i = alpha_i^sigma * P_i^(1-sigma) / sum_j。

    P_i = p_i * (1 + tariff_i) 为含税后到岸价。
    """
    terms = {}
    for c in countries:
        p = price[c] * (1.0 + tariff.get(c, 0.0))
        terms[c] = (alpha[c] ** sigma) * (p ** (1.0 - sigma))
    denom = sum(terms.values())
    return {c: terms[c] / denom for c in countries}


def compute_qty_value(shares: dict, total_demand_ton: float, price: dict,
                      tariff: dict, countries: list[str]):
    """由份额反推出口量与出口额（FOB，出口国实际收到的金额）。

    出口额 = qty * p_i（不含关税，关税由进口方承担，不改变出口国 FOB 单价）。
    返回：qty（吨）, value（美元）。
    """
    qty = {c: shares[c] * total_demand_ton for c in countries}
    value = {c: qty[c] * price[c] for c in countries}
    return qty, value
