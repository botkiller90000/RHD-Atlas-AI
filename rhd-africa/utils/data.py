import pandas as pd
import numpy as np
import streamlit as st

np.random.seed(42)

REGIONS = {
    "Central Sub-Saharan Africa": ["DR Congo", "Central African Republic", "Cameroon", "Chad", "Republic of Congo", "Gabon"],
    "Eastern Sub-Saharan Africa": ["Ethiopia", "Kenya", "Tanzania", "Uganda", "Rwanda", "Burundi", "Somalia", "Eritrea", "Madagascar", "Malawi", "Mozambique", "Zambia", "Zimbabwe"],
    "Southern Sub-Saharan Africa": ["South Africa", "Botswana", "Namibia", "Lesotho", "Eswatini"],
    "Western Sub-Saharan Africa": ["Nigeria", "Ghana", "Senegal", "Mali", "Burkina Faso", "Niger", "Guinea", "Sierra Leone", "Liberia", "Ivory Coast", "Togo", "Benin", "Mauritania", "Gambia"],
    "North Africa": ["Egypt", "Morocco", "Algeria", "Tunisia", "Libya", "Sudan", "South Sudan"],
}

ALL_COUNTRIES = [c for countries in REGIONS.values() for c in countries]
SUB_REGIONS = list(REGIONS.keys())

AGES = ["<5 years", "5-14 years", "15-29 years", "30-44 years", "45-59 years", "60-69 years", "70+ years"]
SEXES = ["Male", "Female", "Both"]
YEARS = list(range(1990, 2020))
METRICS = ["prevalence", "incidence", "mortality", "DALYs"]

REG_MULT = {
    "Central Sub-Saharan Africa": 1.25,
    "Eastern Sub-Saharan Africa": 1.35,
    "Southern Sub-Saharan Africa": 0.85,
    "Western Sub-Saharan Africa": 1.15,
    "North Africa": 0.60,
}
SEX_MULT = {"Female": 1.20, "Male": 0.85, "Both": 1.0}
AGE_MULT = {"<5 years": 0.3, "5-14 years": 0.9, "15-29 years": 1.4,
            "30-44 years": 1.2, "45-59 years": 1.0, "60-69 years": 0.85, "70+ years": 0.7}
METRIC_BASE = {"prevalence": 800, "incidence": 120, "mortality": 40, "DALYs": 1200}


def _gbd_val(region, sex, age, year, metric):
    base = METRIC_BASE[metric]
    trend = 1.0 - 0.008 * (year - 1990)
    val = base * REG_MULT[region] * SEX_MULT[sex] * AGE_MULT[age] * trend
    noise = np.random.normal(1.0, 0.04)
    return max(val * noise, 0)


@st.cache_data
def load_gbd():
    rng = np.random.default_rng(42)
    rows = []
    for region in SUB_REGIONS:
        for sex in SEXES:
            for age in AGES:
                for year in YEARS:
                    for metric in METRICS:
                        val = _gbd_val(region, sex, age, year, metric) * rng.normal(1.0, 0.04)
                        val = max(val, 0)
                        ci = val * 0.12
                        rows.append({
                            "region": region,
                            "sex": sex,
                            "age_group": age,
                            "year": year,
                            "metric": metric,
                            "val": round(val, 2),
                            "lower": round(max(val - 1.96 * ci, 0), 2),
                            "upper": round(val + 1.96 * ci, 2),
                            "unit": "per 100,000",
                        })
    return pd.DataFrame(rows)


@st.cache_data
def load_who():
    rng = np.random.default_rng(43)
    rows = []
    who_years = [2000, 2005, 2010, 2015, 2019]
    who_countries = ALL_COUNTRIES[:47]
    for country in who_countries:
        for region, countries in REGIONS.items():
            if country in countries:
                reg = region
                break
        base_prev = {
            "Central Sub-Saharan Africa": 950,
            "Eastern Sub-Saharan Africa": 1050,
            "Southern Sub-Saharan Africa": 650,
            "Western Sub-Saharan Africa": 880,
            "North Africa": 420,
        }[reg]
        for year in who_years:
            trend = 1.0 - 0.007 * (year - 2000)
            prev = max(base_prev * trend * rng.normal(1.0, 0.06), 50)
            mort = prev * 0.048 * rng.normal(1.0, 0.05)
            rows.append({
                "country": country,
                "region": reg,
                "year": year,
                "prevalence_per_100k": round(prev, 1),
                "mortality_per_100k": round(max(mort, 0), 2),
                "cases_estimated": int(prev * rng.integers(50000, 2000000) / 100000),
            })
    return pd.DataFrame(rows)


@st.cache_data
def load_world_bank():
    rng = np.random.default_rng(44)
    rows = []
    wb_years = list(range(2000, 2017))
    wb_countries = ALL_COUNTRIES[:51]
    gdp_base_map = {
        "Central Sub-Saharan Africa": 1200,
        "Eastern Sub-Saharan Africa": 900,
        "Southern Sub-Saharan Africa": 6500,
        "Western Sub-Saharan Africa": 1400,
        "North Africa": 3800,
    }
    for country in wb_countries:
        for region, countries in REGIONS.items():
            if country in countries:
                reg = region
                break
        gdp_base = gdp_base_map.get(reg, 1200)
        for year in wb_years:
            gdp = gdp_base * (1.03 ** (year - 2000)) * rng.normal(1.0, 0.04)
            health_pct = rng.uniform(3.5, 9.5)
            rows.append({
                "country": country,
                "region": reg,
                "year": year,
                "gdp_per_capita_usd": round(gdp, 1),
                "health_expenditure_pct_gdp": round(health_pct, 2),
                "health_expenditure_per_capita": round(gdp * health_pct / 100, 1),
                "physician_density_per_1000": round(rng.uniform(0.02, 0.8), 3),
                "hospital_beds_per_1000": round(rng.uniform(0.3, 3.5), 2),
                "urban_population_pct": round(rng.uniform(20, 75), 1),
            })
    return pd.DataFrame(rows)
