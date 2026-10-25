"""数据预处理：抽取中国自美/巴/阿大豆进口，并计算基准份额与价格。"""
from __future__ import annotations

import pandas as pd

COUNTRY_NAME = {"USA": "美国", "BRA": "巴西", "ARG": "阿根廷"}


def build_import_frame(rows: list[dict], exclude_years: list[int]) -> pd.DataFrame:
    """抽取 partnerISO=CHN 且 reporterISO in {USA,BRA,ARG} 的记录，按年+国汇总。

    返回列：year, country, qty_ton（千吨? 实为吨）, fob_usd, price_usd_t, share。
    """
    recs = []
    for r in rows:
        if r.get("reporterISO") in ("USA", "BRA", "ARG") and r.get("partnerISO") == "CHN":
            year = int(r["refYear"])
            if year in exclude_years:
                continue
            qty_ton = float(r["qty"]) / 1000.0
            fob = float(r["fobvalue"])
            recs.append({
                "year": year,
                "country": r["reporterISO"],
                "qty_ton": qty_ton,
                "fob_usd": fob,
                "price_usd_t": fob / qty_ton if qty_ton > 0 else 0.0,
            })
    df = pd.DataFrame(recs)
    total = df.groupby("year")["qty_ton"].transform("sum")
    df["share"] = df["qty_ton"] / total
    return df.sort_values(["year", "country"]).reset_index(drop=True)


def get_base_params(frame: pd.DataFrame, base_year: int) -> dict:
    """从基准年提取基准价格、份额与总进口需求（吨）。"""
    sub = frame[frame["year"] == base_year]
    countries = list(sub["country"])
    base_price = {c: float(sub[sub.country == c]["price_usd_t"].iloc[0]) for c in countries}
    base_share = {c: float(sub[sub.country == c]["share"].iloc[0]) for c in countries}
    total_demand = float(sub["qty_ton"].sum())
    return {
        "countries": countries,
        "base_price": base_price,
        "base_share": base_share,
        "total_demand_ton": total_demand,
    }
