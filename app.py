import streamlit as st
import pandas as pd
from streamlit_js_eval import get_geolocation

# Configuración inicial de la página
st.set_page_config(
    page_title="SST 5.0 + IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Inicializar BBDD de reportes en la sesión si no existe
if "reportes" not in st.session_state:
    st.session_state["reportes"] = [
        {
            "ID": "REP-001", 
            "Usuario": "Luis Quintero", 
            "Ubicación": "Zona de Embalaje", 
            "Latitud": 4.6097, 
            "Longitud": -74.0817, 
            "Tipo Riesgo": "Ergonómico (Posturas/Cargas/Movimientos Repetitivos)", 
            "Severidad": "Media", 
            "Descripción": "Posturas forzadas por altura inadecuada de la mesa de empaque.", 
            "Estado": "En Revisión",
            "Respuesta_Admin": "Pendiente de visita técnica por especialista en ergonomía.",
            "Responsable": "Comité SST"
        },
        {
            "ID": "REP-002", 
            "Usuario": "Carlos Perez", 
            "Ubicación": "Datacenter / Servidores", 
            "Latitud": 4.6110, 
            "Longitud": -74.0825, 
            "Tipo Riesgo": "IT - Infraestructura & Datacenter (Racks/Ruido Servidores/Calor)", 
            "Severidad": "Alta", 
            "Descripción": "Exceso de ruido en servidor secundario y sobrecalentamiento en Rack 2.", 
            "Estado": "Validado / En Gestión",
            "Respuesta_Admin": "Se programó mantenimiento preventivo de ventilación.",
            "Responsable": "Infraestructura IT"
        },
        {
            "ID": "REP-003", 
            "Usuario": "Luis Quintero", 
            "Ubicación": "Línea Robótica 3", 
            "Latitud": 4.6105, 
            "Longitud": -74.0820, 
            "Tipo Riesgo": "Mecánico (Maquinaria/Herramientas/Atrapamiento)", 
            "Severidad": "Crítica", 
            "Descripción": "Sensor de proximidad de brazo robótico presenta latencia intermitente.", 
            "Estado": "Atendido / Cerrado",
            "Respuesta_Admin": "Parada de seguridad preventiva ejecutada. Sensor reemplazado bajo ISO 10218.",
            "Responsable": "Mantenimiento Industrial"
        }
    ]

# Contador para garantizar IDs únicos e irrepetibles
if "contador_id" not in st.session_state:
    st.session_state["contador_id"] = len(st.session_state["reportes"]) + 1

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# Estilos CSS
st.markdown("""
    <style>
    .main-title {font-size:30px; font-weight:bold; color:#1E3A8A; margin-bottom:0px;}
    .sub-title {font-size:15px; color:#4B5563; margin-bottom:20px;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:6px 14px; border-radius:20px; font-weight:bold;}
    .report-card-admin {background-color:#F8FAFC; padding:16px; border-radius:10px; border-left:5px solid #2563EB; margin-bottom:15px;}
    .report-card-user {background-color:#F0FDF4; padding:16px; border-radius:10px; border-left:5px solid #16A34A; margin-bottom:15px;}
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown('<p class="main-title">🛡️ Sistema Integrado SST 5.0 + IA & Gobernanza Algorítmica</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Plataforma de Control Empresarial | Dirección Nacional de Investigación - CUN</p>', unsafe_allow_html=True)
st.write("---")

# Menú Lateral
st.sidebar.title("🔐 Control de Acceso")

rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario / Invitado (Reporte & Consulta Personal)",
        "🔒 Administrador (Super Dashboard Empresarial)"
    ]
)

st.sidebar.write("---")

# Validación de Login
if "Administrador" in rol_seleccionado:
    if not st.session_state["admin_autenticado"]:
        st.sidebar.subheader("🔑 Iniciar Sesión de Administrador")
        user_input = st.sidebar.text_input("Usuario:", key="login_user")
        pass_input = st.sidebar.text_input("Contraseña:", type="password", key="login_pass")
        
        if st.sidebar.button("Ingresar al Dashboard"):
            if user_input == "SysAdmin" and pass_input == "097":
                st.session_state["admin_autenticado"] = True
                st.sidebar.success("✅ Autenticado como SysAdmin")
                st.rerun()
            else:
                st.sidebar.error("❌ Credenciales incorrectas")
    else:
        st.sidebar.success("👤 Sesión Activa: SysAdmin")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["admin_autenticado"] = False
            st.rerun()

st.sidebar.markdown(f"**Perfil activo:** <br><span class='role-badge'>{rol_seleccionado}</span>", unsafe_allow_html=True)
st.sidebar.write("---")

# ========================================================
# ROL 1: USUARIO / INVITADO (REGISTRO Y CONSULTA DE HISTORIAL PERSONAL)
# ========================================================
if "Usuario / Invitado" in rol_seleccionado:
    st.header("👷 Módulo de Trabajo para Usuarios & Operarios")
    
    tab_nuevo_rep, tab_mis_reportes = st.tabs(["📝 Registrar Nuevo Reporte (ID Único)", "📋 Consultar Mis Reportes Registrados"])

    # --- PESTAÑA 1: NUEVO REPORTE ---
    with tab_nuevo_rep:
        # Generación del número de reporte único
        id_unico_generado = f"REP-{st.session_state['contador_id']:03d}"
        st.info(f"🆔 **Número de Reporte Único Asignado Automáticamente:** `{id_unico_generado}`")

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre Completo del Reportante / Operario:", value="Luis Quintero")
            ubicacion = st.text_input("Área / Sector de la planta u oficina:", placeholder="Ej. Área IT / Datacenter o Almacén")
            
            tipo_riesgo = st.selectbox(
                "Categoría del Riesgo (General & IT):",
                [
                    "--- 🏢 CATEGORÍAS GENERALES SST ---",
                    "Ergonómico (Posturas/Cargas/Movimientos Repetitivos)",
                    "Mecánico (Maquinaria/Herramientas/Atrapamiento)",
                    "Físico & Locativo (Ruido/Iluminación/Caídas/Resbalones)",
                    "Eléctrico (Tableros/Cableado)",
                    "Químico & Biológico (Sustancias/Polvos/Agentes)",
                    "Psicosocial (Estrés/Carga Mental)",
                    "--- 💻 CATEGORÍAS ESPECÍFICAS DE IT ---",
                    "IT - Visual & Postural (Pantallas/Túnel Carpiano/Sillas)",
                    "IT - Infraestructura & Datacenter (Racks/Ruido Servidores/Calor)",
                    "IT - Tecnoestrés & Ansiedad (Guardias 24/7/SLA)",
                    "IT - Ciberseguridad / Factor Humano (Phishing/Fuga de Datos)"
                ]
            )
            severidad = st.select_slider("Nivel de Severidad Percibido:", options=["Baja", "Media", "Alta", "Crítica"])
            descripcion = st.text_area("Descripción detallada del incidente o condición:")

        with col2:
            st.subheader("📷 Registro Fotográfico")
            foto_capturada = st.camera_input("Capturar foto del hallazgo:")
            if foto_capturada:
                st.success("✅ Evidencia fotográfica cargada.")

            st.subheader("📍 Coordenadas GPS")
            loc = get_geolocation()
            if loc and 'coords' in loc:
                lat_real = loc['coords']['latitude']
                lon_real = loc['coords']['longitude']
                st.success(f"✅ Coordenadas: Lat {lat_real:.5f}, Lon {lon_real:.5f}")
            else:
                lat_real = st.number_input("Latitud GPS:", value=4.6097, format="%.5f")
                lon_real = st.number_input("Longitud GPS:", value=-74.0817, format="%.5f")

        st.write("---")
        if st.button("🚨 Guardar Reporte con ID Único"):
            if "---" in tipo_riesgo:
                st.warning("⚠️ Por favor selecciona una categoría válida de riesgo.")
            elif descripcion and ubicacion and nombre:
                nuevo_reporte = {
                    "ID": id_unico_generado,
                    "Usuario": nombre.strip(),
                    "Ubicación": ubicacion,
                    "Latitud": lat_real,
                    "Longitud": lon_real,
                    "Tipo Riesgo": tipo_riesgo,
                    "Severidad": severidad,
                    "Descripción": descripcion,
                    "Estado": "Pendiente (Nuevo)",
                    "Respuesta_Admin": "Reporte recibido. En cola de revisión por el equipo de SST.",
                    "Responsable": "Por Asignar"
                }
                st.session_state["reportes"].append(nuevo_reporte)
                st.session_state["contador_id"] += 1  # Incrementar contador para el siguiente reporte único
                st.success(f"✅ ¡Reporte **{id_unico_generado}** guardado con éxito para el usuario **{nombre}**!")
                st.rerun()
            else:
                st.warning("⚠️ Por favor completa tu nombre, ubicación y descripción del evento.")

    # --- PESTAÑA 2: CONSULTA POR USUARIO ---
    with tab_mis_reportes:
        st.subheader("🔍 Mis Reportes Registrados")
        st.write("Filtra el historial por el nombre del usuario para ver el estado de tus solicitudes:")

        df_todos = pd.DataFrame(st.session_state["reportes"])
        usuarios_unicos = list(df_todos["Usuario"].unique()) if not df_todos.empty else []

        usuario_buscar = st.selectbox("Selecciona tu nombre de usuario:", usuarios_unicos if usuarios_unicos else ["Sin registros"])

        if usuario_buscar and usuario_buscar != "Sin registros":
            mis_reps = [r for r in st.session_state["reportes"] if r["Usuario"].lower() == usuario_buscar.lower()]

            st.write(f"**Total de reportes asociados a `{usuario_buscar}`:** {len(mis_reps)}")

            for mr in mis_reps:
                st.markdown(f"""
                <div class="report-card-user">
                <b>🆔 Número Único:</b> {mr['ID']} | <b>Ubicación:</b> {mr['Ubicación']}<br>
                <b>Categoría:</b> {mr['Tipo Riesgo']} | <b>Severidad:</b> {mr['Severidad']}<br>
                <b>Descripción:</b> {mr['Descripción']}<br>
                <b>📌 Estado Actual:</b> <code>{mr['Estado']}</code> | <b>Responsable:</b> {mr['Responsable']}<br>
                <b>💬 Respuesta Oficial:</b> {mr['Respuesta_Admin']}
                </div>
                """, unsafe_allow_html=True)

# ========================================================
# ROL 2: ADMINISTRADOR (SUPER DASHBOARD EMPRESARIAL SST + IA)
# ========================================================
else:
    if not st.session_state["admin_autenticado"]:
        st.warning("🔒 Acceso Restringido - Área de Control de SST")
        st.info("Ingresa tus credenciales en el menú lateral para desbloquear el Dashboard Empresarial.")
        st.markdown("""
        * **Usuario Administrador:** `SysAdmin`
        * **Contraseña de Acceso:** `097`
        """)
    else:
        st.header("🔒 Centro de Control Empresarial de SST & Copilot IA")
        
        df_rep = pd.DataFrame(st.session_state["reportes"])

        tab_executive, tab_copilot, tab_management, tab_map, tab_database = st.tabs([
            "📊 Dashboard Ejecutivo & KPIs", 
            "🤖 Copilot IA & Diagnóstico Normativo", 
            "✍️ Centro de Respuesta & Edición", 
            "🗺️ Mapa en Tiempo Real", 
            "💾 Base de Datos por Usuario"
        ])

        # --- TAB 1: DASHBOARD ---
        with tab_executive:
            st.subheader("📈 Indicadores Clave de Gestión (KPIs de SST)")
            
            total_casos = len(df_rep)
            pendientes = len(df_rep[df_rep["Estado"].str.contains("Pendiente|Nuevo")])
            atendidos = len(df_rep[df_rep["Estado"].str.contains("Atendido|Cerrado")])
            criticos = len(df_rep[df_rep["Severidad"].isin(["Alta", "Crítica"])])
            pct_cumplimiento = (atendidos / total_casos * 100) if total_casos > 0 else 0

            kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
            kpi1.metric("Total Incidentes", total_casos)
            kpi2.metric("Pendientes", pendientes, delta=f"{pendientes} requeridos", delta_color="inverse")
            kpi3.metric("Atendidos / Cerrados", atendidos)
            kpi4.metric("Nivel Crítico / Alto", criticos, delta=f"{criticos} en alerta", delta_color="inverse")
            kpi5.metric("Efectividad SST", f"{pct_cumplimiento:.1f}%")

            st.write("---")
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown("##### 📌 Distribución por Nivel de Severidad")
                chart_sev = df_rep["Severidad"].value_counts()
                st.bar_chart(chart_sev)

            with col_chart2:
                st.markdown("##### 🏢 Clasificación por Categorías de Riesgo")
                chart_cat = df_rep["Tipo Riesgo"].value_counts()
                st.bar_chart(chart_cat)

        # --- TAB 2: COPILOT IA ---
        with tab_copilot:
            st.subheader("🤖 Asistente Virtual Inteligente (NLP Copilot SST)")
            ids_disponibles = [r["ID"] for r in st.session_state["reportes"]]
            sel_id_ia = st.selectbox("Seleccionar Reporte Único para Análisis Algorítmico:", ids_disponibles)

            rep_ia = next(r for r in st.session_state["reportes"] if r["ID"] == sel_id_ia)

            st.markdown(f"""
            <div class="report-card-admin">
            <b>🆔 Reporte Único:</b> {rep_ia['ID']} | <b>Usuario Reportado:</b> {rep_ia['Usuario']} | <b>Ubicación:</b> {rep_ia['Ubicación']}<br>
            <b>Categoría:</b> {rep_ia['Tipo Riesgo']} | <b>Severidad:</b> {rep_ia['Severidad']}<br>
            <b>Descripción:</b> {rep_ia['Descripción']}
            </div>
            """, unsafe_allow_html=True)

            if st.button("✨ Generar Diagnóstico Normativo con IA"):
                st.write("---")
                cat_desc = (rep_ia["Tipo Riesgo"] + " " + rep_ia["Descripción"]).lower()

                if "ergonómico" in cat_desc or "postura" in cat_desc or "silla" in cat_desc:
                    st.info("📌 **Diagnóstico Biomecánico:** Riesgo de Trastornos Musculoesqueléticos (TME) por sobrecarga postural[cite: 2].")
                    st.warning("⚠️ **Plan de Acción:** Evaluación postural RULA/REBA, pausas activas e instalación de sensores IMU[cite: 2, 10, 11].")
                elif "mecánico" in cat_desc or "brazo" in cat_desc or "robot" in cat_desc:
                    st.error("🚨 **Diagnóstico de Seguridad Industrial:** Riesgo mecánico o de colisión física en área robótica[cite: 2].")
                    st.markdown("🔒 **Plan de Acción:** Parada de emergencia determinista (CBF)[cite: 2, 11] e inspección bajo estándar **ISO 10218** e **ISO/TS 15066**[cite: 2].")
                else:
                    st.success("✅ **Diagnóstico Estándar:** Incidente locativo general. Programar inspección física.")

        # --- TAB 3: EDICIÓN Y RESPUESTA ---
        with tab_management:
            st.subheader("✍️ Centro de Validación y Gestión de Casos")
            col_sel, col_del = st.columns([3, 1])
            with col_sel:
                id_gestion = st.selectbox("Seleccionar Reporte Único a Responder:", ids_disponibles, key="select_gestion")
            
            idx_gestion = next(i for i, r in enumerate(st.session_state["reportes"]) if r["ID"] == id_gestion)
            r_edit = st.session_state["reportes"][idx_gestion]

            with col_del:
                st.write("")
                st.write("")
                if st.button("🗑️ Eliminar Reporte", type="primary"):
                    st.session_state["reportes"].pop(idx_gestion)
                    st.success(f"Reporte {id_gestion} eliminado de la base de datos.")
                    st.rerun()

            with st.form("form_edit_admin"):
                c_a, c_b = st.columns(2)
                with c_a:
                    nuevo_estado = st.selectbox(
                        "Estado del Reporte:",
                        ["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"],
                        index=["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"].index(r_edit["Estado"]) if r_edit["Estado"] in ["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"] else 0
                    )
                    responsable = st.text_input("Responsable / Área Asignada:", value=r_edit.get("Responsable", "Especialista SST"))

                with c_b:
                    respuesta_admin = st.text_area("Respuesta Oficial / Plan de Intervención:", value=r_edit.get("Respuesta_Admin", ""))

                btn_guardar_cambios = st.form_submit_button("💾 Guardar y Notificar al Usuario")

                if btn_guardar_cambios:
                    st.session_state["reportes"][idx_gestion]["Estado"] = nuevo_estado
                    st.session_state["reportes"][idx_gestion]["Responsable"] = responsable
                    st.session_state["reportes"][idx_gestion]["Respuesta_Admin"] = respuesta_admin
                    st.success(f"✅ Reporte **{id_gestion}** actualizado y disponible en el panel del usuario **{r_edit['Usuario']}**.")
                    st.rerun()

        # --- TAB 4: MAPA ---
        with tab_map:
            st.subheader("📍 Georreferenciación Espacial de Hallazgos")
            df_mapa = df_rep.rename(columns={"Latitud": "lat", "Longitud": "lon"})
            st.map(df_mapa[["lat", "lon"]], zoom=13)

        # --- TAB 5: BBDD ---
        with tab_database:
            st.subheader("💾 Consolidado General Registrado por Usuario")
            
            user_filter = st.selectbox("Filtrar BBDD por Usuario:", ["Todos los Usuarios"] + list(df_rep["Usuario"].unique()))
            
            if user_filter != "Todos los Usuarios":
                df_export = df_rep[df_rep["Usuario"] == user_filter]
            else:
                df_export = df_rep

            st.dataframe(df_export, use_container_width=True)

            csv_export = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Filtrada (CSV / Excel)",
                data=csv_export,
                file_name="Base_Datos_Reportes_SST_CUN.csv",
                mime="text/csv"
            )