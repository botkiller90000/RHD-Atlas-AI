import streamlit as st
import plotly.graph_objects as go
import numpy as np

DARK = {
    "paper": "#0d1117", "plot": "#161b22", "grid": "#21262d",
    "text": "#e6edf3", "muted": "#8b949e", "accent": "#f85149",
    "blue": "#58a6ff", "green": "#3fb950", "yellow": "#e3b341",
}

PHASES = [
    {
        "num": "I",
        "title": "Data Infrastructure & Burden Mapping",
        "status": "complete",
        "completion": 100,
        "color": DARK["green"],
        "description": "Establish unified epidemiological database integrating GBD, WHO, and World Bank datasets. Generate sub-regional prevalence maps and trend analyses.",
        "streams": [
            ("Data harmonisation (GBD, WHO, WB)", True),
            ("Sub-regional burden atlas", True),
            ("Sex and age stratification analysis", True),
            ("Economic correlate modelling", True),
            ("Open data repository", True),
        ],
        "radar": {
            "labels": ["Data Quality", "Coverage", "Harmonisation", "Visualisation", "Dissemination"],
            "values": [90, 95, 88, 92, 80],
        },
    },
    {
        "num": "II",
        "title": "AI Diagnostic Tools",
        "status": "planned",
        "completion": 15,
        "color": DARK["blue"],
        "description": "Develop and validate AI-powered heart sound classifiers and echocardiographic interpretation tools suitable for low-resource settings.",
        "streams": [
            ("PCG dataset curation (n>10,000)", False),
            ("CNN/LSTM classifier development", False),
            ("Multi-site validation (5 countries)", False),
            ("Mobile app for community health workers", False),
            ("Regulatory pathway assessment", False),
        ],
        "radar": {
            "labels": ["Dataset Size", "Model Performance", "Validation", "Deployment", "Regulatory"],
            "values": [20, 10, 5, 5, 8],
        },
    },
    {
        "num": "III",
        "title": "Clinical Integration & Prophylaxis Programmes",
        "status": "planned",
        "completion": 0,
        "color": DARK["yellow"],
        "description": "Integrate screening tools into primary care pathways and establish benzathine penicillin G secondary prophylaxis registries.",
        "streams": [
            ("Prophylaxis registry system", False),
            ("Primary care screening protocol", False),
            ("Community health worker training", False),
            ("Drug supply chain optimisation", False),
            ("Patient adherence monitoring", False),
        ],
        "radar": {
            "labels": ["Registry", "Protocol", "Training", "Supply Chain", "Adherence"],
            "values": [0, 0, 0, 0, 0],
        },
    },
    {
        "num": "IV",
        "title": "Surgical & Interventional Capacity",
        "status": "planned",
        "completion": 0,
        "color": DARK["accent"],
        "description": "Build cardiac surgical capacity across Africa through hub-and-spoke networks, training programmes, and telemedicine cardiology.",
        "streams": [
            ("Cardiac surgery hub network (8 centres)", False),
            ("Cardiothoracic surgeon training pipeline", False),
            ("Telemedicine cardiology platform", False),
            ("Valve procurement consortium", False),
            ("Post-operative monitoring system", False),
        ],
        "radar": {
            "labels": ["Surgical Hubs", "Training", "Telemedicine", "Procurement", "Follow-up"],
            "values": [0, 0, 0, 0, 0],
        },
    },
    {
        "num": "V",
        "title": "Policy, Elimination & Sustainability",
        "status": "planned",
        "completion": 0,
        "color": "#c084fc",
        "description": "Achieve regional RHD elimination targets through policy advocacy, health systems strengthening, and sustainable financing mechanisms.",
        "streams": [
            ("AU/WHO RHD elimination resolution", False),
            ("National RHD control programmes (54 states)", False),
            ("Sustainable financing frameworks", False),
            ("Community-led prevention campaigns", False),
            ("Global RHD elimination declaration", False),
        ],
        "radar": {
            "labels": ["Policy", "National Plans", "Financing", "Community", "Global"],
            "values": [0, 0, 0, 0, 0],
        },
    },
]


def hex_to_rgba(hex_color, alpha=0.2):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def render():
    st.markdown("## 🛣️ RHD Atlas AI — Research Roadmap")

    if "roadmap_phase" not in st.session_state:
        st.session_state.roadmap_phase = 0

    overall = sum(p["completion"] for p in PHASES) / len(PHASES)
    st.markdown("### Overall Programme Progress")
    prog_bar_html = (
        f'<div style="background:{DARK["grid"]};border-radius:8px;height:18px;overflow:hidden;margin-bottom:0.3rem">'
        f'<div style="background:linear-gradient(90deg,{DARK["green"]},{DARK["blue"]});'
        f'width:{overall:.0f}%;height:100%;border-radius:8px;transition:width 0.5s"></div></div>'
        f'<div style="font-size:0.8rem;color:{DARK["muted"]}">{overall:.0f}% complete — Phase I finished, Phases II–V in planning</div>'
    )
    st.markdown(prog_bar_html, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### Phase Overview")
    cols = st.columns(5)
    for i, (col, phase) in enumerate(zip(cols, PHASES)):
        with col:
            border = f"2px solid {phase['color']}" if st.session_state.roadmap_phase == i else f"1px solid {DARK['grid']}"
            bg = hex_to_rgba(phase["color"], 0.12) if st.session_state.roadmap_phase == i else DARK["plot"]
            status_icon = "✅" if phase["status"] == "complete" else "🔵"
            st.markdown(
                f'<div style="background:{bg};border:{border};border-radius:10px;padding:0.8rem;text-align:center">'
                f'<div style="font-size:1.4rem;font-weight:800;color:{phase["color"]}">Phase {phase["num"]}</div>'
                f'<div style="font-size:0.72rem;color:{DARK["muted"]};margin:0.3rem 0">{phase["title"]}</div>'
                f'<div style="font-size:0.8rem">{status_icon} {phase["completion"]}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button(f"View Phase {phase['num']}", key=f"phase_btn_{i}", use_container_width=True):
                st.session_state.roadmap_phase = i
                st.rerun()

    st.markdown("---")
    phase = PHASES[st.session_state.roadmap_phase]

    nav1, nav2, nav3 = st.columns([1, 6, 1])
    with nav1:
        if st.button("◀ Prev", disabled=st.session_state.roadmap_phase == 0):
            st.session_state.roadmap_phase -= 1
            st.rerun()
    with nav2:
        st.markdown(
            f'<h3 style="text-align:center;color:{phase["color"]}">Phase {phase["num"]}: {phase["title"]}</h3>',
            unsafe_allow_html=True,
        )
    with nav3:
        if st.button("Next ▶", disabled=st.session_state.roadmap_phase == len(PHASES) - 1):
            st.session_state.roadmap_phase += 1
            st.rerun()

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown(f"> {phase['description']}")
        st.markdown("**Work Streams**")
        for stream, done in phase["streams"]:
            icon = "✅" if done else "⬜"
            color = DARK["green"] if done else DARK["muted"]
            st.markdown(f'<span style="color:{color}">{icon} {stream}</span>', unsafe_allow_html=True)

        completion = phase["completion"]
        prog_color = phase["color"]
        st.markdown(
            f'<div style="margin-top:1rem"><div style="font-size:0.8rem;color:{DARK["muted"]};margin-bottom:0.3rem">'
            f'Phase completion: {completion}%</div>'
            f'<div style="background:{DARK["grid"]};border-radius:6px;height:12px">'
            f'<div style="background:{prog_color};width:{completion}%;height:100%;border-radius:6px"></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    with col_right:
        radar = phase["radar"]
        theta = radar["labels"] + [radar["labels"][0]]
        r_vals = radar["values"] + [radar["values"][0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=r_vals, theta=theta,
            fill="toself",
            fillcolor=hex_to_rgba(phase["color"], 0.20),
            line=dict(color=phase["color"], width=2),
            name=f"Phase {phase['num']}",
        ))
        fig.update_layout(
            polar=dict(
                bgcolor=DARK["plot"],
                radialaxis=dict(visible=True, range=[0, 100], gridcolor=DARK["grid"],
                                tickfont=dict(color=DARK["muted"], size=9), tickcolor=DARK["muted"]),
                angularaxis=dict(gridcolor=DARK["grid"], tickfont=dict(color=DARK["text"], size=11)),
            ),
            paper_bgcolor=DARK["paper"],
            font=dict(color=DARK["text"]),
            showlegend=False,
            margin=dict(l=30, r=30, t=20, b=20),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Metric Targets by Phase")
    metrics_data = [
        ("Countries with RHD registry", ["0", "5", "15", "35", "54"]),
        ("Community screening sites", ["0", "50", "500", "2,000", "10,000+"]),
        ("Cardiac surgery sites", ["2", "5", "12", "28", "54"]),
        ("Prophylaxis coverage (%)", ["<5%", "15%", "40%", "65%", "80%+"]),
        ("AI tool deployments", ["0", "3", "20", "100", "500+"]),
    ]
    header_cols = st.columns([2, 1, 1, 1, 1, 1])
    header_cols[0].markdown("**Metric**")
    for i, p in enumerate(PHASES):
        header_cols[i + 1].markdown(f'<span style="color:{p["color"]}">**Phase {p["num"]}**</span>', unsafe_allow_html=True)
    for metric, values in metrics_data:
        row_cols = st.columns([2, 1, 1, 1, 1, 1])
        row_cols[0].markdown(metric)
        for j, val in enumerate(values):
            color = PHASES[j]["color"]
            row_cols[j + 1].markdown(f'<span style="color:{color}">{val}</span>', unsafe_allow_html=True)
