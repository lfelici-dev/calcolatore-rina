import streamlit as st
import math

# --- DATABASE TUBI STANDARD (ANSI/ASME B36.10) ---
# Struttura: { Diametro Esterno: { Nome Sch: Spessore } }
PIPE_DATA = {
    21.3:  {"Sch 10": 2.11, "Sch 40": 2.77, "Sch 80": 3.73},
    26.7:  {"Sch 10": 2.11, "Sch 40": 2.87, "Sch 80": 3.91},
    33.4:  {"Sch 10": 2.77, "Sch 40": 3.38, "Sch 80": 4.55},
    42.2:  {"Sch 10": 2.77, "Sch 40": 3.56, "Sch 80": 4.85},
    48.3:  {"Sch 10": 2.77, "Sch 40": 3.68, "Sch 80": 5.08},
    60.3:  {"Sch 10": 2.77, "Sch 40": 3.91, "Sch 80": 5.54},
    88.9:  {"Sch 10": 3.05, "Sch 40": 5.49, "Sch 80": 7.62},
    114.3: {"Sch 10": 3.05, "Sch 40": 6.02, "Sch 80": 8.56},
    168.3: {"Sch 10": 3.40, "Sch 40": 7.11, "Sch 80": 10.97},
}

st.set_page_config(page_title="RINA Standard Pipe Matcher", layout="centered")

st.title("🚢 Relazione Tecnica e Scelta Tubo Standard")
st.markdown("Calcolo normativo con selezione automatica del catalogo **ANSI/ASME**.")
st.divider()

# --- INPUT ---
st.sidebar.header("📋 Input Progetto")
fluido = st.sidebar.selectbox("Tipo di Fluido", ["Acqua Mare", "Combustibile / Olio", "Acqua Dolce"])
p_bar = st.sidebar.number_input("Pressione Progetto (P) [bar]", min_value=1.0, value=12.0)
d_ext = st.sidebar.selectbox("Diametro Esterno Nominale (D) [mm]", list(PIPE_DATA.keys()))

# --- FASE 1: CALCOLO RINA ---
st.subheader("1️⃣ Calcolo Requisito Minimo (RINA)")

# Costanti
f_amm = 120.0
c = 3.0 if fluido == "Acqua Mare" else 1.5
a_tol = 12.5 # Tolleranza fabbricazione %

# Formule
t0 = (p_bar * d_ext) / (20 * f_amm * 1.0 + p_bar)
t_min_req = (t0 + c) / (1 - (a_tol/100))

st.latex(r"t_{min} = \frac{\frac{P \cdot D}{20 \cdot f \cdot e + P} + c}{1 - \frac{a}{100}}")
st.write(f"Secondo i calcoli, lo spessore minimo richiesto è: **{t_min_req:.2f} mm**")

st.divider()

# --- FASE 2: MATCHING COMMERCIALE ---
st.subheader("2️⃣ Selezione Tubo Standard")
st.write(f"Ricerca nel database per il diametro esterno **{d_ext} mm**:")

opzioni_tubi = PIPE_DATA[d_ext]
scelta_finale = None
nome_sch = ""

# Trova il primo spessore che soddisfa il requisito
for sch, spessore in opzioni_tubi.items():
    if spessore >= t_min_req:
        scelta_finale = spessore
        nome_sch = sch
        break

if scelta_finale:
    st.success(f"### Consigliato: {nome_sch}")
    st.info(f"Lo spessore reale di questo tubo è **{scelta_finale} mm**, che copre il tuo fabbisogno di {t_min_req:.2f} mm.")
    
    # Rappresentazione visiva
    st.progress(min(t_min_req / scelta_finale, 1.0))
    st.caption(f"Utilizzo del materiale: { (t_min_req/scelta_finale)*100 :.1f}% della capacità del tubo.")
else:
    st.error("⚠️ Attenzione: nessuno spessore standard (fino a Sch 80) soddisfa il requisito. Valutare un diametro maggiore o materiale diverso.")

st.divider()

# --- FASE 3: PESO E ORDINE ---
st.subheader("3️⃣ Dati per l'Ufficio Acquisti")
if scelta_finale:
    # Calcolo peso reale del tubo scelto
    area = (math.pi / 4) * (d_ext**2 - (d_ext - 2 * scelta_finale)**2)
    peso = (area * 7850) / 1_000_000
    
    col1, col2 = st.columns(2)
    col1.metric("Peso Tubo", f"{peso:.2f} kg/m")
    col2.metric("Specifica", f"DN {d_ext} {nome_sch}")