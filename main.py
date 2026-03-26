import streamlit as st
import math

# Configurazione Pagina
st.set_page_config(page_title="RINA Step-by-Step Designer", layout="wide")

st.title("🚢 Dimensionamento Impianti: Percorso Guidato")
st.write("Segui i passaggi per calcolare lo spessore delle tubazioni secondo il Regolamento RINA.")

# --- INPUT INIZIALI ---
st.sidebar.header("📍 Dati di Partenza")
fluido = st.sidebar.selectbox("1. Tipo di Fluido", ["Acqua Mare", "Combustibile / Olio", "Acqua Dolce", "Aria Compressa"])
p_bar = st.sidebar.number_input("2. Pressione di Progetto (P) [bar]", min_value=0.5, value=10.0)
d_ext = st.sidebar.number_input("3. Diametro Esterno (D) [mm]", min_value=10.0, value=114.3)

# --- STEP 1: SOLLECITAZIONE AMMISSIBILE ---
with st.expander("Step 1: Determinazione della Sollecitazione Ammissibile ($f$)", expanded=True):
    st.markdown("""
    Secondo **RINA Part C, Ch 1, Sec 10**, la sollecitazione ammissibile $f$ dipende dal materiale. 
    Per l'acciaio al carbonio standard si utilizza solitamente:
    """)
    f_amm = 120.0
    st.latex(r"f = 120 \, N/mm^2")
    st.info("Regola: $f$ non deve superare il valore minore tra $R_m/2.7$ e $R_e/1.5$.")

# --- STEP 2: FORMULA DELLO SPESSORE TEORICO ---
with st.expander("Step 2: Calcolo dello Spessore Teorico ($t_0$)", expanded=False):
    st.markdown("La formula fondamentale per lo spessore teorico è:")
    st.latex(r"t_0 = \frac{P \cdot D}{20 \cdot f \cdot e + P}")
    
    e_joint = 1.0 # Efficienza giunto
    t0 = (p_bar * d_ext) / (20 * f_amm * e_joint + p_bar)
    
    st.write(f"Sostituendo i tuoi dati: $({p_bar} \cdot {d_ext}) / (20 \cdot {f_amm} \cdot {e_joint} + {p_bar})$")
    st.metric("Risultato t0", f"{t0:.2f} mm")

# --- STEP 3: SOVRASPESSORE PER CORROSIONE ---
with st.expander("Step 3: Aggiunta Sovraspessore per Corrosione ($c$)", expanded=False):
    st.markdown("Il RINA impone un valore fisso $c$ per compensare l'usura nel tempo (Tabella 23).")
    
    if fluido == "Acqua Mare":
        c = 3.0
        regola_c = "Obbligatorio per linee acqua mare in acciaio."
    elif fluido == "Combustibile / Olio":
        c = 1.5
        regola_c = "Standard per circuiti lubrificazione e combustibile."
    else:
        c = 1.0
        regola_c = "Valore minimo per fluidi non corrosivi."
        
    st.write(f"Per **{fluido}**, il valore selezionato è:")
    st.latex(f"c = {c} \, mm")
    st.caption(f"Nota RINA: {regola_c}")

# --- STEP 4: TOLLERANZA DI FABBRICAZIONE ---
with st.expander("Step 4: Tolleranza di Fabbricazione ($a$)", expanded=False):
    st.markdown("I tubi commerciali hanno una tolleranza negativa (solitamente 12.5%). Lo spessore deve essere aumentato per garantire il minimo.")
    st.latex(r"t_{min} = \frac{t_0 + c}{1 - \frac{a}{100}}")
    
    a = 12.5
    t_min_req = (t0 + c) / (1 - (a/100))
    
    st.metric("Spessore Minimo Richiesto", f"{t_min_req:.2f} mm")

# --- CONCLUSIONE E RISULTATO FINALE ---
st.success(f"### ✅ Risultato Finale: {t_min_req:.2f} mm")
st.markdown(f"""
Sulla base dei calcoli step-by-step:
1. Hai un diametro esterno di **{d_ext} mm**.
2. Lo spessore minimo normativo è **{t_min_req:.2f} mm**.
3. **Azione:** Devi scegliere un tubo commerciale con spessore nominale $\ge$ {t_min_req:.2f} mm.
""")

if st.button("Riavvia il Percorso"):
    st.rerun()