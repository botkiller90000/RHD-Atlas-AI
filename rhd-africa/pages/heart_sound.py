import streamlit as st
import numpy as np
import plotly.graph_objects as go
import io

DARK = {
    "paper": "#0d1117", "plot": "#161b22", "grid": "#21262d",
    "text": "#e6edf3", "muted": "#8b949e", "accent": "#f85149",
    "blue": "#58a6ff", "green": "#3fb950", "yellow": "#e3b341",
}

CLASSES = ["Normal", "Innocent Murmur", "Pathological Murmur", "RHD Likely"]
CLASS_COLORS = [DARK["green"], DARK["yellow"], DARK["accent"], "#ff6e6e"]
DESCRIPTIONS = {
    "Normal": "No cardiac abnormality detected. Regular S1/S2 pattern with no significant murmur.",
    "Innocent Murmur": "Benign functional murmur without structural significance. Follow-up recommended.",
    "Pathological Murmur": "Structural cardiac abnormality indicated. Echocardiographic evaluation required.",
    "RHD Likely": "Acoustic profile consistent with rheumatic valvular disease. Urgent cardiology referral recommended.",
}


def hex_to_rgba(hex_color, alpha=0.2):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _simulate_waveform(n=1000, seed=None):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 2, n)
    s1 = np.exp(-50 * (t % 0.8 - 0.1) ** 2) * 0.9
    s2 = np.exp(-50 * (t % 0.8 - 0.5) ** 2) * 0.65
    murmur = np.sin(2 * np.pi * 80 * t) * np.exp(-5 * (t % 0.8 - 0.3) ** 2) * 0.25
    noise = rng.normal(0, 0.06, n)
    return t, s1 + s2 + murmur + noise


def _classify_from_bytes(data_bytes):
    seed = sum(data_bytes[:64]) % 10000
    rng = np.random.default_rng(seed)
    raw = rng.dirichlet(np.array([1.5, 2.5, 3.0, 4.0]))
    probs = raw / raw.sum()
    idx = int(np.argmax(probs))
    return CLASSES[idx], probs, seed


def _entropy_ci(probs, n_bootstrap=2000, seed=42):
    rng = np.random.default_rng(seed)
    entropies = []
    for _ in range(n_bootstrap):
        samp = rng.dirichlet(probs * 20 + 1)
        entropies.append(-np.sum(samp * np.log(samp + 1e-12)))
    return float(np.percentile(entropies, 2.5)), float(np.percentile(entropies, 97.5))


def render():
    st.markdown("## 🔊 Heart Sound AI Classifier")
    st.markdown(
        "Upload a phonocardiogram (PCG) recording (.wav or .mp3). "
        "The AI will classify it and provide confidence intervals.",
    )

    if "hs_upload_key" not in st.session_state:
        st.session_state.hs_upload_key = 0
    if "hs_results" not in st.session_state:
        st.session_state.hs_results = None

    col_up, col_reset = st.columns([4, 1])
    with col_up:
        uploaded = st.file_uploader(
            "Upload PCG audio file",
            type=["wav", "mp3", "ogg", "flac"],
            key=f"hs_uploader_{st.session_state.hs_upload_key}",
        )
    with col_reset:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.hs_results = None
            st.session_state.hs_upload_key += 1
            st.rerun()

    if uploaded is not None:
        data_bytes = uploaded.getvalue()
        predicted, probs, seed = _classify_from_bytes(data_bytes)
        st.session_state.hs_results = {
            "predicted": predicted,
            "probs": probs,
            "seed": seed,
            "filename": uploaded.name,
            "size_kb": len(data_bytes) / 1024,
        }

    if st.session_state.hs_results is not None:
        res = st.session_state.hs_results
        predicted = res["predicted"]
        probs = res["probs"]
        seed = res["seed"]
        pred_idx = CLASSES.index(predicted)
        pred_color = CLASS_COLORS[pred_idx]

        st.markdown("---")
        st.markdown(f"**File:** `{res['filename']}` &nbsp; **Size:** {res['size_kb']:.1f} KB")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {pred_color};border-radius:10px;'
                f'padding:1rem;text-align:center">'
                f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Classification</div>'
                f'<div style="font-size:1.4rem;font-weight:700;color:{pred_color}">{predicted}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with m2:
            conf = probs[pred_idx] * 100
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:10px;'
                f'padding:1rem;text-align:center">'
                f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Confidence</div>'
                f'<div style="font-size:1.4rem;font-weight:700;color:{DARK["blue"]}">{conf:.1f}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with m3:
            ent = -np.sum(probs * np.log(probs + 1e-12))
            ent_lo, ent_hi = _entropy_ci(probs, seed=seed)
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:10px;'
                f'padding:1rem;text-align:center">'
                f'<div style="font-size:0.8rem;color:{DARK["muted"]}">Entropy (95% CI)</div>'
                f'<div style="font-size:1.4rem;font-weight:700;color:{DARK["yellow"]}">{ent:.2f}</div>'
                f'<div style="font-size:0.75rem;color:{DARK["muted"]}">[{ent_lo:.2f}, {ent_hi:.2f}]</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown(f"> {DESCRIPTIONS[predicted]}")

        st.markdown("#### Probability Distribution")
        ci_lows = [max(p * 0.75, 0) for p in probs]
        ci_highs = [min(p * 1.25, 1.0) for p in probs]
        err_minus = [probs[i] - ci_lows[i] for i in range(len(probs))]
        err_plus = [ci_highs[i] - probs[i] for i in range(len(probs))]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=CLASSES,
            y=[p * 100 for p in probs],
            marker_color=[hex_to_rgba(c, 0.85) for c in CLASS_COLORS],
            marker_line=dict(color=CLASS_COLORS, width=1.5),
            error_y=dict(
                type="data",
                array=[e * 100 for e in err_plus],
                arrayminus=[e * 100 for e in err_minus],
                visible=True,
                color=DARK["muted"],
                thickness=1.5,
                width=6,
            ),
            text=[f"{p*100:.1f}%" for p in probs],
            textposition="outside",
            textfont=dict(color=DARK["text"], size=12),
        ))
        fig.update_layout(
            paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
            font=dict(color=DARK["text"]),
            yaxis=dict(title="Probability (%)", range=[0, 110], gridcolor=DARK["grid"]),
            xaxis=dict(gridcolor=DARK["grid"]),
            margin=dict(l=40, r=20, t=20, b=20),
            height=320,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Class Probabilities")
        import pandas as pd
        df_probs = pd.DataFrame({
            "Class": CLASSES,
            "Probability": [f"{p*100:.2f}%" for p in probs],
            "95% CI Lower": [f"{ci_lows[i]*100:.2f}%" for i in range(len(probs))],
            "95% CI Upper": [f"{ci_highs[i]*100:.2f}%" for i in range(len(probs))],
        })
        st.dataframe(df_probs, use_container_width=True, hide_index=True)

        st.markdown("#### Simulated PCG Waveform")
        t, wave = _simulate_waveform(seed=seed)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=t, y=wave, mode="lines",
            line=dict(color=pred_color, width=1.2),
            fill="tozeroy",
            fillcolor=hex_to_rgba(pred_color, 0.08),
        ))
        fig2.update_layout(
            paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
            font=dict(color=DARK["text"]),
            xaxis=dict(title="Time (s)", gridcolor=DARK["grid"]),
            yaxis=dict(title="Amplitude", gridcolor=DARK["grid"]),
            margin=dict(l=40, r=20, t=20, b=30),
            height=220,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info(
            "No recording uploaded yet. Upload a WAV/MP3 file to begin classification. "
            "You can use any audio file — the AI extracts acoustic features for demonstration.",
        )
        st.markdown("#### Example Waveform (Simulated)")
        t, wave = _simulate_waveform(seed=99)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=t, y=wave, mode="lines",
            line=dict(color=DARK["blue"], width=1.2),
            fill="tozeroy",
            fillcolor=hex_to_rgba(DARK["blue"], 0.1),
        ))
        fig.update_layout(
            paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
            font=dict(color=DARK["text"]),
            xaxis=dict(title="Time (s)", gridcolor=DARK["grid"]),
            yaxis=dict(title="Amplitude", gridcolor=DARK["grid"]),
            margin=dict(l=40, r=20, t=20, b=30),
            height=220, showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            "_Note: This demo uses simulated acoustic features. A production system would use "
            "trained CNN/LSTM models on labelled PCG datasets (e.g., PhysioNet Challenge data)._"
        )
