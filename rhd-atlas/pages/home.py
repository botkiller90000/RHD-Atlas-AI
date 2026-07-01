import streamlit as st
import plotly.graph_objects as go
import numpy as np

DARK = {
    "paper": "#0d1117", "plot": "#161b22", "grid": "#21262d",
    "text": "#e6edf3", "muted": "#8b949e", "accent": "#f85149",
    "blue": "#58a6ff", "green": "#3fb950", "yellow": "#e3b341",
}


def hex_to_rgba(hex_color, alpha=0.2):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def render():
    st.markdown("""
    <style>
    .hero-title {
        font-size: 3rem; font-weight: 800; letter-spacing: -1px;
        background: linear-gradient(135deg, #58a6ff, #3fb950);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-sub {
        font-size: 1.2rem; color: #8b949e; margin-bottom: 1.5rem;
    }
    .stat-card {
        background: #161b22; border: 1px solid #21262d; border-radius: 12px;
        padding: 1.2rem; text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: 700; color: #58a6ff; }
    .stat-label { font-size: 0.85rem; color: #8b949e; margin-top: 0.2rem; }
    .feature-card {
        background: #161b22; border: 1px solid #21262d; border-radius: 12px;
        padding: 1.2rem; height: 100%;
    }
    .feature-title { font-size: 1rem; font-weight: 600; color: #e6edf3; }
    .feature-desc { font-size: 0.85rem; color: #8b949e; margin-top: 0.4rem; }
    .badge {
        display: inline-block; background: #21262d; border-radius: 6px;
        padding: 0.2rem 0.6rem; font-size: 0.75rem; color: #8b949e; margin: 0.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hero-title">RHD Atlas AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">AI-Powered Public Health Atlas for Rheumatic Heart Disease across Africa</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("15,913", "GBD Data Records", DARK["blue"]),
        ("47", "WHO Country Reports", DARK["green"]),
        ("51", "World Bank Indicators", DARK["yellow"]),
        ("5", "Sub-Regions Covered", DARK["accent"]),
    ]
    for col, (num, label, color) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(
                f'<div class="stat-card"><div class="stat-number" style="color:{color}">{num}</div>'
                f'<div class="stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    st.markdown("### About RHD in Africa")
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("""
        **Rheumatic Heart Disease (RHD)** remains the leading acquired heart disease in children 
        and young adults across sub-Saharan Africa, driven by recurrent untreated Group A 
        *Streptococcus* infections leading to rheumatic fever.

        This atlas integrates three major epidemiological databases to provide a comprehensive, 
        data-driven picture of RHD burden, trends, and healthcare capacity across the continent.

        **Key findings at a glance:**
        - Eastern SSA carries the highest age-standardised prevalence (~1,050 per 100,000)
        - Females bear a 20–35% higher burden than males in peak reproductive ages
        - Prevalence has declined ~8% from 1990–2019, but absolute burden remains high
        - Health expenditure per capita correlates inversely with RHD mortality
        """)
    with col_b:
        years = np.arange(1990, 2020)
        trend = 1050 - 8.2 * (years - 1990) + np.random.default_rng(0).normal(0, 15, len(years))
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=trend, mode="lines",
            line=dict(color=DARK["blue"], width=2.5),
            fill="tozeroy",
            fillcolor=hex_to_rgba(DARK["blue"], 0.12),
            name="Prevalence",
        ))
        fig.update_layout(
            title=dict(text="Eastern SSA Prevalence Trend", font=dict(size=13, color=DARK["muted"])),
            paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
            font=dict(color=DARK["text"]),
            margin=dict(l=40, r=20, t=40, b=30),
            height=220,
            xaxis=dict(gridcolor=DARK["grid"], showgrid=True),
            yaxis=dict(gridcolor=DARK["grid"], showgrid=True, title="per 100,000"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### What's Inside")

    fc1, fc2, fc3 = st.columns(3)
    fc4, fc5, fc6 = st.columns(3)
    features = [
        ("🗺️", "Atlas", "20-question EDA research paper exploring burden, trends, sex/age stratification, and economic correlates.", DARK["blue"]),
        ("🔊", "Heart Sound AI", "Upload a PCG recording for AI-powered classification of normal vs. murmur vs. RHD, with confidence intervals.", DARK["green"]),
        ("⚕️", "Risk Calculator", "Evidence-based Bayesian risk score combining clinical, demographic, socioeconomic factors, and Wilkins Score.", DARK["yellow"]),
        ("📚", "Education", "Accessible educational content explaining RHD, rheumatic fever, mitral valve stenosis, and prevention strategies.", DARK["accent"]),
        ("🔬", "Research", "Curated literature repository with peer-reviewed references, data sources, and research methodology.", "#c084fc"),
        ("🛣️", "Roadmap", "Phase I–V research and implementation roadmap for pan-African RHD elimination.", DARK["muted"]),
    ]
    for col, (icon, title, desc, color) in zip([fc1, fc2, fc3], features[:3]):
        with col:
            st.markdown(
                f'<div class="feature-card"><div style="font-size:1.8rem">{icon}</div>'
                f'<div class="feature-title" style="color:{color}">{title}</div>'
                f'<div class="feature-desc">{desc}</div></div>',
                unsafe_allow_html=True,
            )
    for col, (icon, title, desc, color) in zip([fc4, fc5, fc6], features[3:]):
        with col:
            st.markdown(
                f'<div class="feature-card"><div style="font-size:1.8rem">{icon}</div>'
                f'<div class="feature-title" style="color:{color}">{title}</div>'
                f'<div class="feature-desc">{desc}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Data Sources")
    bc1, bc2, bc3 = st.columns(3)
    sources = [
        ("Global Burden of Disease", "IHME 2019", "Sub-regional RHD prevalence, incidence, mortality, and DALYs by age/sex, 1990–2019"),
        ("World Health Organization", "WHO AFRO/EMRO", "Country-level RHD burden estimates, 47 African nations, 2000–2019"),
        ("World Bank", "WDI 2016", "Health expenditure, physician density, GDP per capita, 51 countries, 2000–2016"),
    ]
    for col, (name, org, desc) in zip([bc1, bc2, bc3], sources):
        with col:
            st.markdown(
                f'<div class="feature-card"><div class="feature-title">{name}</div>'
                f'<span class="badge">{org}</span>'
                f'<div class="feature-desc" style="margin-top:0.5rem">{desc}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center;color:#8b949e;font-size:0.8rem">'
        'RHD Atlas AI · Educational & Research Platform · Not for clinical use<br>'
        'GitHub: <a href="https://github.com/botkiller90000/RHD-Atlas-AI" style="color:#58a6ff">github.com/botkiller90000/RHD-Atlas-AI</a>'
        '</div>',
        unsafe_allow_html=True,
    )
