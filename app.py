import streamlit as st
import pandas as pd
from streamlit_js_eval import get_geolocation

# Intentar cargar e inicializar la API de Gemini
try:
    from google import genai
    HAS_GEMINI_LIB = True
except ImportError:
    HAS_GEMINI_LIB = False

# Configuración inicial de la página
st.set_page_config(
    page_title="Central SST 5.0 + Gemini IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Detectar API Key desde Secrets de Streamlit
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)

# Estado Global: Activar/Desactivar Recepción de Reportes (Por defecto: True)
if "recepcion_activa" not in st.session_state:
    st.session_state["recepcion_activa"] = True

# Inicializar Base de Datos de Reportes en la Sesión
if "reportes" not in st.session_state:
    st.session_state["reportes"] = [
        {
            "ID": "REP-001", 
            "Usuario": "Luis Quintero", 
            "Ubicación": "Zona de Embalaje - Planta 1", 
            "Latitud": 4.6097, 
            "Longitud": -74.0817, 
            "Tipo Riesgo": "Ergonómico (Posturas/Cargas/Movimientos Repetitivos)", 
            "Severidad": "Media", 
            "Descripción": "Posturas forzadas por altura inadecuada de la mesa de empaque.", 
            "Estado": "En Revisión",
            "Respuesta_Admin": "Pendiente de visita técnica por especialista en ergonomía.",
            "Responsable": "Comité SST / Ergonomía"
        },
        {
            "ID": "REP-002", 
            "Usuario": "Carlos Perez", 
            "Ubicación": "Datacenter Central / Rack 2", 
            "Latitud": 4.6110, 
            "Longitud": -74.0825, 
            "Tipo Riesgo": "IT - Infraestructura & Datacenter (Racks/Ruido Servidores/Calor)", 
            "Severidad": "Alta", 
            "Descripción": "Exceso de ruido en servidor secundario y sobrecalentamiento en Rack 2.", 
            "Estado": "Validado / En Gestión",
            "Respuesta_Admin": "Se programó mantenimiento preventivo de sistema de ventilación HVAC.",
            "Responsable": "Infraestructura & Soporte IT"
        },
        {
            "ID": "REP-003", 
            "Usuario": "María Rodríguez", 
            "Ubicación": "Celda Robótica 3", 
            "Latitud": 4.6105, 
            "Longitud": -74.0820, 
            "Tipo Riesgo": "Mecánico (Maquinaria/Herramientas/Atrapamiento)", 
            "Severidad": "Crítica", 
            "Descripción": "Sensor de proximidad de brazo robótico presenta latencia intermitente.", 
            "Estado": "Atendido / Cerrado",
            "Respuesta_Admin": "Parada preventiva ejecutada. Sensor reconfigurado bajo norma ISO 10218.",
            "Responsable": "Mantenimiento Industrial & Mecatrónica"
        }
    ]

if "contador_id" not in st.session_state:
    st.session_state["contador_id"] = len(st.session_state["reportes"]) + 1

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# Estilos CSS Avanzados para Central Empresarial
st.markdown("""
    <style>
    .main-title {font-size:28px; font-weight:bold; color:#0F172A; margin-bottom:0px;}
    .sub-title {font-size:14px; color:#475569; margin-bottom:15px;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:5px 12px; border-radius:15px; font-weight:bold;}
    
    .status-online {background-color:#DCFCE7; color:#15803D; border:1px solid #86EFAC; padding:6px 14px; border-radius:20px; font-weight:bold; display:inline-block; text-align:center;}
    .status-offline {background-color:#FEE2E2; color:#B91C1C; border:1px solid #FCA5A5; padding:6px 14px; border-radius:20px; font-weight:bold; display:inline-block; text-align:center;}
    
    .report-card-admin {background-color:#F8FAFC; padding:16px; border-radius:10px; border-left:5px solid #0284C7; margin-bottom:12px;}
    .report-card-user {background-color:#F0FDF4; padding:16px; border-radius:10px; border-left:5px solid #16A34A; margin-bottom:12px;}
    .ai-box {background-color:#F8FAFC; padding:18px; border-radius:10px; border:1px solid #CBD5E1; margin-top:10px; line-height:1.6;}
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
col_header, col_status = st.columns([3, 1])

with col_header:
    st.markdown('<p class="main-title">🏢 Central 360° de Control Empresarial SST 5.0</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Sistema Integrado de Gestión, Gobernanza Algorítmica & Respuesta a Incidentes | Semillero CUN</p>', unsafe_allow_html=True)

with col_status:
    st.write("")
    if st.session_state["recepcion_activa"]:
        st.markdown('<div class="status-online">🟢 Servicio EN LÍNEA</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">🔴 Servicio FUERA DE LÍNEA</div>', unsafe_allow_html=True)

st.write("---")

# Menú Lateral
st.sidebar.title("🔐 Autenticación & Estado")

rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario / Operario (Reporte & Consulta Personal)",
        "🔒 Central Administrador (Dashboard Empresarial 360°)"
    ]
)

st.sidebar.write("---")

if st.session_state["recepcion_activa"]:
    st.sidebar.success("🟢 **Recepción Publica:** ACTIVA")
else:
    st.sidebar.error("🔴 **Recepción Publica:** PAUSADA")

if GEMINI_KEY:
    st.sidebar.info("🤖 **Gemini IA Copilot:** Conectado")

st.sidebar.write("---")

# Login de Administrador
if "Central Administrador" in rol_seleccionado:
    if not st.session_state["admin_autenticado"]:
        st.sidebar.subheader("🔑 Iniciar Sesión SysAdmin")
        user_input = st.sidebar.text_input("Usuario:", key="login_user")
        pass_input = st.sidebar.text_input("Contraseña:", type="password", key="login_pass")
        
        if st.sidebar.button("Ingresar a la Central"):
            if user_input == "SysAdmin" and pass_input == "097":
                st.session_state["admin_autenticado"] = True
                st.sidebar.success("✅ Acceso concedido como SysAdmin")
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

# Función para consultar Gemini API
def consultar_gemini_real(prompt_texto, api_key):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_texto,
        )
        return response.text
    except Exception as e:
        return f"Error en la llamada a la API: {str(e)}"

# Generador de Diagnóstico Heurístico Avanzado SST 5.0
def generar_analisis_avanzado_sst(rep):
    cat = rep["Tipo Riesgo"]
    desc = rep["Descripción"].lower()
    sev = rep["Severidad"]
    ubic = rep["Ubicación"]

    if "ergonómico" in cat.lower() or "postura" in desc or "silla" in desc or "carga" in desc:
        causa = f"Sobrecarga biomecánica en zona postural por movimientos repetitivos o altura inadecuada en <b>'{ubic}'</b>."
        plan = "1. Evaluación ergonométrica en campo mediante metodologías <b>RULA / REBA</b>.<br>2. Ajuste de planos de trabajo y dotación de soportes ergonómicos neutros.<br>3. Sensibilización en pausas activas automatizadas de 5 minutos cada 2 horas e instalación de sensores IMU."
        norma = "<b>ISO 11228</b> (Manipulación de cargas), <b>ISO 9241</b> y marco legal de SST <b>ISO 45001</b>."
    elif "mecánico" in cat.lower() or "brazo" in desc or "robot" in desc or "atrapamiento" in desc:
        causa = f"Riesgo de atrapamiento mecánico o falla en sensores de proximidad en la celda <b>'{ubic}'</b>."
        plan = f"1. Activación del protocolo de parada de emergencia determinista (Runtime Assurance / CBF).<br>2. Recalibración del margen de fuerza biomecánica (140 N - 290 N).<br>3. Despliegue de visión por computador (YOLOv8) para prevención de intrusión."
        norma = "<b>ISO 10218-1/2</b> (Robótica industrial) y especificación técnica <b>ISO/TS 15066</b>."
    elif "it -" in cat.lower() or "datacenter" in desc or "rack" in desc or "servidor" in desc or "pantalla" in desc:
        causa = f"Exposición a ruido contínuo de servidores, fatiga térmica o fatiga visual acumulada en <b>'{ubic}'</b>."
        plan = "1. Medición de sonometría y auditoría de aislamiento acústico/HVAC en gabinete de servidores.<br>2. Ajuste ergonómico de pantallas (pantalla a la altura de los ojos y regla 20-20-20).<br>3. Balance de turnos de soporte para mitigar tecnoestrés."
        norma = "<b>ISO 9241-300</b> (Ergonomía VDT) y normas de higiene ocupacional en infraestructura IT."
    else:
        causa = f"Condición o acto inseguro detectado en <b>'{ubic}'</b> clasificado con nivel de severidad <b>{sev}</b>."
        plan = "1. Inspección inmediata de seguridad física por la brigada de emergencias.<br>2. Aislamiento y señalización preventiva del hallazgo.<br>3. Definición de acción correctiva en comité COPASST."
        norma = "<b>ISO 45001:2018</b> (Sistemas de Gestión de Seguridad y Salud en el Trabajo)."

    return f"""
    <div class="ai-box">
    <h4 style="color:#0F172A; margin-top:0px;">🔬 Dictamen Técnico de Inspección Automática (SST 5.0)</h4>
    <p><b>🆔 Reporte Evaluado:</b> <code>{rep['ID']}</code> | <b>Severidad:</b> <span style="color:#B91C1C; font-weight:bold;">{sev}</span></p>
    <hr style="border:0.5px solid #E2E8F0;">
    <p>🧠 <b>Causa Raíz Identificada:</b><br>{causa}</p>
    <p>🛠️ <b>Plan de Intervención e Impacto Proactivo:</b><br>{plan}</p>
    <p>📜 <b>Sustento Normativo e ISOs Aplicables:</b><br>{norma}</p>
    </div>
    """

# ========================================================
# ROL 1: USUARIO / OPERARIO
# ========================================================
if "Usuario / Operario" in rol_seleccionado:
    st.header("👷 Módulo de Trabajo para Usuarios & Operarios")
    
    tab_nuevo_rep, tab_mis_reportes = st.tabs(["📝 Registrar Nuevo Reporte (ID Único)", "📋 Consultar Mis Reportes Registrados"])

    with tab_nuevo_rep:
        if not st.session_state["recepcion_activa"]:
            st.error("🚫 **El servicio de recepción de reportes se encuentra temporalmente FUERA DE LÍNEA por mantenimiento o pausa administrativa.**")
            st.info("Por favor, intenta nuevamente más tarde.")
        else:
            id_unico_generado = f"REP-{st.session_state['contador_id']:03d}"
            st.info(f"🆔 **Número de Reporte Único Asignado:** `{id_unico_generado}`")

            col1, col2 = st.columns(2)

            with col1:
                nombre = st.text_input("Nombre Completo del Reportante:", value="Luis Quintero")
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
                        "Respuesta_Admin": "Reporte recibido. En cola de revisión por la Central SST.",
                        "Responsable": "Por Asignar"
                    }
                    st.session_state["reportes"].append(nuevo_reporte)
                    st.session_state["contador_id"] += 1
                    st.success(f"✅ ¡Reporte **{id_unico_generado}** guardado con éxito para **{nombre}**!")
                    st.rerun()
                else:
                    st.warning("⚠️ Por favor completa tu nombre, ubicación y descripción.")

    with tab_mis_reportes:
        st.subheader("🔍 Mis Reportes Registrados")
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
# ROL 2: CENTRAL ADMINISTRADOR (360° EMPRESARIAL)
# ========================================================
else:
    if not st.session_state["admin_autenticado"]:
        st.warning("🔒 Acceso Restringido - Central Empresarial de SST")
        st.info("Ingresa tus credenciales en el menú lateral para desbloquear el Panel de Mando.")
        st.markdown("""
        * **Usuario Administrador:** `SysAdmin`
        * **Contraseña de Acceso:** `097`
        """)
    else:
        st.header("🏢 Central 360° de Control Empresarial de SST & Copilot Gemini IA")
        df_rep = pd.DataFrame(st.session_state["reportes"])

        # Pestañas de la Central Empresarial
        tab_executive, tab_copilot, tab_management, tab_map, tab_controls, tab_database = st.tabs([
            "📊 1. KPIs & Tablero Ejecutivo", 
            "🤖 2. Copilot Gemini IA & Causa Raíz", 
            "✍️ 3. Gestión & Asignación de Casos", 
            "🗺️ 4. Sala de Crisis & Mapa GPS", 
            "🎛️ 5. Switch Master On/Off & Ajustes", 
            "💾 6. BBDD Consolidada & Exportación"
        ])

        # --- MÓDULO 1: KPIS & TABLERO EJECUTIVO ---
        with tab_executive:
            st.subheader("📈 Métricas Clave de Gestión Empresarial de SST")
            total_casos = len(df_rep)
            pendientes = len(df_rep[df_rep["Estado"].str.contains("Pendiente|Nuevo")])
            atendidos = len(df_rep[df_rep["Estado"].str.contains("Atendido|Cerrado")])
            criticos = len(df_rep[df_rep["Severidad"].isin(["Alta", "Crítica"])])
            pct_cumplimiento = (atendidos / total_casos * 100) if total_casos > 0 else 0

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total Incidentes", total_casos)
            m2.metric("Pendientes / Nuevos", pendientes)
            m3.metric("Atendidos / Cerrados", atendidos)
            m4.metric("Nivel Alto / Crítico", criticos)
            m5.metric("Efectividad Cierre", f"{pct_cumplimiento:.1f}%")

            st.write("---")
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("##### 📌 Distribución por Severidad")
                st.bar_chart(df_rep["Severidad"].value_counts())
            with col_chart2:
                st.markdown("##### 🏢 Clasificación por Categorías de Riesgo")
                st.bar_chart(df_rep["Tipo Riesgo"].value_counts())

        # --- MÓDULO 2: COPILOT IA GEMINI ---
        with tab_copilot:
            st.subheader("🤖 Asistente Virtual Copilot IA (Analítica Avanzada SST 5.0)")
            ids_disponibles = [r["ID"] for r in st.session_state["reportes"]]
            sel_id_ia = st.selectbox("Seleccionar Reporte Único para Análisis de Causa Raíz:", ids_disponibles)

            rep_ia = next(r for r in st.session_state["reportes"] if r["ID"] == sel_id_ia)

            st.markdown(f"""
            <div class="report-card-admin">
            <b>🆔 Reporte Único:</b> {rep_ia['ID']} | <b>Usuario:</b> {rep_ia['Usuario']} | <b>Ubicación:</b> {rep_ia['Ubicación']}<br>
            <b>Categoría:</b> {rep_ia['Tipo Riesgo']} | <b>Severidad:</b> {rep_ia['Severidad']}<br>
            <b>Descripción:</b> {rep_ia['Descripción']}
            </div>
            """, unsafe_allow_html=True)

            if st.button("✨ Generar Dictamen Técnico con IA"):
                prompt_enviado = f"""
                Actúa como un Especialista Senior en Seguridad y Salud en el Trabajo (SST 5.0).
                Analiza el siguiente reporte:
                - ID: {rep_ia['ID']}
                - Ubicación: {rep_ia['Ubicación']}
                - Categoría: {rep_ia['Tipo Riesgo']}
                - Severidad: {rep_ia['Severidad']}
                - Descripción: {rep_ia['Descripción']}

                Estructura tu respuesta en:
                1. 🧠 Causa Raíz
                2. 🛠️ Plan de Acción Preventivo y Corrección
                3. 📜 Marco Normativo ISO (ISO 45001, ISO 10218, ISO/TS 15066)
                """

                if GEMINI_KEY and HAS_GEMINI_LIB:
                    with st.spinner("Consultando al modelo Gemini 2.5 en la nube de Google..."):
                        respuesta_gemini = consultar_gemini_real(prompt_enviado, GEMINI_KEY)
                        st.success("✅ Dictamen en tiempo real por Gemini IA:")
                        st.markdown(f'<div class="ai-box">{respuesta_gemini}</div>', unsafe_allow_html=True)
                else:
                    st.info("💡 **Dictamen del Motor Heurístico de la Central (Matriz SST 5.0):**")
                    html_diagnostico = generar_analisis_avanzado_sst(rep_ia)
                    st.markdown(html_diagnostico, unsafe_allow_html=True)

        # --- MÓDULO 3: GESTIÓN & ASIGNACIÓN DE CASOS ---
        with tab_management:
            st.subheader("✍️ Centro de Validación, Asignación y Respuesta Oficial")
            col_sel, col_del = st.columns([3, 1])
            with col_sel:
                id_gestion = st.selectbox("Seleccionar Reporte Único a Responder/Editar:", ids_disponibles, key="select_gestion")
            
            idx_gestion = next(i for i, r in enumerate(st.session_state["reportes"]) if r["ID"] == id_gestion)
            r_edit = st.session_state["reportes"][idx_gestion]

            with col_del:
                st.write("")
                st.write("")
                if st.button("🗑️ Eliminar Reporte", type="primary"):
                    st.session_state["reportes"].pop(idx_gestion)
                    st.success(f"Reporte {id_gestion} eliminado de la Central.")
                    st.rerun()

            with st.form("form_edit_admin"):
                c_a, c_b = st.columns(2)
                with c_a:
                    nuevo_estado = st.selectbox(
                        "Estado de la Solicitud:",
                        ["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"],
                        index=["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"].index(r_edit["Estado"]) if r_edit["Estado"] in ["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"] else 0
                    )
                    responsable = st.text_input("Asignar Área/Responsable de Caso:", value=r_edit.get("Responsable", "Comité SST"))

                with c_b:
                    respuesta_admin = st.text_area("Respuesta Oficial / Plan de Intervención:", value=r_edit.get("Respuesta_Admin", ""))

                btn_guardar_cambios = st.form_submit_button("💾 Guardar Cambios en BBDD")

                if btn_guardar_cambios:
                    st.session_state["reportes"][idx_gestion]["Estado"] = nuevo_estado
                    st.session_state["reportes"][idx_gestion]["Responsable"] = responsable
                    st.session_state["reportes"][idx_gestion]["Respuesta_Admin"] = respuesta_admin
                    st.success(f"✅ Registro **{id_gestion}** actualizado correctamente.")
                    st.rerun()

        # --- MÓDULO 4: SALA DE CRISIS & MAPA GPS ---
        with tab_map:
            st.subheader("🗺️ Sala de Crisis & Mapa de Calor Georreferenciado")
            df_mapa = df_rep.rename(columns={"Latitud": "lat", "Longitud": "lon"})
            st.map(df_mapa[["lat", "lon"]], zoom=13)

        # --- MÓDULO 5: SWITCH MASTER ON/OFF & AJUSTES ---
        with tab_controls:
            st.subheader("🎛️ Centro de Mando Master & Disponibilidad del Servicio")
            st.write("Controla la disponibilidad pública para la recepción de reportes desde cualquier dispositivo:")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                nuevo_estado_switch = st.toggle("🟢 Prender (EN LÍNEA) / 🔴 Apagar (FUERA DE LÍNEA)", value=st.session_state["recepcion_activa"])
                if nuevo_estado_switch != st.session_state["recepcion_activa"]:
                    st.session_state["recepcion_activa"] = nuevo_estado_switch
                    st.rerun()

            with col_c2:
                if st.session_state["recepcion_activa"]:
                    st.success("✅ **Estado Global:** EN LÍNEA (Recepción de reportes habilitada)")
                else:
                    st.error("🚨 **Estado Global:** FUERA DE LÍNEA (Formulario bloqueado en modo mantenimiento)")

        # --- MÓDULO 6: BBDD CONSOLIDADA & EXPORTACIÓN ---
        with tab_database:
            st.subheader("💾 Consolidado General Registrado por Usuario")
            user_filter = st.selectbox("Filtrar BBDD por Usuario:", ["Todos los Usuarios"] + list(df_rep["Usuario"].unique()))
            df_export = df_rep[df_rep["Usuario"] == user_filter] if user_filter != "Todos los Usuarios" else df_rep
            st.dataframe(df_export, use_container_width=True)

            csv_export = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Consolidada (CSV / Excel)",
                data=csv_export,
                file_name="Base_Datos_SST_Central_CUN.csv",
                mime="text/csv"
            )