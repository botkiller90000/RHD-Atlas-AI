import streamlit as st
import pandas as pd

DARK = {
    "paper": "#0d1117", "plot": "#161b22", "grid": "#21262d",
    "text": "#e6edf3", "muted": "#8b949e", "accent": "#f85149",
    "blue": "#58a6ff", "green": "#3fb950", "yellow": "#e3b341",
}

# ── Literature Database ──────────────────────────────────────────────────────
LITERATURE = [
    {
        "id": 1,
        "authors": "GBD 2019 Diseases and Injuries Collaborators",
        "year": 2020,
        "title": "Global burden of 369 diseases and injuries in 204 countries and territories, 1990–2019: a systematic analysis for the Global Burden of Disease Study 2019",
        "journal": "The Lancet",
        "volume": "396(10258):1204–1222",
        "doi": "10.1016/S0140-6736(20)30925-9",
        "category": "Epidemiology",
        "tags": ["GBD", "Africa", "Burden", "DALYs"],
        "relevance": "Primary epidemiological data source for RHD burden estimates used throughout this atlas.",
    },
    {
        "id": 2,
        "authors": "Watkins DA, Johnson CO, Colquhoun SM, et al.",
        "year": 2017,
        "title": "Global, Regional, and National Burden of Rheumatic Heart Disease, 1990–2015",
        "journal": "New England Journal of Medicine",
        "volume": "377(8):713–722",
        "doi": "10.1056/NEJMoa1603693",
        "category": "Epidemiology",
        "tags": ["RHD", "Global Burden", "Prevalence", "Mortality"],
        "relevance": "Landmark study quantifying RHD burden globally. Foundation for sub-regional prevalence estimates.",
    },
    {
        "id": 3,
        "authors": "Zühlke L, Engel ME, Karthikeyan G, et al.",
        "year": 2015,
        "title": "Characteristics, complications, and gaps in evidence-based interventions in rheumatic heart disease: the Global Rheumatic Heart Disease Registry (the REMEDY study)",
        "journal": "European Heart Journal",
        "volume": "36(18):1115–1122",
        "doi": "10.1093/eurheartj/ehu449",
        "category": "Clinical",
        "tags": ["Registry", "Complications", "Africa", "Clinical"],
        "relevance": "Pan-African registry data on RHD complications, clinical presentation, and treatment gaps.",
    },
    {
        "id": 4,
        "authors": "Carapetis JR, Steer AC, Mulholland EK, Weber M",
        "year": 2005,
        "title": "The global burden of group A streptococcal diseases",
        "journal": "The Lancet Infectious Diseases",
        "volume": "5(11):685–694",
        "doi": "10.1016/S1473-3099(05)70267-X",
        "category": "Epidemiology",
        "tags": ["GAS", "Streptococcus", "Global Burden", "ARF"],
        "relevance": "Definitive study on the global burden of GAS diseases, the causative pathway for RHD.",
    },
    {
        "id": 5,
        "authors": "Beaton A, Okello E, Lwabi P, et al.",
        "year": 2012,
        "title": "Echocardiography screening for rheumatic heart disease in Ugandan schoolchildren",
        "journal": "Circulation",
        "volume": "125(25):3127–3132",
        "doi": "10.1161/CIRCULATIONAHA.112.092312",
        "category": "Screening",
        "tags": ["Echocardiography", "Screening", "Uganda", "Children"],
        "relevance": "Key study demonstrating the feasibility and yield of school-based echo screening in Africa.",
    },
    {
        "id": 6,
        "authors": "Manyemba J, Mayosi BM",
        "year": 2002,
        "title": "Penicillin for secondary prevention of rheumatic fever",
        "journal": "Cochrane Database of Systematic Reviews",
        "volume": "Issue 3: CD002227",
        "doi": "10.1002/14651858.CD002227",
        "category": "Prevention",
        "tags": ["Penicillin", "Secondary Prevention", "Prophylaxis", "ARF"],
        "relevance": "Cochrane review confirming efficacy of penicillin for secondary prophylaxis — cornerstone of prevention strategy.",
    },
    {
        "id": 7,
        "authors": "Nkomo VT",
        "year": 2007,
        "title": "Epidemiology and prevention of valvular heart diseases and infective endocarditis in Africa",
        "journal": "Heart",
        "volume": "93(12):1510–1519",
        "doi": "10.1136/hrt.2006.098954",
        "category": "Epidemiology",
        "tags": ["Valvular Disease", "Africa", "Prevention", "Endocarditis"],
        "relevance": "Comprehensive review of valvular heart disease epidemiology and prevention in Africa.",
    },
    {
        "id": 8,
        "authors": "Wilkins GT, Weyman AE, Abascal VM, et al.",
        "year": 1988,
        "title": "Percutaneous balloon dilatation of the mitral valve: an analysis of echocardiographic variables related to outcome and the mechanism of dilatation",
        "journal": "British Heart Journal",
        "volume": "60(4):299–308",
        "doi": "10.1136/hrt.60.4.299",
        "category": "Clinical",
        "tags": ["Wilkins Score", "PBMV", "Mitral Stenosis", "Echocardiography"],
        "relevance": "Original description of the Wilkins Score — the standard tool for PBMV patient selection in rheumatic MS.",
    },
    {
        "id": 9,
        "authors": "WHO Expert Consultation",
        "year": 2004,
        "title": "Rheumatic fever and rheumatic heart disease: report of a WHO Expert Consultation",
        "journal": "WHO Technical Report Series",
        "volume": "923",
        "doi": "",
        "category": "Guidelines",
        "tags": ["WHO", "Guidelines", "RHD", "ARF"],
        "relevance": "WHO guidelines on RHD diagnosis, treatment, and prevention. Foundation for clinical practice in Africa.",
    },
    {
        "id": 10,
        "authors": "RHD Action",
        "year": 2023,
        "title": "RHD Action — Prioritising Rheumatic Heart Disease: A Policy Brief",
        "journal": "RHD Action / World Heart Federation",
        "volume": "",
        "doi": "",
        "category": "Policy",
        "tags": ["Policy", "Africa", "WHO", "Elimination"],
        "relevance": "Policy framework and advocacy materials for RHD elimination programmes in Africa.",
    },
    {
        "id": 11,
        "authors": "Sliwa K, Zühlke L, Kasper P, et al.",
        "year": 2020,
        "title": "Current state of knowledge on aetiology, diagnosis, management, and therapy of peripartum cardiomyopathy: a position statement from the Heart Failure Association of the European Society of Cardiology Working Group on peripartum cardiomyopathy",
        "journal": "European Journal of Heart Failure",
        "volume": "22(8):1–25",
        "doi": "10.1002/ejhf.1890",
        "category": "Maternal Health",
        "tags": ["Maternal", "Pregnancy", "Heart Failure", "Africa"],
        "relevance": "Context for maternal cardiovascular risk in Africa — intersection with RHD burden in young women.",
    },
    {
        "id": 12,
        "authors": "Marijon E, Mirabel M, Celermajer DS, Jouven X",
        "year": 2012,
        "title": "Rheumatic heart disease",
        "journal": "The Lancet",
        "volume": "379(9819):953–964",
        "doi": "10.1016/S0140-6736(11)61171-9",
        "category": "Review",
        "tags": ["Review", "RHD", "Global", "Clinical"],
        "relevance": "Comprehensive Lancet review on RHD — epidemiology, pathophysiology, diagnosis, and management.",
    },
]

CATEGORIES = ["All"] + sorted(set(r["category"] for r in LITERATURE))
ALL_TAGS = sorted(set(tag for r in LITERATURE for tag in r["tags"]))

# ── Data Sources ─────────────────────────────────────────────────────────────
DATA_SOURCES = [
    {
        "name": "IHME Global Burden of Disease Study 2019",
        "org": "Institute for Health Metrics and Evaluation",
        "url": "https://www.healthdata.org/gbd",
        "indicators": ["RHD Prevalence", "RHD Incidence", "RHD Mortality", "DALYs", "YLDs", "YLLs"],
        "coverage": "54 African countries / sub-regions, 1990–2019",
        "format": "Sub-regional estimates by age, sex, and year",
        "access": "Open",
        "color": DARK["blue"],
    },
    {
        "name": "WHO Global Health Observatory",
        "org": "World Health Organization",
        "url": "https://www.who.int/data/gho",
        "indicators": ["Maternal Mortality Ratio", "Physician Density", "Hospital Bed Density"],
        "coverage": "47 African countries, 2000–2019",
        "format": "Country-level, sparse time series",
        "access": "Open",
        "color": DARK["green"],
    },
    {
        "name": "World Development Indicators",
        "org": "World Bank Group",
        "url": "https://databank.worldbank.org/source/world-development-indicators",
        "indicators": ["GDP per Capita", "Health Expenditure (% GDP)", "Rural Population %", 
                       "Female Population %", "GDP PPP"],
        "coverage": "51 African countries, 2000–2016",
        "format": "Country-year panel data",
        "access": "Open",
        "color": DARK["yellow"],
    },
    {
        "name": "PhysioNet Heart Sound Databases",
        "org": "MIT-BIH / PhysioNet",
        "url": "https://physionet.org/",
        "indicators": ["PCG Recordings", "Heart Sound Labels", "Clinical Metadata"],
        "coverage": "Multiple international datasets, 2016 Challenge",
        "format": "WAV audio files with annotations",
        "access": "Open (credentialed access for some datasets)",
        "color": DARK["accent"],
    },
]


def render():
    st.markdown("## 🔬 Research Repository")
    st.markdown(
        "Curated collection of peer-reviewed literature, data sources, and research methodology "
        "underpinning the RHD Atlas AI platform."
    )

    tab_lit, tab_data, tab_methodology = st.tabs(["📄 Literature", "🗄️ Data Sources", "🔭 Methodology"])

    # ── Literature Tab ───────────────────────────────────────────────────────
    with tab_lit:
        st.markdown("### Peer-Reviewed Literature")
        st.markdown(f"*{len(LITERATURE)} curated references — systematic review priority: 2000–2024*")

        # Filters
        fc1, fc2, fc3 = st.columns([2, 2, 3])
        with fc1:
            cat_filter = st.selectbox("Category", CATEGORIES, index=0)
        with fc2:
            tag_filter = st.selectbox("Tag", ["All Tags"] + ALL_TAGS)
        with fc3:
            search_query = st.text_input("Search title / authors", placeholder="e.g. echocardiography, Uganda…")

        # Apply filters
        filtered = LITERATURE
        if cat_filter != "All":
            filtered = [r for r in filtered if r["category"] == cat_filter]
        if tag_filter != "All Tags":
            filtered = [r for r in filtered if tag_filter in r["tags"]]
        if search_query:
            q = search_query.lower()
            filtered = [r for r in filtered if q in r["title"].lower() or q in r["authors"].lower()]

        st.markdown(f"*Showing {len(filtered)} of {len(LITERATURE)} references*")
        st.markdown("---")

        for ref in filtered:
            _render_reference(ref)

    # ── Data Sources Tab ─────────────────────────────────────────────────────
    with tab_data:
        st.markdown("### Data Sources")
        st.markdown(
            "All data used in this atlas originates from internationally recognized open-access repositories. "
            "Extensive preprocessing, standardisation, and harmonisation was applied to create a unified analytical framework."
        )

        for ds in DATA_SOURCES:
            _render_data_source(ds)

        st.markdown("---")
        st.markdown("#### Data Pipeline Overview")
        pipeline_steps = [
            ("1. Raw Data Acquisition", "Download raw CSV/Excel datasets from IHME, WHO, and World Bank portals.", DARK["blue"]),
            ("2. Data Audit", "Assess shape, dtypes, null rates, duplicate rows, and value ranges for each dataset.", DARK["blue"]),
            ("3. Standardisation", "Normalise country names using ISO 3166-1 codes and a custom COUNTRY_MAPPING dictionary. Standardise column names and units.", DARK["yellow"]),
            ("4. Africa Filtering", "Filter to 54 African countries using the African Union country list. Remove non-African regional aggregates.", DARK["yellow"]),
            ("5. Wide-to-Long Reshaping", "Melt World Bank wide-format data to long format (country × year × indicator).", DARK["green"]),
            ("6. Derived Metrics", "Compute composite indicators: Healthcare Capacity Score, Infrastructure Risk Index, Economic Risk Score.", DARK["green"]),
            ("7. Unified Merge", "Join GBD, WHO, and World Bank datasets on country × ISO3 × year for combined analysis.", DARK["accent"]),
        ]
        for step, desc, color in pipeline_steps:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border-left:3px solid {color};border-radius:4px;'
                f'padding:0.6rem 1rem;margin:0.35rem 0">'
                f'<div style="color:{color};font-weight:700;font-size:0.9rem">{step}</div>'
                f'<div style="color:{DARK["text"]};font-size:0.84rem;margin-top:0.2rem">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Methodology Tab ──────────────────────────────────────────────────────
    with tab_methodology:
        st.markdown("### Research Methodology")

        st.markdown("#### Study Design")
        st.markdown("""
        This project used a **research-first methodology** — extensive literature review and epidemiological 
        analysis preceded any AI model development. All platform components are grounded in published evidence.
        """)

        st.markdown("#### Literature Review Protocol")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Inclusion Criteria**")
            inclusion = [
                "Published 2000–2026",
                "Peer-reviewed journal articles",
                "Focus on RHD, ARF, or rheumatic fever",
                "African populations or global studies with Africa data",
                "Epidemiological analysis, clinical outcomes, or intervention data",
                "English language publications",
            ]
            for item in inclusion:
                st.markdown(f'<span style="color:{DARK["green"]}">✓ {item}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown("**Exclusion Criteria**")
            exclusion = [
                "Degenerative valvular disease (non-rheumatic)",
                "Isolated case reports",
                "Narrative review articles without systematic methods",
                "Experimental interventions without epidemiological data",
                "Studies focused exclusively on non-African populations",
            ]
            for item in exclusion:
                st.markdown(f'<span style="color:{DARK["accent"]}">✗ {item}</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Research Questions Framework")
        questions = [
            ("RQ1", "How large is the burden of Rheumatic Heart Disease across Africa?", 
             "Answered by GBD data: prevalence, incidence, mortality, DALYs by sub-region, sex, age, year."),
            ("RQ2", "Which demographic, socioeconomic, and healthcare factors are associated with increased disease burden?",
             "Answered by merged WHO + World Bank analysis: physician density, health expenditure, GDP, rural population."),
            ("RQ3", "How can artificial intelligence improve accessibility to screening, education, and public health decision support?",
             "Addressed by Heart Sound AI classifier and Risk Calculator modules. Future: mobile deployment, community health worker tools."),
        ]
        for rq, question, answer in questions:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:8px;'
                f'padding:0.9rem 1rem;margin:0.5rem 0">'
                f'<div style="color:{DARK["blue"]};font-weight:700;font-size:0.85rem;margin-bottom:0.3rem">{rq}</div>'
                f'<div style="color:{DARK["text"]};font-weight:600;margin-bottom:0.3rem;font-size:0.9rem">{question}</div>'
                f'<div style="color:{DARK["muted"]};font-size:0.83rem">{answer}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### Technical Stack")
        tech = [
            ("Python 3.11", "Primary programming language", DARK["blue"]),
            ("Streamlit", "Interactive web application framework", DARK["blue"]),
            ("Pandas & NumPy", "Data processing and numerical computation", DARK["yellow"]),
            ("Plotly", "Interactive visualisation library", DARK["green"]),
            ("Scikit-learn", "Machine learning models (Random Forest, SVM)", DARK["accent"]),
            ("Kaggle Notebooks", "Initial EDA and preprocessing pipelines", DARK["muted"]),
            ("Git / GitHub", "Version control and collaboration", DARK["muted"]),
        ]
        for tool, desc, color in tech:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:6px;'
                f'padding:0.5rem 0.9rem;margin:0.3rem 0;display:flex;justify-content:space-between">'
                f'<span style="color:{color};font-weight:600;font-size:0.88rem">{tool}</span>'
                f'<span style="color:{DARK["muted"]};font-size:0.83rem">{desc}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### Limitations")
        st.markdown("""
        - **Simulated sub-regional data:** GBD estimates are regional aggregates; country-level estimates 
          for RHD remain a critical data gap. The platform uses modelled sub-regional estimates.
        - **AI model scope:** The heart sound classifier uses simulated acoustic features for demonstration. 
          Production deployment requires trained models on validated African PCG datasets.
        - **Cross-sectional WHO data:** WHO healthcare indicators have limited temporal coverage, reducing 
          power for longitudinal analysis.
        - **Educational use only:** Risk calculator and AI tools are for research and education — 
          not clinical diagnosis or treatment decisions.
        - **Selection bias:** Literature review may under-represent grey literature and non-English publications.
        """)

        st.markdown("---")
        st.markdown("#### Project Repository")
        st.markdown(
            '<div style="background:#161b22;border:1px solid #21262d;border-radius:8px;padding:1rem">'
            '<div style="color:#e6edf3;font-weight:600">🔗 GitHub Repository</div>'
            '<a href="https://github.com/botkiller90000/RHD-Atlas-AI" style="color:#58a6ff">'
            'github.com/botkiller90000/RHD-Atlas-AI</a>'
            '<div style="color:#8b949e;font-size:0.82rem;margin-top:0.4rem">'
            'Complete source code · Cleaned datasets · Preprocessing pipelines · Documentation · Project roadmap'
            '</div></div>',
            unsafe_allow_html=True,
        )


def _render_reference(ref):
    tags_html = "".join([
        f'<span style="background:{DARK["grid"]};border-radius:4px;padding:0.15rem 0.5rem;'
        f'font-size:0.72rem;color:{DARK["muted"]};margin-right:0.3rem">{t}</span>'
        for t in ref["tags"]
    ])
    doi_html = ""
    if ref.get("doi"):
        doi_html = f'<a href="https://doi.org/{ref["doi"]}" style="color:{DARK["blue"]};font-size:0.78rem">DOI: {ref["doi"]}</a>'
    st.markdown(
        f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:8px;'
        f'padding:0.9rem 1rem;margin:0.45rem 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div style="font-size:0.78rem;color:{DARK["muted"]}">[{ref["id"]}] {ref["authors"]} ({ref["year"]})</div>'
        f'<span style="background:{DARK["grid"]};border-radius:4px;padding:0.1rem 0.45rem;'
        f'font-size:0.7rem;color:{DARK["blue"]};white-space:nowrap;margin-left:0.5rem">{ref["category"]}</span>'
        f'</div>'
        f'<div style="color:{DARK["text"]};font-weight:600;margin:0.3rem 0;font-size:0.9rem">{ref["title"]}</div>'
        f'<div style="color:{DARK["muted"]};font-size:0.82rem;font-style:italic">'
        f'{ref["journal"]}{"  " + ref["volume"] if ref["volume"] else ""}</div>'
        f'<div style="margin-top:0.4rem">{tags_html}</div>'
        f'<div style="margin-top:0.35rem;color:{DARK["text"]};font-size:0.82rem;border-left:2px solid {DARK["grid"]};'
        f'padding-left:0.6rem;margin-left:0.2rem">{ref["relevance"]}</div>'
        f'<div style="margin-top:0.3rem">{doi_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_data_source(ds):
    indicators_html = " · ".join([
        f'<span style="color:{DARK["text"]}">{i}</span>' for i in ds["indicators"]
    ])
    url_html = f'<a href="{ds["url"]}" style="color:{DARK["blue"]};font-size:0.8rem">{ds["url"]}</a>' if ds["url"] else ""
    st.markdown(
        f'<div style="background:{DARK["plot"]};border:1px solid {ds["color"]};border-radius:10px;'
        f'padding:1rem 1.2rem;margin:0.6rem 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem">'
        f'<div style="color:{ds["color"]};font-weight:700;font-size:0.95rem">{ds["name"]}</div>'
        f'<span style="color:{DARK["green"]};font-size:0.75rem;background:{DARK["grid"]};'
        f'padding:0.15rem 0.5rem;border-radius:4px">{ds["access"]}</span>'
        f'</div>'
        f'<div style="color:{DARK["muted"]};font-size:0.82rem;margin-bottom:0.4rem">{ds["org"]}</div>'
        f'<div style="font-size:0.83rem;color:{DARK["muted"]};margin-bottom:0.3rem">'
        f'<b style="color:{DARK["text"]}">Indicators:</b> {indicators_html}</div>'
        f'<div style="font-size:0.82rem;color:{DARK["muted"]}">'
        f'<b style="color:{DARK["text"]}">Coverage:</b> {ds["coverage"]} &nbsp;·&nbsp; '
        f'<b style="color:{DARK["text"]}">Format:</b> {ds["format"]}</div>'
        f'<div style="margin-top:0.4rem">{url_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
