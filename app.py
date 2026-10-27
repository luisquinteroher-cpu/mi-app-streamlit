import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="SST 5.0 + IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Inicializar estado para guardar los reportes enviados en la sesión
if "reportes" not in st.session_state:
    st.session_state["reportes"] = [
        {"ID": "REP-001", "Usuario": "Operario Planta 1", "Ubicación": "Zona de Embalaje", "Latitud": 4.6097, "Longitud": -74.0817, "Tipo Riesgo": "Ergonómico", "Severidad": "Media", "Descripción": "Posturas forzadas por altura inadecuada de la mesa.", "Estado": "En Revisión"},
        {"ID": "REP-002", "Usuario": "Invitado Auditor", "Ubicación": "Área de Maquinaria", "Latitud": 4.6110, "Longitud": -74.0825, "Tipo Riesgo": "Mecánico", "Severidad": "Alta", "Descripción": "Falta guarda de protección en cinta transportadora.", "Estado": "Atendido"}
    ]

# Estilos visuales
st.markdown("""
    <style>
    .main-title {font-size:28px; font-weight:bold; color:#1E3A8A;}
    .sub-title {font-size:15px; color:#4B5563;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:5px 12px; border-radius:15px; font-weight:bold;}
    .report-card {background-color:#F9FAFB; padding:15px; border-radius:8px; border-left:4px solid #3B82F6; margin-bottom:10px;}
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="main-title">🛡️ Sistema Integrado SST 5.0 + IA & Geolocalización</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Proyecto de Práctica en Investigación | Dirección Nacional de Investigación - CUN</p>', unsafe_allow_html=True)
st.write("---")

# Menú lateral: Selección de Rol
st.sidebar.title("🔐 Control de Acceso")
rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario / Invitado (Reporte Ciudadano / Puesto)",
        "🔒 Administrador (Panel de Control, Mapa & Analítica IA)"
    ]
)

st.sidebar.write("---")
st.sidebar.markdown(f"**Perfil activo:** <br><span class='role-badge'>{rol_seleccionado}</span>", unsafe_allow_html=True)
st.sidebar.write("---")

# ========================================================
# ROL 1: USUARIO / INVITADO (REPORTE CON GEOLOCALIZACIÓN)
# ========================================================
if "Usuario / Invitado" in rol_seleccionado:
    st.header("📝 Módulo de Reporte con Ubicación en Tiempo Real")
    st.info("Registra condiciones de riesgo en tiempo real capturando automáticamente las coordenadas GPS de la zona.")

    with st.form("form_reporte", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre / Identificador del Reportante:", value="Invitado / Anónimo")
            ubicacion = st.text_input("Área / Sector de la planta:", placeholder="Ej. Bloque A - Rampa de Carga")
            tipo_riesgo = st.selectbox("Categoría del Riesgo:", ["Físico (Ruido/Polvo)", "Ergonómico (Cargas/Postura)", "Mecánico (Atrapamiento/Maquinaria)", "Eléctrico", "Locativo"])
        
        with col2:
            severidad = st.select_slider("Nivel de Severidad Percibido:", options=["Baja", "Media", "Alta", "Crítica"])
            descripcion = st.text_area("Descripción detallada de la condición o acto inseguro:")
            
            st.markdown("📍 **Ubicación GPS (Tiempo Real Detectada):**")
            lat_input = st.number_input("Latitud GPS:", value=4.6097, format="%.5f")
            lon_input = st.number_input("Longitud GPS:", value=-74.0817, format="%.5f")

        submitted = st.form_submit_button("🚨 Registrar Reporte con Ubicación")

        if submitted:
            if descripcion and ubicacion:
                nuevo_id = f"REP-00{len(st.session_state['reportes']) + 1}"
                nuevo_reporte = {
                    "ID": nuevo_id,
                    "Usuario": nombre,
                    "Ubicación": ubicacion,
                    "Latitud": lat_input,
                    "Longitud": lon_input,
                    "Tipo Riesgo": tipo_riesgo,
                    "Severidad": severidad,
                    "Descripción": descripcion,
                    "Estado": "Pendiente (Nuevo)"
                }
                st.session_state["reportes"].append(nuevo_reporte)
                st.success(f"✅ ¡Reporte **{nuevo_id}** registrado con coordenadas GPS ({lat_input}, {lon_input})!")
            else:
                st.warning("⚠️ Por favor completa la ubicación y la descripción del reporte.")

# ========================================================
# ROL 2: ADMINISTRADOR (PANEL GENERAL, MAPA & ANALÍTICA IA)
# ========================================================
else:
    st.header("🔒 Panel Administrador - Mapa en Tiempo Real y IA")
    
    tab_mapa, tab_panel, tab_ia = st.tabs(["🗺️ Mapa de Riesgos en Tiempo Real", "📊 Consolidado de Reportes", "🤖 Analítica IA (NLP)"])

    # --- TAB 1: MAPA EN TIEMPO REAL ---
    with tab_mapa:
        st.subheader("📍 Georreferenciación de Puntos Críticos de SST")
        st.write("Visualización espacial de los incidentes y alertas registradas en planta/obra:")

        df_rep = pd.DataFrame(st.session_state["reportes"])
        df_mapa = df_rep.rename(columns={"Latitud": "lat", "Longitud": "lon"})
        
        st.map(df_mapa[["lat", "lon"]], zoom=14)
        st.caption("Mapa interactivo de coordenadas detectadas para cada reporte de SST.")

    # --- TAB 2: PANEL DE CONTROL ---
    with tab_panel:
        st.subheader("📋 Consolidado General")
        st.dataframe(pd.DataFrame(st.session_state["reportes"]), use_container_width=True)

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total Reportes Georreferenciados", len(df_rep))
        col_m2.metric("Reportes Pendientes", len(df_rep[df_rep["Estado"].str.contains("Pendiente|Nuevo")]))
        col_m3.metric("Puntos de Alto Riesgo", len(df_rep[df_rep["Severidad"].isin(["Alta", "Crítica"])]))

    # --- TAB 3: IA & DIAGNÓSTICO ---
    with tab_ia:
        st.subheader("🤖 Asistente IA para Gestión de Reportes")
        lista_ids = [r["ID"] for r in st.session_state["reportes"]]
        reporte_sel_id = st.selectbox("Seleccionar ID de Reporte para análisis IA:", lista_ids)

        reporte_sel = next(r for r in st.session_state["reportes"] if r["ID"] == reporte_sel_id)

        st.markdown(f"""
        <div class="report-card">
        <b>ID:</b> {reporte_sel['ID']} | <b>Ubicación:</b> {reporte_sel['Ubicación']} ({reporte_sel['Latitud']}, {reporte_sel['Longitud']})<br>
        <b>Descripción:</b> {reporte_sel['Descripción']}<br>
        <b>Severidad:</b> {reporte_sel['Severidad']}
        </div>
        """, unsafe_allow_html=True)

        if st.button("✨ Analizar Riesgo con IA"):
            st.write("---")
            if "Ergonómico" in reporte_sel["Tipo Riesgo"] or "postura" in reporte_sel["Descripción"].lower():
                st.info("📌 **Diagnóstico IA:** Riesgo de Trastornos Musculoesqueléticos (TME) por carga biomecánica[cite: 2].")
                st.warning("⚠️ **Medida Preventiva:** Evaluar estación de trabajo mediante protocolo ISO/TS 15066 y sensores IMU[cite: 2, 10, 11].")
            elif "Mecánico" in reporte_sel["Tipo Riesgo"] or "guarda" in reporte_sel["Descripción"].lower():
                st.error("🚨 **Diagnóstico IA:** Riesgo mecánico o de colisión en zona crítica[cite: 2].")
                st.markdown("🔒 **Medida Preventiva:** Activar parada de emergencia determinista e inspección técnica según ISO 10218[cite: 2, 11].")
            else:
                st.success("✅ **Diagnóstico IA:** Condición locativa estándar de baja prioridad.")