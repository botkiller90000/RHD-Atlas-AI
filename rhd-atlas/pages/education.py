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


def _card(title, body, color=None, icon=""):
    color = color or DARK["blue"]
    st.markdown(
        f'<div style="background:{DARK["plot"]};border-left:4px solid {color};border-radius:8px;'
        f'padding:1rem 1.2rem;margin:0.6rem 0">'
        f'<div style="font-size:1rem;font-weight:700;color:{color};margin-bottom:0.4rem">{icon} {title}</div>'
        f'<div style="font-size:0.88rem;color:{DARK["text"]};line-height:1.6">{body}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render():
    st.markdown("## 📚 RHD Education Hub")
    st.markdown(
        "Accessible educational content on Rheumatic Heart Disease — from basic biology to "
        "public health intervention strategies. Designed for patients, students, and community health workers."
    )

    topics = [
        "🦠 What is Rheumatic Heart Disease?",
        "🤒 Rheumatic Fever",
        "❤️ Mitral Valve Stenosis",
        "📈 Disease Progression",
        "💊 Prevention Strategies",
        "🌍 Public Health & Policy",
        "🤰 Women & Maternal Risk",
        "🩺 Diagnosis & Screening",
    ]

    selected_topic = st.selectbox("Select Topic", topics, index=0)

    st.markdown("---")

    if selected_topic == topics[0]:
        _topic_what_is_rhd()
    elif selected_topic == topics[1]:
        _topic_rheumatic_fever()
    elif selected_topic == topics[2]:
        _topic_mitral_stenosis()
    elif selected_topic == topics[3]:
        _topic_progression()
    elif selected_topic == topics[4]:
        _topic_prevention()
    elif selected_topic == topics[5]:
        _topic_public_health()
    elif selected_topic == topics[6]:
        _topic_women()
    elif selected_topic == topics[7]:
        _topic_diagnosis()

    st.markdown("---")
    st.markdown(
        '<div style="background:#161b22;border:1px solid #21262d;border-radius:8px;padding:1rem;text-align:center">'
        '<div style="color:#8b949e;font-size:0.8rem">📺 Learn more on the Good Glance YouTube channel — '
        'Science, Biology & Diseases explained simply for everyone</div>'
        '<a href="https://www.youtube.com/@GGsciences" style="color:#58a6ff;font-size:0.85rem">'
        'youtube.com/@GGsciences</a></div>',
        unsafe_allow_html=True,
    )
    st.caption("⚠️ This educational content is for general awareness only and does not constitute medical advice.")


# ── Topic pages ─────────────────────────────────────────────────────────────

def _topic_what_is_rhd():
    st.markdown("### 🦠 What is Rheumatic Heart Disease?")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        **Rheumatic Heart Disease (RHD)** is a chronic heart condition caused by damage to the 
        heart valves — most commonly the mitral valve — as a result of recurrent episodes of 
        **acute rheumatic fever (ARF)**.

        RHD is caused by Group A *Streptococcus* (GAS) bacteria, the same bacteria responsible 
        for strep throat. When strep throat is left untreated or inadequately treated, the immune 
        system can mistakenly attack the heart's own tissue — a process called **molecular mimicry**.

        **Key facts:**
        - Affects an estimated **39 million people** worldwide
        - Responsible for **~300,000 deaths** per year globally
        - The **leading cause of acquired heart disease** in children and young adults in Africa
        - Entirely **preventable** with timely antibiotic treatment
        - Predominantly affects people in **low- and middle-income countries**
        """)
    with col2:
        # Simple prevalence comparison chart
        regions = ["Eastern SSA", "Western SSA", "Central SSA", "Southern SSA", "North Africa"]
        prevalence = [1050, 880, 950, 650, 420]
        colors = ["#3fb950", "#58a6ff", "#58a6ff", "#e3b341", "#c084fc"]
        fig = go.Figure(go.Bar(
            x=prevalence, y=regions, orientation="h",
            marker_color=colors,
            text=[f"{v}/100k" for v in prevalence],
            textposition="outside",
            textfont=dict(color=DARK["text"], size=10),
        ))
        fig.update_layout(
            paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
            font=dict(color=DARK["text"]),
            title=dict(text="RHD Prevalence by Region", font=dict(size=12, color=DARK["muted"])),
            xaxis=dict(title="per 100,000", gridcolor=DARK["grid"]),
            yaxis=dict(gridcolor=DARK["grid"]),
            margin=dict(l=10, r=40, t=35, b=30),
            height=260,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    _card("The Core Problem", 
          "A simple sore throat (strep throat), easily cured with a single course of penicillin, "
          "can silently damage the heart over repeated episodes — causing irreversible valve scarring "
          "that leads to heart failure, stroke, and premature death.",
          DARK["accent"], "⚠️")

    _card("Who is Most Affected?",
          "Children aged 5–14 are most susceptible to strep infections and initial rheumatic fever. "
          "Women aged 15–35 carry the highest RHD burden, worsened by cardiovascular strain of pregnancy. "
          "Communities in poverty face heightened risk due to overcrowding and limited healthcare access.",
          DARK["blue"], "👥")


def _topic_rheumatic_fever():
    st.markdown("### 🤒 Acute Rheumatic Fever (ARF)")
    st.markdown("""
    **Acute Rheumatic Fever (ARF)** is an inflammatory disease that occurs 2–4 weeks after an 
    untreated or inadequately treated Group A Streptococcal (GAS) throat infection.
    """)

    st.markdown("#### The Disease Chain")
    steps = [
        ("Step 1", "GAS Infection", "Group A Streptococcus bacteria cause strep throat (pharyngitis). "
         "In crowded, low-resource settings, strep throat is endemic.", DARK["blue"]),
        ("Step 2", "Immune Response", "The body mounts an immune response against GAS antigens. "
         "Due to molecular mimicry, antibodies cross-react with heart, joint, brain, and skin tissue.", DARK["yellow"]),
        ("Step 3", "Acute Rheumatic Fever", "2–4 weeks post-infection: fever, painful migratory arthritis, "
         "characteristic skin lesions (erythema marginatum), Sydenham's chorea, and carditis.", DARK["accent"]),
        ("Step 4", "Carditis", "Inflammation of the heart (pancarditis) — endocarditis, myocarditis, "
         "pericarditis. Valve leaflets become swollen and scarred.", DARK["accent"]),
        ("Step 5", "Repeated Episodes", "Each subsequent strep infection causes further valve damage. "
         "Risk of permanent damage increases dramatically with each ARF episode.", "#ff4444"),
        ("Step 6", "Rheumatic Heart Disease", "Chronic, irreversible scarring and fibrosis of heart valves. "
         "Leads to stenosis (narrowing) or regurgitation (leaking) — ultimately heart failure.", "#ff4444"),
    ]
    for step_num, title, desc, color in steps:
        st.markdown(
            f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:8px;'
            f'padding:0.8rem 1rem;margin:0.4rem 0;display:flex;align-items:flex-start;gap:1rem">'
            f'<div style="min-width:60px;background:{color};border-radius:6px;padding:0.3rem 0.5rem;'
            f'font-size:0.7rem;font-weight:700;color:#0d1117;text-align:center">{step_num}</div>'
            f'<div><div style="font-weight:600;color:{color};margin-bottom:0.2rem">{title}</div>'
            f'<div style="font-size:0.85rem;color:{DARK["text"]}">{desc}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Jones Criteria (Diagnosis)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Major Criteria**")
        major = ["Carditis (clinical or subclinical)", "Polyarthritis", "Chorea (Sydenham's)", 
                 "Erythema marginatum", "Subcutaneous nodules"]
        for m in major:
            st.markdown(f'<span style="color:{DARK["accent"]}">● {m}</span>', unsafe_allow_html=True)
    with col2:
        st.markdown("**Minor Criteria**")
        minor = ["Fever", "Elevated inflammatory markers (ESR/CRP)", "Prolonged PR interval on ECG",
                 "Arthralgia (if arthritis not a major criterion)", "Prior episode of ARF"]
        for m in minor:
            st.markdown(f'<span style="color:{DARK["yellow"]}">● {m}</span>', unsafe_allow_html=True)

    st.markdown(
        "*Diagnosis requires: 2 major criteria, OR 1 major + 2 minor criteria, "
        "plus evidence of preceding GAS infection.*"
    )


def _topic_mitral_stenosis():
    st.markdown("### ❤️ Rheumatic Mitral Valve Stenosis")
    st.markdown("""
    The **mitral valve** separates the left atrium from the left ventricle. In rheumatic heart disease, 
    repeated inflammation causes the valve leaflets to thicken, fuse, and calcify — progressively 
    narrowing the valve opening. This obstruction is called **mitral stenosis (MS)**.
    """)

    _card("Normal Mitral Valve Area", 
          "Normal valve area: 4–6 cm². Symptoms typically develop when area falls below 1.5 cm² (severe stenosis). "
          "The valve opening progressively narrows over years of cumulative rheumatic damage.",
          DARK["green"], "📐")

    st.markdown("#### Severity Classification")
    severity_data = [
        ("Mild", "> 1.5 cm²", "Usually asymptomatic", DARK["green"]),
        ("Moderate", "1.0–1.5 cm²", "Exertional dyspnoea, palpitations", DARK["yellow"]),
        ("Severe", "< 1.0 cm²", "Dyspnoea at rest, pulmonary oedema, atrial fibrillation", DARK["accent"]),
        ("Critical", "< 0.6 cm²", "Severe heart failure, high mortality risk without intervention", "#ff4444"),
    ]
    cols = st.columns(4)
    for col, (level, area, symptoms, color) in zip(cols, severity_data):
        with col:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:2px solid {color};border-radius:10px;'
                f'padding:0.8rem;text-align:center;height:140px">'
                f'<div style="color:{color};font-weight:700;font-size:0.9rem">{level}</div>'
                f'<div style="color:{DARK["blue"]};font-size:1rem;font-weight:700;margin:0.3rem 0">{area}</div>'
                f'<div style="color:{DARK["muted"]};font-size:0.75rem">{symptoms}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("#### Key Complications")
    complications = [
        ("Atrial Fibrillation", "Irregular heart rhythm occurs in up to 40% of severe MS. "
         "Increases stroke risk 5-fold. A common trigger for acute decompensation.", DARK["accent"]),
        ("Pulmonary Hypertension", "Chronic back-pressure causes elevated pulmonary artery pressure, "
         "right heart failure, and reduced exercise tolerance.", DARK["yellow"]),
        ("Thromboembolic Stroke", "Blood clots form in the dilated left atrium, particularly during AF. "
         "A leading cause of mortality and disability in young African women with RHD.", DARK["accent"]),
        ("Heart Failure", "Progressive valve dysfunction leads to left and right heart failure. "
         "Without surgical intervention, severe MS carries high 10-year mortality.", "#ff4444"),
    ]
    for title, desc, color in complications:
        _card(title, desc, color)

    st.markdown("#### Treatment Options")
    tx_data = [
        ("Medical Management", DARK["blue"], ["Diuretics for fluid overload", "Rate control for AF (beta-blockers, digoxin)", 
                                               "Anticoagulation to prevent stroke", "Penicillin prophylaxis to prevent recurrent ARF"]),
        ("Percutaneous Balloon Mitral Valvotomy (PBMV)", DARK["green"], ["Catheter-based procedure — balloon inflated across mitral valve", 
                                                                           "Suitable for Wilkins Score ≤8", 
                                                                           "Avoids open-heart surgery", "Preferred in resource-limited settings"]),
        ("Surgical Intervention", DARK["yellow"], ["Mitral valve repair (commissurotomy)", 
                                                     "Mitral valve replacement (mechanical or bioprosthetic)", 
                                                     "Required for Wilkins Score ≥12 or failed PBMV", 
                                                     "Lifelong anticoagulation needed with mechanical valve"]),
    ]
    tx_cols = st.columns(3)
    for col, (title, color, items) in zip(tx_cols, tx_data):
        with col:
            items_html = "".join([f'<li style="margin:0.3rem 0;font-size:0.82rem;color:{DARK["text"]}">{i}</li>' for i in items])
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {color};border-radius:8px;padding:0.8rem">'
                f'<div style="color:{color};font-weight:700;margin-bottom:0.5rem;font-size:0.9rem">{title}</div>'
                f'<ul style="margin:0;padding-left:1rem">{items_html}</ul></div>',
                unsafe_allow_html=True,
            )


def _topic_progression():
    st.markdown("### 📈 Disease Progression")
    st.markdown("""
    RHD progresses silently over years to decades. The rate of progression depends on the number of 
    ARF recurrences, patient age, and access to secondary prophylaxis.
    """)

    # Timeline visualisation
    years = [0, 2, 5, 10, 15, 20, 25]
    severity = [0, 5, 20, 45, 65, 80, 90]
    no_prophylaxis = [0, 8, 30, 60, 78, 88, 95]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=severity, mode="lines+markers", name="With Prophylaxis",
        line=dict(color=DARK["green"], width=2.5),
        marker=dict(size=7),
        fill="tozeroy", fillcolor=hex_to_rgba(DARK["green"], 0.08),
    ))
    fig.add_trace(go.Scatter(
        x=years, y=no_prophylaxis, mode="lines+markers", name="Without Prophylaxis",
        line=dict(color=DARK["accent"], width=2.5),
        marker=dict(size=7),
        fill="tozeroy", fillcolor=hex_to_rgba(DARK["accent"], 0.08),
    ))
    for threshold, label in [(20, "Moderate"), (50, "Severe"), (80, "Critical")]:
        fig.add_hline(y=threshold, line_dash="dash", line_color=DARK["grid"],
                      annotation_text=label, annotation_position="right",
                      annotation_font_color=DARK["muted"])
    fig.update_layout(
        paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
        font=dict(color=DARK["text"]),
        title=dict(text="Disease Severity Progression (Illustrative)", font=dict(size=13, color=DARK["muted"])),
        xaxis=dict(title="Years from First ARF Episode", gridcolor=DARK["grid"]),
        yaxis=dict(title="Disease Severity Score", range=[0, 100], gridcolor=DARK["grid"]),
        legend=dict(bgcolor=DARK["plot"]),
        margin=dict(l=50, r=80, t=40, b=40),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

    _card("Without Secondary Prophylaxis",
          "Each strep reinfection causes further valve damage. Roughly 70% of untreated patients "
          "with moderate RHD progress to severe disease within 10 years. In Africa, ~70% of affected "
          "individuals die by age 25 without adequate treatment.",
          DARK["accent"], "⚠️")

    _card("With Secondary Prophylaxis",
          "Monthly benzathine penicillin G (BPG) injections prevent recurrent GAS infections. "
          "Halts or significantly slows valve disease progression. Most effective when started "
          "early — before significant valve damage has occurred.",
          DARK["green"], "✅")

    st.markdown("#### Key Mortality Statistics — Africa")
    stat_cols = st.columns(3)
    for col, (stat, label, color) in zip(stat_cols, [
        ("~20%", "of African children with RHD die by age 15", DARK["accent"]),
        ("~70%", "die by age 25 without treatment", "#ff4444"),
        (">60%", "of RHD cases are female", DARK["blue"]),
    ]):
        with col:
            st.markdown(
                f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:10px;'
                f'padding:1rem;text-align:center">'
                f'<div style="font-size:2rem;font-weight:800;color:{color}">{stat}</div>'
                f'<div style="font-size:0.82rem;color:{DARK["muted"]};margin-top:0.3rem">{label}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


def _topic_prevention():
    st.markdown("### 💊 Prevention Strategies")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Primary Prevention")
        st.markdown("""
        Preventing the **first episode of ARF** by treating strep throat promptly.
        
        **Target:** All patients with GAS pharyngitis
        
        **Treatment:** Benzathine penicillin G (single IM injection) or oral penicillin V for 10 days
        
        **Amoxicillin** is an effective alternative (once daily oral dosing improves adherence)
        
        **Challenges in Africa:**
        - Strep throat diagnosis is clinical — no rapid tests available in most clinics
        - BPG stockouts are frequent in rural health facilities
        - Over-the-counter antibiotic access is inconsistent
        - Patients often present late or to traditional healers
        """)
    with col2:
        st.markdown("#### Secondary Prevention")
        st.markdown("""
        Preventing **recurrent ARF** in patients who have already had one episode — halting 
        further valve damage.
        
        **Target:** All patients with documented ARF or RHD
        
        **Treatment:** Monthly benzathine penicillin G 1.2 million units IM
        
        **Duration:**
        - RHD with persistent valvular disease: until age 40 or lifelong
        - ARF without valvular involvement: until age 21 or 5 years post-ARF (whichever is longer)
        
        **Challenges:**
        - Monthly injections are painful and require clinic visits
        - Drug supply chain interruptions are common
        - Decentralised patient tracking is lacking
        """)

    _card("The Penicillin Gap",
          "BPG costs approximately $0.50 per injection. Monthly prophylaxis for 10 years "
          "costs ~$60 per patient — yet stockouts persist across Africa. Supply chain failures "
          "represent one of the most critical and solvable gaps in RHD prevention.",
          DARK["yellow"], "💉")

    st.markdown("#### Tertiary Prevention")
    st.markdown("""
    Preventing complications in patients with **established RHD**:
    
    - **Anticoagulation** (warfarin) for patients with atrial fibrillation or prior thromboembolism
    - **Rate/rhythm control** for atrial fibrillation
    - **Surgical valve repair or replacement** for severe valvular disease
    - **Percutaneous balloon mitral valvotomy (PBMV)** for eligible mitral stenosis cases
    - **Infective endocarditis prophylaxis** for dental and invasive procedures
    """)

    st.markdown("#### Prevention Effectiveness")
    interventions = ["Primary Prevention\n(Treat strep throat)", "Secondary Prophylaxis\n(Monthly BPG)", 
                     "Valve Surgery / PBMV", "Community Screening"]
    effectiveness = [95, 80, 70, 60]
    feasibility = [85, 65, 30, 50]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Effectiveness (%)", x=interventions, y=effectiveness, marker_color=DARK["green"]))
    fig.add_trace(go.Bar(name="Feasibility in Africa (%)", x=interventions, y=feasibility, marker_color=DARK["blue"]))
    fig.update_layout(
        paper_bgcolor=DARK["paper"], plot_bgcolor=DARK["plot"],
        font=dict(color=DARK["text"]),
        barmode="group",
        xaxis=dict(gridcolor=DARK["grid"]),
        yaxis=dict(title="%", gridcolor=DARK["grid"], range=[0, 110]),
        legend=dict(bgcolor=DARK["plot"]),
        margin=dict(l=40, r=20, t=20, b=40),
        height=300,
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def _topic_public_health():
    st.markdown("### 🌍 Public Health & Policy")
    st.markdown("""
    Despite being entirely preventable, RHD remains a leading cause of cardiovascular death in 
    Africa due to systemic failures across health systems, policy, and drug supply chains.
    """)

    _card("Data Fragmentation",
          "Patient records are maintained in paper ledgers across isolated clinics, ministries, "
          "NGOs, and academic institutions. No standardised pan-African RHD registry exists. "
          "This makes it impossible to track prophylaxis adherence or disease burden at a national level.",
          DARK["accent"], "📋")

    _card("Healthcare Infrastructure Gap",
          "Over 80% of rural health clinics in sub-Saharan Africa lack basic ultrasound equipment. "
          "Community nurses are rarely trained to identify subclinical RHD. Early cardiac fatigue "
          "is routinely misdiagnosed as asthma or malnutrition.",
          DARK["yellow"], "🏥")

    _card("WHO & Global Commitments",
          "The World Heart Federation's 25×25 initiative and WHO's NCD action plan target "
          "rheumatic fever and RHD. The RHD Action network advocates for national elimination programmes. "
          "Several African countries have established national RHD control programmes, but coverage remains limited.",
          DARK["blue"], "🌐")

    st.markdown("#### Policy Priority Framework")
    priorities = [
        ("Surveillance & Data", "Establish national RHD registries and standardised patient tracking systems", "Critical", DARK["accent"]),
        ("Drug Supply Chain", "Ensure uninterrupted BPG supply through strategic national stockpiles", "Critical", DARK["accent"]),
        ("Task Shifting", "Train community health workers in strep throat recognition and BPG administration", "High", DARK["yellow"]),
        ("School Screening", "Implement echocardiographic screening programmes in primary schools", "High", DARK["yellow"]),
        ("Surgical Capacity", "Build hub-and-spoke cardiac surgery networks across the continent", "High", DARK["yellow"]),
        ("Health Expenditure", "Increase domestic health financing — most modifiable predictor of RHD outcomes", "Moderate", DARK["blue"]),
    ]
    for title, desc, level, color in priorities:
        st.markdown(
            f'<div style="background:{DARK["plot"]};border-left:3px solid {color};border-radius:4px;'
            f'padding:0.6rem 1rem;margin:0.4rem 0;display:flex;justify-content:space-between;align-items:center">'
            f'<div><div style="color:{DARK["text"]};font-weight:600;font-size:0.9rem">{title}</div>'
            f'<div style="color:{DARK["muted"]};font-size:0.82rem">{desc}</div></div>'
            f'<div style="color:{color};font-weight:700;font-size:0.78rem;min-width:60px;text-align:right">{level}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


def _topic_women():
    st.markdown("### 🤰 Women & Maternal Risk in RHD")
    st.markdown("""
    Women bear a disproportionately higher burden of RHD across Africa, accounting for more than 
    **60% of all cases**. The intersection of RHD with pregnancy creates a uniquely dangerous situation.
    """)

    _card("Why Women Are More Affected",
          "Hormonal factors and heightened immune response may increase susceptibility to rheumatic fever. "
          "Women in high-burden settings often have longer untreated infection windows due to healthcare access barriers. "
          "Cultural factors may delay care-seeking, allowing repeated strep exposures.",
          DARK["blue"], "👩")

    st.markdown("#### RHD & Pregnancy: A Dangerous Combination")
    st.markdown("""
    Pregnancy imposes significant cardiovascular demands — cardiac output increases by 30–50% during gestation. 
    In women with previously undiagnosed or asymptomatic mitral stenosis, this increased demand can trigger:
    """)

    risks = [
        ("Acute Pulmonary Oedema", "Sudden fluid accumulation in the lungs. Life-threatening emergency.", DARK["accent"]),
        ("Atrial Fibrillation with Haemodynamic Collapse", "Rapid AF with low blood pressure — medical emergency.", DARK["accent"]),
        ("Thromboembolic Stroke", "Blood clots form in the dilated left atrium — leading cause of maternal stroke.", DARK["accent"]),
        ("Maternal Mortality", "RHD is a leading cardiovascular cause of maternal death across Africa.", "#ff4444"),
        ("Foetal Distress", "Reduced cardiac output compromises placental perfusion — foetal growth restriction.", DARK["yellow"]),
        ("Premature Birth", "Haemodynamic instability and hospitalisation increase preterm delivery risk.", DARK["yellow"]),
    ]
    r1, r2 = st.columns(2)
    for i, (title, desc, color) in enumerate(risks):
        with (r1 if i % 2 == 0 else r2):
            _card(title, desc, color)

    _card("The Screening Gap",
          "Most women with severe RHD are first diagnosed during pregnancy — when intervention options "
          "are limited and risk is highest. Pre-conception echocardiographic screening in high-burden "
          "communities would be the highest-impact intervention for reducing maternal mortality from RHD.",
          DARK["green"], "🔍")

    st.markdown("#### Key Recommendations for Pregnant Women with RHD")
    st.markdown("""
    - **Pre-conception counselling** — women with severe MS should be counselled before pregnancy
    - **Early antenatal echocardiography** — baseline valve assessment in the first trimester
    - **Multidisciplinary care** — joint obstetric-cardiology management throughout pregnancy
    - **Planned delivery** — caesarean vs. vaginal delivery decision based on haemodynamic status
    - **Postpartum monitoring** — haemodynamic shifts continue for 24–48 hours post-delivery
    - **Anticoagulation management** — warfarin vs. heparin decision throughout pregnancy
    """)


def _topic_diagnosis():
    st.markdown("### 🩺 Diagnosis & Screening")

    st.markdown("#### Clinical Presentation")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Symptoms**")
        symptoms = [
            ("Dyspnoea (breathlessness)", "Especially on exertion — earliest symptom"),
            ("Palpitations", "From atrial fibrillation or ectopic beats"),
            ("Fatigue", "Reduced cardiac output"),
            ("Chest pain", "Pulmonary hypertension or coronary embolism"),
            ("Syncope", "Severe obstruction or arrhythmia"),
            ("Haemoptysis", "Pulmonary venous hypertension"),
            ("Peripheral oedema", "Right heart failure"),
        ]
        for symptom, desc in symptoms:
            st.markdown(
                f'<div style="margin:0.3rem 0;font-size:0.85rem">'
                f'<span style="color:{DARK["blue"]};font-weight:600">● {symptom}</span>'
                f'<span style="color:{DARK["muted"]}"> — {desc}</span></div>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("**Physical Examination Signs**")
        signs = [
            ("Mid-diastolic murmur", "Low-pitched 'rumble' at the apex — hallmark of MS"),
            ("Opening snap", "High-pitched sound after S2 — pliable leaflets"),
            ("Loud S1", "Increased first heart sound — mobile anterior leaflet"),
            ("Malar flush", "Pink-purple cheeks from low cardiac output"),
            ("Irregular pulse", "Atrial fibrillation"),
            ("Elevated JVP", "Right heart failure"),
            ("Pulmonary crackles", "Pulmonary oedema"),
        ]
        for sign, desc in signs:
            st.markdown(
                f'<div style="margin:0.3rem 0;font-size:0.85rem">'
                f'<span style="color:{DARK["green"]};font-weight:600">● {sign}</span>'
                f'<span style="color:{DARK["muted"]}"> — {desc}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown("#### Diagnostic Investigations")
    investigations = [
        ("Echocardiography", "Gold standard", 
         "2D/Doppler echocardiography measures valve area, gradient, and morphology. "
         "Handheld echo devices are increasingly used for community screening in Africa.", DARK["green"]),
        ("Electrocardiogram (ECG)", "Supportive",
         "P-mitrale (broad, bifid P waves), AF, right ventricular hypertrophy in advanced disease. "
         "Inexpensive and widely available — good screening adjunct.", DARK["blue"]),
        ("Chest X-ray", "Supportive",
         "Left atrial enlargement (double density sign, splaying of carina). Pulmonary oedema, "
         "mitral valve calcification. Available in most district hospitals.", DARK["blue"]),
        ("Cardiac MRI", "Advanced",
         "Highly accurate valve assessment. Not routinely available in most African settings. "
         "Used in complex cases or pre-surgical planning.", DARK["muted"]),
    ]
    for title, level, desc, color in investigations:
        st.markdown(
            f'<div style="background:{DARK["plot"]};border:1px solid {DARK["grid"]};border-radius:8px;'
            f'padding:0.8rem 1rem;margin:0.4rem 0">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="color:{color};font-weight:700">{title}</span>'
            f'<span style="color:{color};font-size:0.75rem;background:{DARK["grid"]};padding:0.15rem 0.5rem;border-radius:4px">{level}</span>'
            f'</div>'
            f'<div style="font-size:0.85rem;color:{DARK["text"]};margin-top:0.3rem">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    _card("Echocardiographic Screening Programmes",
          "School-based echo screening programmes have successfully identified subclinical RHD in Uganda, "
          "Mozambique, and Ethiopia — detecting disease at an earlier, more treatable stage. "
          "Training nurses to use handheld echo devices is the most scalable approach for Africa.",
          DARK["green"], "🔊")
