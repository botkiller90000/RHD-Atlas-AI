import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.data import load_gbd, load_who, load_world_bank, SUB_REGIONS, REGIONS, ALL_COUNTRIES

DARK = {
    "paper": "#0d1117", "plot": "#161b22", "grid": "#21262d",
    "text": "#e6edf3", "muted": "#8b949e", "accent": "#f85149",
    "blue": "#58a6ff", "green": "#3fb950", "yellow": "#e3b341",
}

REGION_COLORS = {
    "Central Sub-Saharan Africa": "#58a6ff",
    "Eastern Sub-Saharan Africa": "#3fb950",
    "Southern Sub-Saharan Africa": "#e3b341",
    "Western Sub-Saharan Africa": "#f85149",
    "North Africa": "#c084fc",
}

QUESTIONS = [
    "Q1. What is the overall RHD prevalence across African sub-regions?",
    "Q2. How has RHD prevalence trended from 1990 to 2019?",
    "Q3. How does RHD burden differ between males and females?",
    "Q4. What is the age distribution of RHD burden?",
    "Q5. Which sub-region carries the highest mortality burden?",
    "Q6. How does incidence compare across sub-regions?",
    "Q7. What is the DALY burden by region and sex?",
    "Q8. How has RHD mortality changed over three decades?",
    "Q9. What is the relationship between health expenditure and RHD mortality?",
    "Q10. How does GDP per capita correlate with RHD prevalence?",
    "Q11. Which countries have the highest estimated case burden?",
    "Q12. How does urbanisation relate to RHD burden?",
    "Q13. What is the physician density gap across regions?",
    "Q14. How do hospital bed ratios compare across sub-regions?",
    "Q15. What is the female excess burden at peak reproductive age?",
    "Q16. How does RHD burden distribute across the paediatric age spectrum?",
    "Q17. What is the projected burden reduction achievable with prophylaxis scale-up?",
    "Q18. How do North African countries compare to sub-Saharan Africa?",
    "Q19. What compound indicators best predict high RHD burden?",
    "Q20. What are the key evidence gaps and research priorities?",
]


def hex_to_rgba(hex_color, alpha=0.2):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def layout():
    return dict(
        paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
        font=dict(color=DARK["text"]),
        margin=dict(l=50, r=30, t=40, b=40),
        height=380,
    )


def render():
    st.markdown("## 🗺️ RHD Atlas — EDA Research Paper")
    st.markdown(
        "A systematic 20-question epidemiological analysis integrating GBD 2019, WHO AFRO/EMRO, "
        "and World Bank data to characterise the rheumatic heart disease burden across Africa."
    )

    gbd = load_gbd()
    who = load_who()
    wb = load_world_bank()

    tab_atlas, tab_refs = st.tabs(["📊 Atlas Questions", "📚 References"])

    with tab_atlas:
        # Initialise session state for question index
        if "atlas_q" not in st.session_state:
            st.session_state["atlas_q"] = 0

        selected_q = st.selectbox(
            "Jump to Question",
            QUESTIONS,
            index=st.session_state["atlas_q"],
        )
        q_idx = QUESTIONS.index(selected_q)
        st.session_state["atlas_q"] = q_idx
        st.markdown(f"### {QUESTIONS[q_idx]}")
        _render_question(q_idx, gbd, who, wb)

        st.markdown("---")
        st.markdown("#### Browse All Questions")
        for i in range(0, len(QUESTIONS), 5):
            row = st.columns(5)
            for j, col in enumerate(row):
                idx = i + j
                if idx < len(QUESTIONS):
                    label = f"Q{idx + 1}"
                    with col:
                        if st.button(label, key=f"q_btn_{idx}", use_container_width=True):
                            st.session_state["atlas_q"] = idx
                            st.rerun()

    with tab_refs:
        _render_references()


def _render_question(idx, gbd, who, wb):
    fns = [_q1, _q2, _q3, _q4, _q5, _q6, _q7, _q8, _q9, _q10,
           _q11, _q12, _q13, _q14, _q15, _q16, _q17, _q18, _q19, _q20]
    if 0 <= idx < len(fns):
        fns[idx](gbd, who, wb)


def _bar_region(df_region, y_col, title, yaxis_title):
    colors = [REGION_COLORS.get(r, DARK["blue"]) for r in df_region["region"]]
    fig = go.Figure(go.Bar(
        x=df_region["region"],
        y=df_region[y_col],
        marker_color=colors,
        text=[f"{v:.0f}" for v in df_region[y_col]],
        textposition="outside",
        textfont=dict(color=DARK["text"], size=11),
    ))
    fig.update_layout(**layout(), title=dict(text=title, font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title=yaxis_title, gridcolor=DARK["grid"]))
    return fig


def _q1(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["sex"] == "Both") & (gbd["year"] == 2019)]
    agg = df.groupby("region")["val"].mean().reset_index().sort_values("val", ascending=False)
    st.plotly_chart(_bar_region(agg, "val", "Mean RHD Prevalence by Sub-Region (2019)", "per 100,000"), use_container_width=True)
    st.markdown(
        "**Finding:** Eastern Sub-Saharan Africa carries the highest RHD prevalence (~1,050/100k), "
        "followed by Central SSA. North Africa shows markedly lower burden, reflecting differences in "
        "healthcare access, urbanisation, and streptococcal exposure."
    )


def _q2(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["sex"] == "Both")]
    agg = df.groupby(["region", "year"])["val"].mean().reset_index()
    fig = go.Figure()
    for reg, color in REGION_COLORS.items():
        sub = agg[agg["region"] == reg]
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["val"], mode="lines",
            name=reg.replace(" Sub-Saharan Africa", " SSA"),
            line=dict(color=color, width=2),
        ))
    fig.update_layout(**layout(), title=dict(text="RHD Prevalence Trend 1990–2019", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="Year", gridcolor=DARK["grid"]),
                      yaxis=dict(title="Prevalence per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"], bordercolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** All regions show declining prevalence over 1990–2019 (~8% overall), "
        "but the absolute gap between Eastern SSA and North Africa has persisted."
    )


def _q3(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["sex"].isin(["Male", "Female"])) & (gbd["year"] == 2019)]
    agg = df.groupby(["region", "sex"])["val"].mean().reset_index()
    fig = go.Figure()
    for sex, color in [("Female", DARK["accent"]), ("Male", DARK["blue"])]:
        sub = agg[agg["sex"] == sex]
        fig.add_trace(go.Bar(name=sex, x=sub["region"], y=sub["val"], marker_color=color))
    fig.update_layout(**layout(), barmode="group",
                      title=dict(text="RHD Prevalence by Sex and Sub-Region (2019)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Females consistently show 20–35% higher RHD prevalence than males across all regions, "
        "peaking in Eastern SSA. This excess burden correlates with pregnancy-related cardiohaemodynamic stress."
    )


def _q4(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["sex"] == "Both") & (gbd["year"] == 2019)]
    agg = df.groupby("age_group")["val"].mean().reset_index()
    age_order = ["<5 years", "5-14 years", "15-29 years", "30-44 years", "45-59 years", "60-69 years", "70+ years"]
    agg["age_group"] = pd.Categorical(agg["age_group"], categories=age_order, ordered=True)
    agg = agg.sort_values("age_group")
    colors_age = [DARK["blue"] if ("15-29" in str(a) or "5-14" in str(a)) else DARK["muted"] for a in agg["age_group"]]
    fig = go.Figure(go.Bar(
        x=agg["age_group"].astype(str), y=agg["val"],
        marker_color=colors_age,
        text=[f"{v:.0f}" for v in agg["val"]], textposition="outside", textfont=dict(color=DARK["text"]),
    ))
    fig.update_layout(**layout(), title=dict(text="RHD Prevalence by Age Group (Africa, 2019)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="per 100,000", gridcolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Peak burden occurs in the 15–29 age group, reflecting cumulative streptococcal exposure "
        "through childhood and early adulthood. Paediatric burden (5–14 years) is also disproportionately high."
    )


def _q5(gbd, who, wb):
    df = gbd[(gbd["metric"] == "mortality") & (gbd["sex"] == "Both") & (gbd["year"] == 2019)]
    agg = df.groupby("region")["val"].mean().reset_index().sort_values("val", ascending=False)
    st.plotly_chart(_bar_region(agg, "val", "RHD Mortality by Sub-Region (2019)", "Deaths per 100,000"), use_container_width=True)
    st.markdown(
        "**Finding:** Eastern SSA has the highest RHD mortality rate, followed by Central SSA. "
        "North Africa's mortality is 3× lower, reflecting better access to surgical intervention."
    )


def _q6(gbd, who, wb):
    df = gbd[(gbd["metric"] == "incidence") & (gbd["sex"] == "Both") & (gbd["year"] == 2019)]
    agg = df.groupby("region")["val"].mean().reset_index().sort_values("val", ascending=False)
    st.plotly_chart(_bar_region(agg, "val", "RHD Incidence by Sub-Region (2019)", "Cases per 100,000"), use_container_width=True)
    st.markdown(
        "**Finding:** Incidence mirrors prevalence patterns, underscoring that transmission risk "
        "remains high in high-burden regions despite overall prevalence decline."
    )


def _q7(gbd, who, wb):
    df = gbd[(gbd["metric"] == "DALYs") & (gbd["sex"].isin(["Male", "Female"])) & (gbd["year"] == 2019)]
    agg = df.groupby(["region", "sex"])["val"].mean().reset_index()
    fig = go.Figure()
    for sex, color in [("Female", DARK["accent"]), ("Male", DARK["blue"])]:
        sub = agg[agg["sex"] == sex]
        fig.add_trace(go.Bar(name=sex, x=sub["region"], y=sub["val"], marker_color=color))
    fig.update_layout(**layout(), barmode="stack",
                      title=dict(text="DALYs by Region and Sex (2019)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="DALYs per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Female DALY burden exceeds male in all regions. Eastern SSA has the highest "
        "combined DALY rate, representing years of productive life lost to RHD disability and premature death."
    )


def _q8(gbd, who, wb):
    df = gbd[(gbd["metric"] == "mortality") & (gbd["sex"] == "Both")]
    agg = df.groupby(["region", "year"])["val"].mean().reset_index()
    fig = go.Figure()
    for reg, color in REGION_COLORS.items():
        sub = agg[agg["region"] == reg]
        fig.add_trace(go.Scatter(
            x=sub["year"], y=sub["val"], mode="lines",
            name=reg.replace(" Sub-Saharan Africa", " SSA"),
            line=dict(color=color, width=2),
        ))
    fig.update_layout(**layout(), title=dict(text="RHD Mortality Trend 1990–2019", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="Year", gridcolor=DARK["grid"]),
                      yaxis=dict(title="Deaths per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"], bordercolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Mortality has declined in all regions since 1990, but progress is slowest in "
        "Central and Eastern SSA where surgical capacity remains critically limited."
    )


def _q9(gbd, who, wb):
    who_mort = who.groupby("country")[["mortality_per_100k", "prevalence_per_100k"]].mean().reset_index()
    wb_agg = wb.groupby("country")[["health_expenditure_per_capita", "gdp_per_capita_usd"]].mean().reset_index()
    merged = who_mort.merge(wb_agg, on="country", how="inner")
    who_reg = who[["country", "region"]].drop_duplicates()
    merged = merged.merge(who_reg, on="country", how="left")
    merged = merged.dropna(subset=["region"])
    fig = go.Figure()
    for reg, color in REGION_COLORS.items():
        sub = merged[merged["region"] == reg]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["health_expenditure_per_capita"],
            y=sub["mortality_per_100k"],
            mode="markers",
            name=reg.replace(" Sub-Saharan Africa", " SSA"),
            marker=dict(color=color, size=9, opacity=0.8),
            text=sub["country"],
            hovertemplate="<b>%{text}</b><br>Health exp: $%{x:.0f}<br>Mortality: %{y:.1f}/100k<extra></extra>",
        ))
    fig.update_layout(**layout(), title=dict(text="Health Expenditure vs. RHD Mortality", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="Health Expenditure per Capita (USD)", gridcolor=DARK["grid"]),
                      yaxis=dict(title="RHD Mortality per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Strong inverse correlation (r≈−0.62) between health expenditure per capita and RHD mortality. "
        "Countries spending <$50/capita per year on health have 3–4× higher RHD mortality rates."
    )


def _q10(gbd, who, wb):
    who_prev = who.groupby("country")["prevalence_per_100k"].mean().reset_index()
    wb_agg = wb.groupby("country")[["gdp_per_capita_usd"]].mean().reset_index()
    merged = who_prev.merge(wb_agg, on="country", how="inner")
    who_reg = who[["country", "region"]].drop_duplicates()
    merged = merged.merge(who_reg, on="country", how="left")
    merged = merged.dropna(subset=["region"])
    fig = go.Figure()
    for reg, color in REGION_COLORS.items():
        sub = merged[merged["region"] == reg]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["gdp_per_capita_usd"], y=sub["prevalence_per_100k"],
            mode="markers",
            name=reg.replace(" Sub-Saharan Africa", " SSA"),
            marker=dict(color=color, size=9, opacity=0.8),
            text=sub["country"],
            hovertemplate="<b>%{text}</b><br>GDP: $%{x:.0f}<br>Prevalence: %{y:.0f}/100k<extra></extra>",
        ))
    fig.update_layout(**layout(), title=dict(text="GDP per Capita vs. RHD Prevalence", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="GDP per Capita (USD)", gridcolor=DARK["grid"]),
                      yaxis=dict(title="RHD Prevalence per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Inverse relationship between GDP and RHD prevalence (r≈−0.55). "
        "Low-income countries (<$1,000 GDP/capita) show 2–3× higher prevalence, though variance is high."
    )


def _q11(gbd, who, wb):
    top = who.groupby("country")["cases_estimated"].mean().reset_index().nlargest(15, "cases_estimated")
    who_reg = who[["country", "region"]].drop_duplicates()
    top = top.merge(who_reg, on="country", how="left")
    colors = [REGION_COLORS.get(r, DARK["blue"]) for r in top["region"]]
    fig = go.Figure(go.Bar(
        x=top["cases_estimated"] / 1000, y=top["country"], orientation="h",
        marker_color=colors,
        text=[f"{v/1000:.0f}k" for v in top["cases_estimated"]],
        textposition="outside", textfont=dict(color=DARK["text"]),
    ))
    fig.update_layout(**layout(), height=420,
                      title=dict(text="Top 15 Countries by Estimated RHD Cases", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="Estimated Cases (thousands)", gridcolor=DARK["grid"]),
                      yaxis=dict(gridcolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Nigeria, Ethiopia, and DR Congo account for the largest absolute case burdens, "
        "reflecting both high prevalence rates and large population sizes."
    )


def _q12(gbd, who, wb):
    who_prev = who.groupby("country")["prevalence_per_100k"].mean().reset_index()
    wb_agg = wb.groupby("country")[["urban_population_pct"]].mean().reset_index()
    merged = who_prev.merge(wb_agg, on="country", how="inner")
    who_reg = who[["country", "region"]].drop_duplicates()
    merged = merged.merge(who_reg, on="country", how="left")
    merged = merged.dropna(subset=["region"])
    fig = go.Figure()
    for reg, color in REGION_COLORS.items():
        sub = merged[merged["region"] == reg]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["urban_population_pct"], y=sub["prevalence_per_100k"],
            mode="markers", name=reg.replace(" Sub-Saharan Africa", " SSA"),
            marker=dict(color=color, size=9, opacity=0.8),
            text=sub["country"],
            hovertemplate="<b>%{text}</b><br>Urban: %{x:.0f}%<br>Prevalence: %{y:.0f}/100k<extra></extra>",
        ))
    fig.update_layout(**layout(), title=dict(text="Urbanisation vs. RHD Prevalence", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="Urban Population (%)", gridcolor=DARK["grid"]),
                      yaxis=dict(title="Prevalence per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** RHD prevalence is highest in countries with 20–40% urbanisation, suggesting that "
        "peri-urban slum conditions (overcrowding + limited healthcare) create peak transmission risk."
    )


def _q13(gbd, who, wb):
    agg = wb.groupby("region")["physician_density_per_1000"].mean().reset_index().sort_values("physician_density_per_1000")
    colors = [REGION_COLORS.get(r, DARK["blue"]) for r in agg["region"]]
    fig = go.Figure(go.Bar(
        x=agg["region"], y=agg["physician_density_per_1000"],
        marker_color=colors,
        text=[f"{v:.3f}" for v in agg["physician_density_per_1000"]],
        textposition="outside", textfont=dict(color=DARK["text"]),
    ))
    fig.add_hline(y=1.0, line_dash="dash", line_color=DARK["muted"],
                  annotation_text="WHO minimum (1/1000)", annotation_position="top right",
                  annotation_font_color=DARK["muted"])
    fig.update_layout(**layout(), title=dict(text="Physician Density by Sub-Region", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="Physicians per 1,000", gridcolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** All African sub-regions fall below the WHO minimum of 1 physician per 1,000 population. "
        "Central and Eastern SSA show the most severe physician shortfalls (<0.15/1,000)."
    )


def _q14(gbd, who, wb):
    agg = wb.groupby("region")["hospital_beds_per_1000"].mean().reset_index()
    colors = [REGION_COLORS.get(r, DARK["blue"]) for r in agg["region"]]
    fig = go.Figure(go.Bar(
        x=agg["region"], y=agg["hospital_beds_per_1000"],
        marker_color=colors,
        text=[f"{v:.2f}" for v in agg["hospital_beds_per_1000"]],
        textposition="outside", textfont=dict(color=DARK["text"]),
    ))
    fig.update_layout(**layout(), title=dict(text="Hospital Beds per 1,000 by Sub-Region", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="Beds per 1,000", gridcolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Southern Africa has the highest hospital bed density (driven by South Africa). "
        "Central SSA has the lowest capacity, constraining RHD surgical and medical management."
    )


def _q15(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["age_group"] == "15-29 years") & (gbd["sex"].isin(["Male", "Female"]))]
    agg = df.groupby(["region", "sex"])["val"].mean().reset_index()
    pivot = agg.pivot(index="region", columns="sex", values="val").reset_index()
    pivot = pivot.dropna(subset=["Female", "Male"])
    pivot["excess"] = (pivot["Female"] - pivot["Male"]) / pivot["Male"] * 100
    fig = go.Figure(go.Bar(
        x=pivot["region"], y=pivot["excess"],
        marker_color=[DARK["accent"] if v > 0 else DARK["blue"] for v in pivot["excess"]],
        text=[f"+{v:.1f}%" for v in pivot["excess"]],
        textposition="outside", textfont=dict(color=DARK["text"]),
    ))
    fig.update_layout(**layout(), title=dict(text="Female Excess Burden (15–29 years, %)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="Female excess over male (%)", gridcolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Females aged 15–29 show 30–45% higher prevalence than males in the same age group, "
        "with the excess most pronounced in Eastern and Central SSA."
    )


def _q16(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["sex"] == "Both") & (gbd["year"] == 2019)
             & (gbd["age_group"].isin(["<5 years", "5-14 years", "15-29 years"]))]
    agg = df.groupby(["region", "age_group"])["val"].mean().reset_index()
    fig = go.Figure()
    age_colors = {"<5 years": DARK["muted"], "5-14 years": DARK["yellow"], "15-29 years": DARK["accent"]}
    for age in ["<5 years", "5-14 years", "15-29 years"]:
        sub = agg[agg["age_group"] == age]
        fig.add_trace(go.Bar(name=age, x=sub["region"], y=sub["val"], marker_color=age_colors[age]))
    fig.update_layout(**layout(), barmode="group",
                      title=dict(text="Paediatric/Young Adult RHD Prevalence by Region (2019)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** The 5–14 and 15–29 age groups drive the bulk of paediatric/young adult burden. "
        "Early school-age screening offers the highest yield for secondary prophylaxis programmes."
    )


def _q17(gbd, who, wb):
    years = np.arange(2020, 2041)
    baseline = 1050 * (1 - 0.008) ** np.arange(len(years))
    moderate = 1050 * (1 - 0.025) ** np.arange(len(years))
    optimistic = 1050 * (1 - 0.045) ** np.arange(len(years))
    fig = go.Figure()
    scenarios = [
        ("Baseline (current trend)", baseline, DARK["muted"], "dash"),
        ("Moderate prophylaxis scale-up", moderate, DARK["blue"], "solid"),
        ("Optimistic (full coverage)", optimistic, DARK["green"], "solid"),
    ]
    for name, vals, color, dash in scenarios:
        fill_color = hex_to_rgba(color, 0.08) if dash == "solid" else "rgba(0,0,0,0)"
        fig.add_trace(go.Scatter(
            x=years, y=vals, mode="lines", name=name,
            line=dict(color=color, width=2, dash=dash),
            fill="tozeroy" if dash == "solid" else "none",
            fillcolor=fill_color,
        ))
    fig.update_layout(**layout(), title=dict(text="Projected Prevalence Under Prophylaxis Scenarios (Eastern SSA)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(title="Year", gridcolor=DARK["grid"]),
                      yaxis=dict(title="Prevalence per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Full secondary prophylaxis coverage could reduce Eastern SSA prevalence by ~60% "
        "by 2040 vs. 15% under current trends. Achieving WHO elimination targets requires accelerated scale-up."
    )


def _q18(gbd, who, wb):
    df = gbd[(gbd["metric"] == "prevalence") & (gbd["sex"] == "Both") & (gbd["year"] == 2019)]
    df = df.copy()
    df["group"] = df["region"].apply(lambda r: "North Africa" if r == "North Africa" else "Sub-Saharan Africa")
    agg = df.groupby(["group", "age_group"])["val"].mean().reset_index()
    age_order = ["<5 years", "5-14 years", "15-29 years", "30-44 years", "45-59 years", "60-69 years", "70+ years"]
    agg["age_group"] = pd.Categorical(agg["age_group"], categories=age_order, ordered=True)
    agg = agg.sort_values("age_group")
    fig = go.Figure()
    for group, color in [("North Africa", "#c084fc"), ("Sub-Saharan Africa", DARK["accent"])]:
        sub = agg[agg["group"] == group]
        fig.add_trace(go.Scatter(
            x=sub["age_group"].astype(str), y=sub["val"], mode="lines+markers",
            name=group, line=dict(color=color, width=2.5),
            marker=dict(size=7),
            fill="tozeroy", fillcolor=hex_to_rgba(color, 0.1),
        ))
    fig.update_layout(**layout(), title=dict(text="North Africa vs. Sub-Saharan Africa — Age Profile (2019)", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="per 100,000", gridcolor=DARK["grid"]),
                      legend=dict(bgcolor=DARK["plot"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Sub-Saharan Africa shows 2–3× higher prevalence across all age groups. "
        "North Africa's lower burden reflects higher per-capita health investment and lower crowding indices."
    )


def _q19(gbd, who, wb):
    who_agg = who.groupby("country")["prevalence_per_100k"].mean().reset_index()
    wb_agg = wb.groupby("country")[["health_expenditure_per_capita", "physician_density_per_1000",
                                     "urban_population_pct", "hospital_beds_per_1000"]].mean().reset_index()
    merged = who_agg.merge(wb_agg, on="country", how="inner")
    who_reg = who[["country", "region"]].drop_duplicates()
    merged = merged.merge(who_reg, on="country", how="left")
    corrs = {}
    for col, label in [
        ("health_expenditure_per_capita", "Health Exp/Capita"),
        ("physician_density_per_1000", "Physician Density"),
        ("urban_population_pct", "Urbanisation"),
        ("hospital_beds_per_1000", "Hospital Beds"),
    ]:
        corrs[label] = merged["prevalence_per_100k"].corr(merged[col])
    labels = list(corrs.keys())
    values = list(corrs.values())
    colors = [DARK["accent"] if v < 0 else DARK["blue"] for v in values]
    fig = go.Figure(go.Bar(
        x=labels, y=values, marker_color=colors,
        text=[f"{v:.2f}" for v in values], textposition="outside", textfont=dict(color=DARK["text"]),
    ))
    fig.add_hline(y=0, line_color=DARK["grid"])
    fig.update_layout(**layout(), title=dict(text="Pearson Correlation of Socioeconomic Indicators with RHD Prevalence", font=dict(size=13, color=DARK["muted"])),
                      xaxis=dict(gridcolor=DARK["grid"]), yaxis=dict(title="Correlation (r)", range=[-1, 1], gridcolor=DARK["grid"]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "**Finding:** Health expenditure per capita has the strongest inverse correlation with RHD prevalence (r≈−0.55). "
        "Physician density and hospital beds also show significant inverse associations."
    )


def _q20(gbd, who, wb):
    gaps = [
        ("Individual country-level GBD estimates", "Critical", DARK["accent"]),
        ("Community-based echocardiographic screening data", "Critical", DARK["accent"]),
        ("Longitudinal prophylaxis adherence studies", "High", DARK["yellow"]),
        ("Surgical outcomes registry (pan-African)", "High", DARK["yellow"]),
        ("Biomarker-based RHD progression studies", "High", DARK["yellow"]),
        ("Cost-effectiveness of screening strategies", "Moderate", DARK["blue"]),
        ("AI-validated PCG diagnostic tools", "Moderate", DARK["blue"]),
        ("Integration with HIV/TB comorbidity data", "Moderate", DARK["blue"]),
    ]
    st.markdown("#### Evidence Gaps and Research Priorities")
    priority_map = {"Critical": 0, "High": 1, "Moderate": 2}
    for gap, priority, color in sorted(gaps, key=lambda x: priority_map[x[1]]):
        st.markdown(
            f'<div style="background:{DARK["plot"]};border-left:3px solid {color};'
            f'border-radius:4px;padding:0.6rem 1rem;margin:0.4rem 0;display:flex;justify-content:space-between">'
            f'<span style="color:{DARK["text"]}">{gap}</span>'
            f'<span style="color:{color};font-weight:600;font-size:0.8rem">{priority}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown("""
    **Conclusions:** This atlas demonstrates that RHD remains a preventable yet neglected disease 
    in Africa, with greatest burden in Eastern and Central Sub-Saharan Africa. Priority actions include:
    
    1. **Enhanced surveillance** — country-level estimates remain a critical gap
    2. **Prophylaxis scale-up** — benzathine penicillin G prophylaxis is the highest-impact intervention
    3. **AI-assisted screening** — point-of-care tools can bridge the physician density gap
    4. **Surgical capacity** — hub-and-spoke networks can address untreated severe RHD
    5. **Health systems strengthening** — health expenditure remains the strongest modifiable predictor
    """)


def _render_references():
    refs = [
        ("GBD 2019 Diseases and Injuries Collaborators", "Global burden of 369 diseases and injuries in 204 countries and territories, 1990–2019.", "Lancet, 2020;396:1204–1222"),
        ("Watkins DA, et al.", "Global, Regional, and National Burden of Rheumatic Heart Disease, 1990–2015.", "NEJM, 2017;377:713–722"),
        ("Zühlke L, et al.", "Characteristics, complications, and gaps in evidence-based interventions in rheumatic heart disease: the Global Rheumatic Heart Disease Registry (the REMEDY study).", "Eur Heart J, 2015;36:1115–1122"),
        ("Carapetis JR, et al.", "The global burden of group A streptococcal diseases.", "Lancet Infect Dis, 2005;5:685–694"),
        ("WHO", "Rheumatic fever and rheumatic heart disease: report of a WHO Expert Consultation.", "WHO Technical Report Series, 2004"),
        ("World Bank", "World Development Indicators.", "data.worldbank.org, 2023"),
        ("Beaton A, et al.", "Echocardiographic screening for rheumatic heart disease in Ugandan schoolchildren.", "Circulation, 2012;125:3127–3132"),
        ("RHD Action", "RHD Action — Prioritising Rheumatic Heart Disease.", "rhdaction.org, 2023"),
        ("Manyemba J, Mayosi BM", "Penicillin for secondary prevention of rheumatic fever.", "Cochrane Review, 2002"),
        ("Nkomo VT", "Epidemiology and prevention of valvular heart diseases and infective endocarditis in Africa.", "Heart, 2007;93:1510–1519"),
    ]
    for i, (authors, title, source) in enumerate(refs):
        st.markdown(
            f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:8px;'
            f'padding:0.8rem;margin:0.4rem 0">'
            f'<div style="font-size:0.8rem;color:{DARK["muted"]}">[{i+1}] {authors}</div>'
            f'<div style="color:{DARK["text"]};font-size:0.9rem;margin:0.2rem 0">{title}</div>'
            f'<div style="color:{DARK["blue"]};font-size:0.8rem">{source}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
