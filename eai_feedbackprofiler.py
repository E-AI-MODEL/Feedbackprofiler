import streamlit as st
import matplotlib.pyplot as plt

# --- RUBRIC DEFINITIES ---

rubric_VC = {
    (0.1, 0.2): {
        "omschrijving": "AI toont nauwelijks potentieel voor begripsvorming",
        "micro_min": "Statische herhaling van losse feiten",
        "micro_max": "Geen begripsvorming mogelijk",
        "advies": (
            "Gebruik AI alleen als hulpmiddel bij begripsopbouw, "
            "niet als vervanger."
        )
    },
    (0.5, 0.6): {
        "omschrijving": (
            "AI ondersteunt verklarend denken en eenvoudige analyse"
        ),
        "micro_min": "Verklaringen via vergelijkingen",
        "micro_max": "Oorzaak-gevolgredenering in beperkte context",
        "advies": (
            "Laat leerlingen eigen verklaringen formuleren in plaats van "
            "AI-responses kopiëren."
        )
    },
    (0.9, 1.0): {
        "omschrijving": "AI faciliteert complexe probleemoplossing",
        "micro_min": "Strategieontwikkeling",
        "micro_max": "Hypothesetoetsing in onbekende context",
        "advies": (
            "Begeleid leerlingen actief bij het doorgronden van complexe "
            "AI-output."
        )
    }
}

rubric_VM = {
    (0.1, 0.2): {
        "omschrijving": "AI ondersteunt nauwelijks zelfregulatie",
        "micro_min": "Alleen eindfeedback",
        "micro_max": "Geen zicht op leerproces",
        "advies": (
            "Stimuleer leerlingen om zelf doelen en reflecties te formuleren."
        )
    },
    (0.5, 0.6): {
        "omschrijving": "AI ondersteunt losse stappen van zelfregulatie",
        "micro_min": "Monitoring tijdens taak",
        "micro_max": "Reflectievragen en logboeken",
        "advies": "Laat leerlingen expliciet hun leerstrategie verwoorden."
    },
    (0.9, 1.0): {
        "omschrijving": "AI ondersteunt gepersonaliseerde leerstrategieën",
        "micro_min": "Zelfgegenereerde strategieën",
        "micro_max": "Ondersteuning van eigen regulatieroutines",
        "advies": (
            "Zorg voor evenwicht tussen AI-coaching en menselijke begeleiding."
        )
    }
}

# --- TD MATRIX SIMPLIFIED ---

td_matrix = {
    ("0.9", "V_C"): {
        "kernhandeling": "evalueren en generaliseren van kennis",
        "flag": "AI_dominantie",
        "norm": 0.3
    },
    ("0.5", "V_M"): {
        "kernhandeling": "bewustwording van eigen begrip",
        "flag": "Underuse_warning",
        "norm": 0.5
    }
}


# --- HELPERFUNCTIES ---

def match_rubric(score, rubric):
    for (low, high), data in rubric.items():
        if low <= score <= high:
            return data
    return None


def td_flag(p, v_type, td_score):
    key = (str(p), v_type)
    if key in td_matrix:
        norm = td_matrix[key]["norm"]
        if td_score > norm:
            return td_matrix[key]["flag"]
    return "TD_balanced"

# --- STREAMLIT INTERFACE ---


st.title("E_AI Feedbackprofiler")

st.write("Analyseer feedbackinstructies op leerwaarde en AI-dominantie")

feedback = st.text_area("Voer hier de feedbackprompt of instructie in")
rol = st.selectbox("Kies gebruikersrol", ["Docent", "Leerling", "Ontwikkelaar"])


if st.button("Analyseer feedback") and feedback.strip():

    st.subheader("1. Rubric-inschatting")

    # Gesimuleerde analyse (kan vervangen worden door GPT-inschatting)
    score_vc = 0.6
    score_vm = 0.6
    p_score = 0.9
    td_score = 0.65

    vc_match = match_rubric(score_vc, rubric_VC)
    vm_match = match_rubric(score_vm, rubric_VM)
    td_flag_result = td_flag(p_score, "V_C", td_score)

    st.markdown(f"**V_C-score:** {score_vc} → {vc_match['omschrijving']}")
    st.markdown(
        f"- Microdescriptoren: {vc_match['micro_min']} → "
        f"{vc_match['micro_max']}"
    )

    st.markdown(f"**V_M-score:** {score_vm} → {vm_match['omschrijving']}")
    st.markdown(
        f"- Microdescriptoren: {vm_match['micro_min']} → "
        f"{vm_match['micro_max']}"
    )

    st.subheader("2. Taakdichtheid (TD)")
    td_markdown = (
        f"**TD-score**: {td_score} bij P={p_score}, V_C → "
        f"Flag: `{td_flag_result}`"
    )
    st.markdown(td_markdown)

    st.subheader("3. Rolspecifiek advies")
    if rol == "Docent":
        st.markdown(f"- {vc_match['advies']}")
        st.markdown(f"- {vm_match['advies']}")
    elif rol == "Leerling":
        st.markdown("- Let op je eigen denkwerk bij gebruik van AI.")
        st.markdown("- Reflecteer op wat je leert zonder hulp van de tool.")
    elif rol == "Ontwikkelaar":
        st.markdown("- Zorg voor transparante AI-output.")
        st.markdown("- Bouw reflectievragen of keuzemomenten in.")

    st.subheader("4. Visualisatie: Taakdichtheid")
    fig, ax = plt.subplots()
    ax.barh(
        ["TD-score"],
        [td_score],
        color="orange" if td_score > 0.5 else "green"
    )
    ax.set_xlim(0, 1)
    st.pyplot(fig)
