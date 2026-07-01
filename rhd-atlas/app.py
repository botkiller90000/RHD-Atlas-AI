import streamlit as st

st.set_page_config(
    page_title="RHD Atlas AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #21262d;
}
.stRadio > label { color: #e6edf3; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #8b949e; font-size: 0.85rem; }
div[data-baseweb="radio"] label {
    color: #e6edf3 !important;
    padding: 0.35rem 0;
}
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.markdown(
        '<div style="font-size:1.3rem;font-weight:800;color:#58a6ff;margin-bottom:0.2rem">🫀 RHD Atlas AI</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:0.75rem;color:#8b949e;margin-bottom:1rem">Africa Public Health Atlas</div>',
        unsafe_allow_html=True,
    )

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem;color:#8b949e;margin-bottom:0.4rem">NAVIGATION</div>', unsafe_allow_html=True)

    nav_options = [
        "🗺️ Atlas",
        "🔊 Heart Sound AI",
        "⚕️ Risk Calculator",
        "📚 Education",
        "🔬 Research",
        "🛣️ Roadmap",
    ]
    nav_map = {
        "🗺️ Atlas": "Atlas",
        "🔊 Heart Sound AI": "Heart Sound AI",
        "⚕️ Risk Calculator": "Risk Calculator",
        "📚 Education": "Education",
        "🔬 Research": "Research",
        "🛣️ Roadmap": "Roadmap",
    }

    current_nav = None
    for k, v in nav_map.items():
        if st.session_state.page == v:
            current_nav = k
            break

    radio_idx = nav_options.index(current_nav) if current_nav else None

    selected = st.radio(
        "Pages",
        nav_options,
        index=radio_idx,
        label_visibility="collapsed",
    )

    if selected is not None and nav_map[selected] != st.session_state.page:
        st.session_state.page = nav_map[selected]
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.72rem;color:#8b949e;line-height:1.5">'
        'Data: GBD 2019 · WHO AFRO · World Bank<br>'
        'Built with Streamlit &amp; Plotly'
        '</div>',
        unsafe_allow_html=True,
    )

page = st.session_state.page

if page == "Home":
    from pages.home import render
    render()
elif page == "Atlas":
    from pages.atlas import render
    render()
elif page == "Heart Sound AI":
    from pages.heart_sound import render
    render()
elif page == "Risk Calculator":
    from pages.risk_calculator import render
    render()
elif page == "Education":
    from pages.education import render
    render()
elif page == "Research":
    from pages.research import render
    render()
elif page == "Roadmap":
    from pages.roadmap import render
    render()
