import streamlit as st
import math

# Configurazione interfaccia
st.set_page_config(page_title="RINA Ship System Designer", layout="centered")

st.title("🚢 Naval Plant Designer (RINA Rules)")
st.markdown("Strumento di calcolo per impianti ausiliari secondo **RINA Part C, Ch 1, Sec 10**.")

# --- SIDEBAR PER INPUT ---
st.sidebar.header("📥 Dati di Input")
fluido = st.sidebar.selectbox("Tipo di Fluido", ["Acqua Mare", "Combustibile/Olio", "Acqua Dolce", "Aria Compressa"])
p_bar = st.sidebar.number_input("Pressione di Progetto (P) [bar]", min_value=0.5, value=10.0, step=0.5)
d_ext = st.sidebar.number_input("Diametro Esterno Tubo (D) [mm]", min_value=10.0, value=114.3, step=0.1)

# Parametri materiali (Acciaio Standard)
f_amm = 120  # Sollecitazione ammissibile [N/mm2]
e_joint = 1.0 # Efficienza giunto (1.0 per tubi senza saldatura)

# --- LOGICA DI CALCOLO ---
# 1. Sovraspessore Corrosione (c)
if fluido == "Acqua Mare":
    c = 3.0
elif fluido == "Combustibile/Olio":
    c = 1.5
else:
    c = 1.0

# 2. Spessore Teorico (t0)
t0 = (p_bar * d_ext) / (20 * f_amm * e_joint + p_bar)

# 3. Spessore Minimo Totale (considerando tolleranza fabbricazione 12.5%)
t_min_req = (t0 + c) / 0.875

# --- VISUALIZZAZIONE RISULTATI ---
tab1, tab2, tab3 = st.tabs(["📊 Calcolo Spessori", "📉 Perdite di Carico", "✅ Checklist RINA"])

with tab1:
    st.subheader("Risultati Dimensionamento")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Spessore Teorico (t0)", f"{t0:.2f} mm")
        st.write(f"**Sovraspessore corrosione:** {c} mm")
    with col2:
        st.metric("Spessore Minimo Finale", f"{t_min_req:.2f} mm", delta_color="inverse")
        st.info("Scegliere lo spessore commerciale superiore a questo valore.")

with tab2:
    st.subheader("Stima Prevalenza Pompa")
    portata = st.number_input("Portata richiesta [m³/h]", value=25.0)
    lunghezza = st.number_input("Lunghezza linea equivalente [m]", value=30.0)
    
    # Calcolo Velocità
    area = math.pi * ((d_ext - 2*t_min_req)/2000)**2
    v = (portata / 3600) / area
    
    # Perdita di carico (approssimata Darcy)
    rho = 1025 if fluido == "Acqua Mare" else 900
    dp = 0.025 * (lunghezza / (d_ext/1000)) * (rho * v**2 / 2) / 100000
    
    st.write(f"**Velocità fluido:** {v:.2f} m/s")
    if v > 3.0: st.warning("⚠️ Velocità eccessiva! Aumentare il diametro.")
    st.metric("Perdita di carico stimata", f"{dp:.2f} bar")

with tab3:
    st.subheader("Verifiche Obbligatorie RINA")
    st.checkbox("Valvole Quick-Closing installate sui serbatoi?")
    st.checkbox("Linee combustibile separate da quelle acqua mare?")
    st.checkbox("Filtri installati a monte delle pompe?")
    st.checkbox("Comandi remoti per pompe emergenza funzionanti?")

st.divider()
st.caption("Nota: Questo software è un supporto al calcolo. La verifica finale spetta al progettista abilitato.")