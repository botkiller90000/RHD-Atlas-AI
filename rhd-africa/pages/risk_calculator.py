import streamlit as st
import numpy as np
import plotly.graph_objects as go

DARK = {
    "paper": "#0d1117", "plot": "#161b22", "grid": "#21262d",
    "text": "#e6edf3", "muted": "#8b949e", "accent": "#f85149",
    "blue": "#58a6ff", "green": "#3fb950", "yellow": "#e3b341",
}


def hex_to_rgba(hex_color, alpha=0.2):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


RISK_FACTORS = {
    "Age 5–14 years": 2.8,
    "Age 15–29 years": 2.2,
    "Female sex": 1.4,
    "Prior rheumatic fever episode": 4.5,
    "Household overcrowding (>3 persons/room)": 2.1,
    "No access to primary care": 2.6,
    "Urban slum / informal settlement": 1.8,
    "GAS pharyngitis in past 12 months": 3.2,
    "Family history of RHD": 1.9,
    "Low health expenditure region (<$50/capita)": 1.7,
    "No penicillin prophylaxis": 3.8,
    "Heart murmur detected on auscultation": 5.1,
}

BASELINE_RISK = 0.008


def compute_risk(selected_factors):
    prob = BASELINE_RISK
    for factor, rr in RISK_FACTORS.items():
        if factor in selected_factors:
            prob = 1 - (1 - prob) * (1 - min(prob * (rr - 1), 0.95))
    prob = min(prob, 0.98)
    return prob


def risk_category(prob):
    if prob < 0.05:
        return "Low", DARK["green"]
    elif prob < 0.20:
        return "Moderate", DARK["yellow"]
    elif prob < 0.50:
        return "High", DARK["accent"]
    else:
        return "Very High", "#ff4444"


def render():
    st.markdown("## ⚕️ RHD Risk Calculator")
    st.markdown(
        "Evidence-based Bayesian risk estimation for Rheumatic Heart Disease. "
        "Select all applicable risk factors to compute a personalised probability estimate."
    )

    st.markdown("### Select Risk Factors")
    selected = []
    cols = st.columns(2)
    factor_list = list(RISK_FACTORS.keys())
    for i, factor in enumerate(factor_list):
        rr = RISK_FACTORS[factor]
        label = f"{factor} &nbsp; *(RR = {rr})*"
        with cols[i % 2]:
            if st.checkbox(factor, key=f"rf_{i}"):
                selected.append(factor)

    st.markdown("---")

    prob = compute_risk(selected)
    cat, cat_color = risk_category(prob)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div style="background:{DARK["plot"]};border:2px solid {cat_color};border-radius:12px;'
            f'padding:1.2rem;text-align:center">'
            f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Estimated Risk</div>'
            f'<div style="font-size:2rem;font-weight:800;color:{cat_color}">{prob*100:.1f}%</div>'
            f'<div style="font-size:0.9rem;color:{cat_color}">{cat} Risk</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with m2:
        n_factors = len(selected)
        st.markdown(
            f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:12px;'
            f'padding:1.2rem;text-align:center">'
            f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Factors Selected</div>'
            f'<div style="font-size:2rem;font-weight:800;color:{DARK["blue"]}">{n_factors}</div>'
            f'<div style="font-size:0.9rem;color:{DARK["muted"]}">of {len(RISK_FACTORS)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with m3:
        nnt = int(round(1 / max(prob - BASELINE_RISK, 0.001)))
        nnt_str = f"1 in {min(nnt, 9999):,}"
        st.markdown(
            f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:12px;'
            f'padding:1.2rem;text-align:center">'
            f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Attributable Risk</div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:{DARK["yellow"]}">{nnt_str}</div>'
            f'<div style="font-size:0.9rem;color:{DARK["muted"]}">excess cases/population</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Risk Gauge")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number=dict(suffix="%", font=dict(color=DARK["text"], size=28)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=DARK["muted"], tickfont=dict(color=DARK["muted"])),
            bar=dict(color=cat_color, thickness=0.25),
            bgcolor=DARK["plot"],
            borderwidth=0,
            steps=[
                dict(range=[0, 5], color=hex_to_rgba(DARK["green"], 0.25)),
                dict(range=[5, 20], color=hex_to_rgba(DARK["yellow"], 0.25)),
                dict(range=[20, 50], color=hex_to_rgba(DARK["accent"], 0.25)),
                dict(range=[50, 100], color=hex_to_rgba("#ff4444", 0.25)),
            ],
            threshold=dict(line=dict(color=DARK["text"], width=3), thickness=0.8, value=prob * 100),
        ),
    ))
    fig_gauge.update_layout(
        paper_bgcolor=DARK["paper"],
        font=dict(color=DARK["text"]),
        height=280,
        margin=dict(l=30, r=30, t=20, b=20),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    if selected:
        st.markdown("#### Factor Contribution")
        factor_risks = []
        for f in selected:
            rr = RISK_FACTORS[f]
            marginal = BASELINE_RISK * (rr - 1)
            factor_risks.append((f, marginal))
        factor_risks.sort(key=lambda x: x[1], reverse=True)
        labels = [x[0] for x in factor_risks]
        values = [x[1] * 100 for x in factor_risks]
        bar_colors = [DARK["accent"] if v > np.median(values) else DARK["blue"] for v in values]

        fig_bar = go.Figure(go.Bar(
            x=values, y=labels, orientation="h",
            marker_color=bar_colors,
            text=[f"+{v:.2f}%" for v in values],
            textposition="outside",
            textfont=dict(color=DARK["text"], size=11),
        ))
        fig_bar.update_layout(
            paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
            font=dict(color=DARK["text"]),
            xaxis=dict(title="Marginal Risk Contribution (%)", gridcolor=DARK["grid"]),
            yaxis=dict(gridcolor=DARK["grid"]),
            margin=dict(l=10, r=60, t=10, b=30),
            height=max(200, 35 * len(selected) + 60),
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Clinical Guidance")
    guidance = {
        "Low": (
            DARK["green"],
            "**Low Risk (<5%):** Routine screening recommended at next primary care visit. "
            "Educate on GAS pharyngitis recognition and treatment-seeking behaviour.",
        ),
        "Moderate": (
            DARK["yellow"],
            "**Moderate Risk (5–20%):** Targeted screening with auscultation within 3 months. "
            "Consider echocardiographic evaluation if murmur detected.",
        ),
        "High": (
            DARK["accent"],
            "**High Risk (20–50%):** Priority echocardiographic evaluation within 4 weeks. "
            "Initiate secondary prophylaxis discussion. Cardiology referral if pathology confirmed.",
        ),
        "Very High": (
            "#ff4444",
            "**Very High Risk (>50%):** Urgent cardiology referral. Echocardiogram within 1 week. "
            "Initiate benzathine penicillin G prophylaxis pending confirmation.",
        ),
    }
    color, text = guidance[cat]
    st.markdown(
        f'<div style="background:{DARK["plot"]};border-left:4px solid {color};'
        f'border-radius:4px;padding:1rem;margin-top:0.5rem">'
        f'<span style="color:{DARK["text"]}">{text}</span></div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "⚠️ This tool is for educational and research purposes only. "
        "It does not constitute medical advice. All risk estimates are derived from "
        "published epidemiological relative risks and should be interpreted by qualified clinicians."
    )
