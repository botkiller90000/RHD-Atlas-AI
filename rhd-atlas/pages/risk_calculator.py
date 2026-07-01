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


def compute_wilkins(mobility, thickening, calcification, subvalvular):
    """Wilkins Score: sum of 4 components, each 1–4. Score ≤8 = favourable for PBMV."""
    return mobility + thickening + calcification + subvalvular


def wilkins_interpretation(score):
    if score <= 8:
        return "Favourable (≤8)", DARK["green"], (
            "Score ≤8 indicates favourable valve morphology for percutaneous balloon "
            "mitral valvotomy (PBMV). Good procedural outcomes expected."
        )
    elif score <= 11:
        return "Intermediate (9–11)", DARK["yellow"], (
            "Score 9–11 indicates intermediate morphology. PBMV may still be considered "
            "with careful patient selection and operator expertise."
        )
    else:
        return "Unfavourable (≥12)", DARK["accent"], (
            "Score ≥12 indicates unfavourable valve morphology. Surgical mitral valve "
            "repair or replacement should be considered over PBMV."
        )


def render():
    st.markdown("## ⚕️ RHD Risk Calculator")
    st.markdown(
        "Evidence-based Bayesian risk estimation for Rheumatic Heart Disease. "
        "Select all applicable risk factors to compute a personalised probability estimate."
    )

    tab_risk, tab_wilkins = st.tabs(["🎯 Population Risk Score", "🫀 Wilkins Echo Score"])

    # ── Tab 1: Population Risk ──────────────────────────────────────────────
    with tab_risk:
        st.markdown("### Select Risk Factors")
        selected = []
        cols = st.columns(2)
        factor_list = list(RISK_FACTORS.keys())
        for i, factor in enumerate(factor_list):
            rr = RISK_FACTORS[factor]
            with cols[i % 2]:
                if st.checkbox(f"{factor}  *(RR = {rr})*", key=f"rf_{i}"):
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

    # ── Tab 2: Wilkins Score ────────────────────────────────────────────────
    with tab_wilkins:
        st.markdown("### Wilkins Echocardiographic Score")
        st.markdown(
            "The Wilkins Score assesses mitral valve morphology using four echocardiographic "
            "parameters. Each parameter is scored 1–4; the total score (4–16) guides decision-making "
            "for percutaneous balloon mitral valvotomy (PBMV) in rheumatic mitral stenosis."
        )

        with st.expander("📖 Scoring Guide"):
            st.markdown("""
            | Grade | Leaflet Mobility | Leaflet Thickening | Calcification | Subvalvular Thickening |
            |-------|-----------------|-------------------|--------------|----------------------|
            | **1** | Highly mobile, restriction only at tips | Near normal (4–5 mm) | Single area of brightness | Minimal thickening just below leaflets |
            | **2** | Mid-portion and base have normal mobility | Mid-leaflet thickening; margins nearly normal (5–8 mm) | Scattered areas of brightness confined to margins | Thickening of chordal structures extending to one-third of chordal length |
            | **3** | Valve continues to move forward in diastole, mainly from the base | Thickening extending through entire leaflet (5–8 mm) | Brightness extending into mid-portion of leaflets | Thickening to distal third of the chords |
            | **4** | No or minimal forward movement of leaflet in diastole | Marked thickening of all leaflet tissue (>8–10 mm) | Extensive brightness throughout much of the leaflet tissue | Extensive thickening and shortening of all chordal structures extending to papillary muscles |
            
            **Interpretation:** Score ≤8 → favourable for PBMV · Score 9–11 → intermediate · Score ≥12 → unfavourable
            """)

        st.markdown("---")
        wc1, wc2 = st.columns(2)

        with wc1:
            mobility = st.slider(
                "**1. Leaflet Mobility**",
                min_value=1, max_value=4, value=2,
                help="Degree of anterior mitral leaflet mobility during diastole",
                key="wilkins_mob",
            )
            thickening = st.slider(
                "**2. Leaflet Thickening**",
                min_value=1, max_value=4, value=2,
                help="Degree of leaflet thickening on echocardiography",
                key="wilkins_thick",
            )

        with wc2:
            calcification = st.slider(
                "**3. Calcification**",
                min_value=1, max_value=4, value=2,
                help="Degree of leaflet calcification (echo brightness)",
                key="wilkins_calc",
            )
            subvalvular = st.slider(
                "**4. Subvalvular Thickening**",
                min_value=1, max_value=4, value=2,
                help="Degree of thickening of the subvalvular apparatus",
                key="wilkins_sub",
            )

        total_score = compute_wilkins(mobility, thickening, calcification, subvalvular)
        interp_label, interp_color, interp_text = wilkins_interpretation(total_score)

        st.markdown("---")
        ws1, ws2, ws3 = st.columns(3)
        with ws1:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:2px solid {interp_color};border-radius:12px;'
                f'padding:1.2rem;text-align:center">'
                f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Total Wilkins Score</div>'
                f'<div style="font-size:2.5rem;font-weight:800;color:{interp_color}">{total_score}</div>'
                f'<div style="font-size:0.85rem;color:{interp_color}">{interp_label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with ws2:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:12px;'
                f'padding:1.2rem;text-align:center">'
                f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Score Range</div>'
                f'<div style="font-size:1.4rem;font-weight:700;color:{DARK["blue"]}">4 – 16</div>'
                f'<div style="font-size:0.85rem;color:{DARK["muted"]}">Min – Max</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with ws3:
            pct = (total_score - 4) / 12 * 100
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:12px;'
                f'padding:1.2rem;text-align:center">'
                f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Severity Percentile</div>'
                f'<div style="font-size:1.4rem;font-weight:700;color:{DARK["yellow"]}">{pct:.0f}%</div>'
                f'<div style="font-size:0.85rem;color:{DARK["muted"]}">within scoring range</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Radar chart for component breakdown
        st.markdown("#### Component Breakdown")
        components = ["Leaflet Mobility", "Leaflet Thickening", "Calcification", "Subvalvular Thickening"]
        values_radar = [mobility, thickening, calcification, subvalvular]
        theta = components + [components[0]]
        r_vals = values_radar + [values_radar[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals, theta=theta,
            fill="toself",
            fillcolor=hex_to_rgba(interp_color, 0.25),
            line=dict(color=interp_color, width=2),
            name="Wilkins Score",
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor=DARK["plot"],
                radialaxis=dict(
                    visible=True, range=[0, 4],
                    gridcolor=DARK["grid"],
                    tickfont=dict(color=DARK["muted"], size=9),
                    tickvals=[1, 2, 3, 4],
                ),
                angularaxis=dict(gridcolor=DARK["grid"], tickfont=dict(color=DARK["text"], size=11)),
            ),
            paper_bgcolor=DARK["paper"],
            font=dict(color=DARK["text"]),
            showlegend=False,
            margin=dict(l=30, r=30, t=20, b=20),
            height=320,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Score bar gauge
        fig_bar = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_score,
            number=dict(font=dict(color=DARK["text"], size=28)),
            gauge=dict(
                axis=dict(range=[4, 16], tickcolor=DARK["muted"], tickfont=dict(color=DARK["muted"])),
                bar=dict(color=interp_color, thickness=0.25),
                bgcolor=DARK["plot"],
                borderwidth=0,
                steps=[
                    dict(range=[4, 8], color=hex_to_rgba(DARK["green"], 0.25)),
                    dict(range=[8, 12], color=hex_to_rgba(DARK["yellow"], 0.25)),
                    dict(range=[12, 16], color=hex_to_rgba(DARK["accent"], 0.25)),
                ],
                threshold=dict(line=dict(color=DARK["text"], width=3), thickness=0.8, value=total_score),
            ),
        ))
        fig_bar.update_layout(
            paper_bgcolor=DARK["paper"],
            font=dict(color=DARK["text"]),
            height=240,
            margin=dict(l=30, r=30, t=10, b=10),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### Clinical Implication")
        st.markdown(
            f'<div style="background:{DARK["plot"]};border-left:4px solid {interp_color};'
            f'border-radius:4px;padding:1rem;margin-top:0.5rem">'
            f'<span style="color:{DARK["text"]}">{interp_text}</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            "**Reference:** Wilkins GT, et al. *Percutaneous balloon dilatation of the mitral valve: "
            "an analysis of echocardiographic variables related to outcome and the mechanism of dilatation.* "
            "Br Heart J. 1988;60(4):299–308."
        )

    st.caption(
        "⚠️ This tool is for educational and research purposes only. "
        "It does not constitute medical advice. All risk estimates are derived from "
        "published epidemiological relative risks and should be interpreted by qualified clinicians."
    )
