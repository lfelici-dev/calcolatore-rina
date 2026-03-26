import streamlit as st
import math

# Configurazione Pagina
st.set_page_config(page_title="RINA Design Timeline", layout="centered")

st.title("🚢 Relazione di Calcolo Impianti")
st.markdown("---")

# --- INPUT LATERALE ---
st.sidebar.header("📋 Dati di Input")
fluido = st.sidebar.selectbox("Tipo di Fluido", ["Acqua Mare", "Combustibile / Olio", "Acqua Dolce", "Aria Compressa"])
p_bar = st.sidebar.number_input("Pressione di Progetto (P) [bar]", min_value=0.5, value=10.0)
d_ext = st.sidebar.number_input("Diametro Esterno (D) [mm]", min_value=10.0, value=114.3)

# --- FASE 1: MATERIALE E SOLLECITAZIONE ---
st.subheader("1️⃣ Definizione del Materiale")
st.write("Il primo passo è stabilire la sollecitazione ammissibile ($f$) in base al materiale scelto (Acciaio al carbonio).")

f_amm = 120.0
st.latex(r"f = 120 \, N/mm^2")
st.info("**Regola RINA:** Il valore di $f$ è il minore tra $R_m/2.7$ e $R_e/1.5$ a temperatura ambiente.")

st.markdown("---")

# --- FASE 2: SPESSORE TEORICO ---
st.subheader("2️⃣ Calcolo dello Spessore Teorico")
st.write("Applichiamo la formula per la pressione interna per determinare lo spessore minimo strutturale ($t_0$):")

st.latex(r"t_0 = \frac{P \cdot D}{20 \cdot f \cdot e + P}")

e_joint = 1.0 # Efficienza giunto per tubi senza saldatura
t0 = (p_bar * d_ext) / (20 * f_amm * e_joint + p_bar)

st.write(f"Con $P = {p_bar}$ bar e $D = {d_ext}$ mm, otteniamo:")
st.metric("Spessore Teorico (t0)", f"{t0:.2f} mm")

st.markdown("---")

# --- FASE 3: CORROSIONE ---
st.subheader("3️⃣ Sovraspessore di Corrosione")
st.write(f"In base al fluido (**{fluido}**), il regolamento (Tabella 23) impone un margine di sacrificio ($c$).")

if fluido == "Acqua Mare":
    c = 3.0
elif fluido == "Combustibile / Olio":
    c = 1.5
else:
    c = 1.0

st.latex(f"c = {c} \, mm")
st.write(f"Questo spessore garantisce la tenuta dell'impianto nonostante l'ossidazione nel tempo.")

st.markdown("---")

# --- FASE 4: TOLLERANZE E RISULTATO FINALE ---
st.subheader("4️⃣ Spessore Minimo di Progetto")
st.write("Infine, consideriamo la tolleranza negativa di fabbricazione ($a$) del 12.5% per i tubi d'acciaio.")

st.latex(r"t_{min} = \frac{t_0 + c}{1 - \frac{a}{100}}")

a_tol = 12.5
t_min_req = (t0 + c) / (1 - (a_tol/100))

st.success(f"### Risultato Finale: {t_min_req:.2f} mm")

# --- AGGIUNTA TABELLA MINIMI RINA ---
st.warning(f"**Attenzione:** Verifica che {t_min_req:.2f} mm non sia inferiore agli spessori minimi assoluti tabellati dal RINA (es. Tabella 24).")

# Tasto per resettare
if st.button("Nuovo Calcolo"):
    st.rerun()