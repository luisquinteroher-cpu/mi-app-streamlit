import streamlit as st
import pandas as pd
from streamlit_js_eval import get_geolocation
import os

# Intentar cargar e inicializar la API de Gemini
try:
    from google import genai
    HAS_GEMINI_LIB = True
except ImportError:
    HAS_GEMINI_LIB = False

# Configuración de la página
st.set_page_config(
    page_title="Central SST 5.0 - Verifty Flow Style",
    page_icon="🛡️",
    layout="wide"
)

# Detectar API Key desde Secrets de Streamlit
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)

# Estado Global de Recepción de Reportes
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
            "Responsable": "Comité SST / Ergonomía",
            "Zona_Cuerpo": "Tronco / Espalda"
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
            "Responsable": "Infraestructura & Soporte IT",
            "Zona_Cuerpo": "Cabeza / Cara"
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
            "Responsable": "Mantenimiento Industrial & Mecatrónica",
            "Zona_Cuerpo": "Brazo derecho"
        }
    ]

if "contador_id" not in st.session_state:
    st.session_state["contador_id"] = len(st.session_state["reportes"]) + 1

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# ========================================================
# BARRA LATERAL (ESTILO VERIFTY FLOW)
# ========================================================
st.sidebar.markdown("""
    <div style="text-align: center; padding-bottom: 15px;">
        <h2 style="color: #4F46E5; margin:0;"><b>verifty</b></h2>
        <span style="font-size: 11px; color: #6B7280;">SST FLOW 5.0</span>
    </div>
""", unsafe_allow_html=True)

# Logos en la barra lateral si existen
col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if os.path.exists("mi_logo.jpg"):
        st.image("mi_logo.jpg", width=65)
with col_sb2:
    if os.path.exists("logo_cun.png"):
        st.image("logo_cun.png", width=65)

st.sidebar.write("---")

st.sidebar.title("🎨 Apariencia & Rol")

tema_seleccionado = st.sidebar.radio(
    "Selecciona el Tema:",
    ["☀️ Modo Claro (Verifty)", "🌙 Modo Oscuro"],
    index=0
)

st.sidebar.write("---")

rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario / Operario (Reporte & Consulta)",
        "🔒 Central Administrador (Dashboard Verifty SST)"
    ]
)

st.sidebar.write("---")

if st.session_state["recepcion_activa"]:
    st.sidebar.success("🟢 **Recepción Pública:** ACTIVA")
else:
    st.sidebar.error("🔴 **Recepción Pública:** PAUSADA")

if GEMINI_KEY:
    st.sidebar.info("🤖 **Gemini IA Copilot:** Conectado")

st.sidebar.write("---")

# Login Administrador
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

# DETERMINAR EL NOMBRE Y ROL DINÁMICO PARA EL SALUDO
if "Central Administrador" in rol_seleccionado and st.session_state["admin_autenticado"]:
    nombre_saludo = "SysAdmin"
    cargo_saludo = "Administrador del Sistema / SST"
elif "Central Administrador" in rol_seleccionado:
    nombre_saludo = "Invitado Admin"
    cargo_saludo = "Pendiente de Autenticación"
else:
    nombre_saludo = "Luis Quintero"
    cargo_saludo = "Operario / Usuario SST"

# ========================================================
# ESTILOS CSS PERSONALIZADOS (ESTILO VERIFTY)
# ========================================================
if tema_seleccionado == "🌙 Modo Oscuro":
    st.markdown("""
        <style>
        .stApp { background-color: #0F172A; color: #F8FAFC; }
        .v-card { background-color: #1E293B; border-radius: 12px; padding: 18px; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3); margin-bottom: 15px; }
        .v-metric-num { font-size: 28px; font-weight: bold; color: #38BDF8; }
        .v-metric-title { font-size: 11px; font-weight: 700; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.5px; }
        .v-metric-sub { font-size: 12px; color: #94A3B8; }
        .v-alert { background-color: #7F1D1D; border-left: 5px solid #EF4444; color: #FECDD3; padding: 12px 18px; border-radius: 8px; font-size: 14px; margin-bottom: 20px; }
        .v-banner { background-color: #1E1B4B; border: 1px solid #4338CA; border-radius: 12px; padding: 16px; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #F4F6FC; color: #1E293B; }
        .v-card { background-color: #FFFFFF; border-radius: 14px; padding: 18px; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 15px; }
        .v-metric-num { font-size: 30px; font-weight: bold; color: #1E293B; }
        .v-metric-title { font-size: 11px; font-weight: 800; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.6px; }
        .v-metric-sub { font-size: 12px; color: #64748B; }
        .v-alert { background-color: #FEF2F2; border-left: 5px solid #EF4444; color: #991B1B; padding: 12px 18px; border-radius: 10px; font-size: 14px; font-weight: 500; margin-bottom: 20px; }
        .v-banner { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 16px; margin-bottom: 20px; }
        .v-progress-bg { background-color: #EEF2FF; border-radius: 10px; height: 10px; overflow: hidden; margin-top: 4px; }
        .v-progress-fill { background: linear-gradient(90deg, #6366F1 0%, #3B82F6 100%); height: 100%; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

# ========================================================
# HEADER ESTILO NAVBAR VERIFTY CON SALUDO DINÁMICO
# ========================================================
col_head_left, col_head_right = st.columns([3, 1])

with col_head_left:
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:15px;">
            <div>
                <h2 style="margin:0; font-size:26px; font-weight:800; color:#4F46E5;">Hola, {nombre_saludo}</h2>
                <p style="margin:0; font-size:14px; color:#64748B;">Panel de Seguridad y Salud en el Trabajo | CUN & Verifty Flow</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_head_right:
    st.markdown(f"""
        <div style="text-align:right;">
            <p style="margin:0; font-size:12px; font-weight:600; color:#64748B;">Martes, 18 de Agosto de 2026</p>
            <span style="background-color:#EEF2FF; color:#4338CA; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:bold;">{cargo_saludo} 🔔</span>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# BANNER DE CONFIGURACIÓN Y ALERTA NORMATIVA
st.markdown("""
    <div class="v-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-weight:bold; color:#4F46E5; font-size:14px;">⚙️ Configura tu empresa: 2/7 pasos completados</span><br>
                <span style="font-size:12px; color:#64748B;">Haz clic en el módulo para continuar la implementación de ISO 45001</span>
            </div>
            <div>
                <span style="background-color:#4F46E5; color:white; padding:6px 16px; border-radius:20px; font-size:12px; font-weight:bold;">28% listo</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="v-alert">
        ⚠️ <b>5 accidentes graves o mortales sin reportar a Mintrabajo</b> — Resolución 1401 de 2014
    </div>
""", unsafe_allow_html=True)

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

# Diagnóstico Heurístico Avanzado
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
    <div style="background-color:#F8FAFC; padding:18px; border-radius:12px; border:1px solid #CBD5E1; margin-top:10px;">
    <h4 style="color:#4F46E5; margin-top:0px;">🔬 Dictamen Técnico de Inspección Automática (SST 5.0)</h4>
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
                        "Responsable": "Por Asignar",
                        "Zona_Cuerpo": "Tronco / Espalda"
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
                <div class="v-card">
                <b>🆔 Número Único:</b> {mr['ID']} | <b>Ubicación:</b> {mr['Ubicación']}<br>
                <b>Categoría:</b> {mr['Tipo Riesgo']} | <b>Severidad:</b> {mr['Severidad']}<br>
                <b>Descripción:</b> {mr['Descripción']}<br>
                <b>📌 Estado Actual:</b> <code>{mr['Estado']}</code> | <b>Responsable:</b> {mr['Responsable']}<br>
                <b>💬 Respuesta Oficial:</b> {mr['Respuesta_Admin']}
                </div>
                """, unsafe_allow_html=True)

# ========================================================
# ROL 2: CENTRAL ADMINISTRADOR (DASHBOARD TIPO VERIFTY FLOW)
# ========================================================
else:
    if not st.session_state["admin_autenticado"]:
        st.warning("🔒 Acceso Restringido - Central Empresarial Verifty SST")
        st.info("Ingresa tus credenciales en el menú lateral para desbloquear el Dashboard.")
        st.markdown("""
        * **Usuario Administrador:** `SysAdmin`
        * **Contraseña de Acceso:** `097`
        """)
    else:
        df_rep = pd.DataFrame(st.session_state["reportes"])

        # GRID PRINCIPAL DE TARJETAS TIPO VERIFTY
        col_m1, col_m2, col_m3, col_m4 = st.columns([1, 1, 1.4, 1.2])

        with col_m1:
            st.markdown(f"""
                <div class="v-card">
                    <div class="v-metric-title">Reportes del Mes</div>
                    <div class="v-metric-num">{len(df_rep)}</div>
                    <div class="v-metric-sub">Actos y condiciones inseguras</div>
                </div>
                <div class="v-card">
                    <div class="v-metric-title">Tareas Pendientes</div>
                    <div class="v-metric-num" style="color:#F59E0B;">{len(df_rep[df_rep["Estado"].str.contains("Pendiente|Nuevo")])}</div>
                    <div class="v-metric-sub">Esperando acción en la empresa</div>
                </div>
                <div class="v-card">
                    <div class="v-metric-title">Incidentes del Año</div>
                    <div class="v-metric-num">{len(df_rep)}</div>
                    <div class="v-metric-sub">Sin lesión, registrados en 2026</div>
                </div>
            """, unsafe_allow_html=True)

        with col_m2:
            st.markdown(f"""
                <div class="v-card">
                    <div class="v-metric-title">Acciones Activas</div>
                    <div class="v-metric-num">{len(df_rep[df_rep["Estado"].str.contains("Gestión|Revisión")])}</div>
                    <div class="v-metric-sub">En gestión operativa</div>
                </div>
                <div class="v-card">
                    <div class="v-metric-title">Instancias Completadas</div>
                    <div class="v-metric-num" style="color:#10B981;">{len(df_rep[df_rep["Estado"].str.contains("Atendido|Cerrado")])}</div>
                    <div class="v-metric-sub">Flujos terminados este mes</div>
                </div>
                <div class="v-card">
                    <div class="v-metric-title">Días Perdidos</div>
                    <div class="v-metric-num">172</div>
                    <div class="v-metric-sub">Incapacidad por accidentes</div>
                </div>
            """, unsafe_allow_html=True)

        with col_m3:
            st.markdown("""
                <div class="v-card">
                    <div class="v-metric-title">🤺 Zonas del Cuerpo Afectadas</div>
                    <div style="margin-top:10px; font-size:12px;">
                        <b>Cabeza / Cara</b> <span style="float:right;">6</span>
                        <div class="v-progress-bg"><div class="v-progress-fill" style="width:75%;"></div></div>
                    </div>
                    <div style="margin-top:8px; font-size:12px;">
                        <b>Tronco / Espalda</b> <span style="float:right;">6</span>
                        <div class="v-progress-bg"><div class="v-progress-fill" style="width:75%;"></div></div>
                    </div>
                    <div style="margin-top:8px; font-size:12px;">
                        <b>Brazo derecho</b> <span style="float:right;">6</span>
                        <div class="v-progress-bg"><div class="v-progress-fill" style="width:75%;"></div></div>
                    </div>
                    <div style="margin-top:8px; font-size:12px;">
                        <b>Brazo izquierdo</b> <span style="float:right;">3</span>
                        <div class="v-progress-bg"><div class="v-progress-fill" style="width:40%;"></div></div>
                    </div>
                    <div style="margin-top:8px; font-size:12px;">
                        <b>Pierna derecha</b> <span style="float:right;">3</span>
                        <div class="v-progress-bg"><div class="v-progress-fill" style="width:40%;"></div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col_m4:
            st.markdown("""
                <div class="v-card">
                    <div class="v-metric-title">Instancias Activas</div>
                    <div class="v-metric-num">8</div>
                    <div class="v-metric-sub">Flujos en ejecución ahora</div>
                </div>
                <div class="v-card">
                    <div class="v-metric-title">Accidentes del Año</div>
                    <div class="v-metric-num" style="color:#EF4444;">24</div>
                    <div class="v-metric-sub">Accidentes de trabajo en 2026</div>
                </div>
                <div class="v-card">
                    <div class="v-metric-title">Índice de Frecuencia</div>
                    <div class="v-metric-num">0</div>
                    <div class="v-metric-sub">Último mes calculated con HHT</div>
                </div>
            """, unsafe_allow_html=True)

        st.write("---")

        # PESTAÑAS DE CONTROL COMPLETO
        tab_executive, tab_copilot, tab_management, tab_map, tab_controls, tab_database = st.tabs([
            "📈 1. Tendencia & Gráficos", 
            "🤖 2. Copilot Gemini IA & Causa Raíz", 
            "✍️ 3. Gestión & Respuesta de Casos", 
            "🗺️ 4. Sala de Crisis & Mapa GPS", 
            "🎛️ 5. Switch Master On/Off & Ajustes", 
            "💾 6. BBDD Consolidada & Exportación"
        ])

        with tab_executive:
            st.subheader("📉 Tendencia de Accidentalidad e Histórico de Instancias")
            col_t1, col_t2 = st.columns([1.5, 1])
            with col_t1:
                st.markdown("##### 📌 Distribución por Categorías de Riesgo")
                st.bar_chart(df_rep["Tipo Riesgo"].value_counts())
            with col_t2:
                st.markdown("##### 🏢 Severidad de Eventos")
                st.bar_chart(df_rep["Severidad"].value_counts())

        with tab_copilot:
            st.subheader("🤖 Asistente Virtual Copilot IA (Analítica Avanzada Verifty)")
            ids_disponibles = [r["ID"] for r in st.session_state["reportes"]]
            sel_id_ia = st.selectbox("Seleccionar Reporte Único para Análisis de Causa Raíz:", ids_disponibles)

            rep_ia = next(r for r in st.session_state["reportes"] if r["ID"] == sel_id_ia)

            st.markdown(f"""
            <div class="v-card">
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
                        st.markdown(f'<div style="background-color:#F8FAFC; padding:18px; border-radius:12px; border:1px solid #CBD5E1; color:#0F172A;">{respuesta_gemini}</div>', unsafe_allow_html=True)
                else:
                    st.info("💡 **Dictamen del Motor Heurístico Verifty (Matriz SST 5.0):**")
                    html_diagnostico = generar_analisis_avanzado_sst(rep_ia)
                    st.markdown(html_diagnostico, unsafe_allow_html=True)

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

        with tab_map:
            st.subheader("🗺️ Sala de Crisis & Mapa de Calor Georreferenciado")
            df_mapa = df_rep.rename(columns={"Latitud": "lat", "Longitud": "lon"})
            st.map(df_mapa[["lat", "lon"]], zoom=13)

        with tab_controls:
            st.subheader("🎛️ Centro de Mando Master & Disponibilidad del Servicio")
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

        with tab_database:
            st.subheader("💾 Consolidado General Registrado por Usuario")
            user_filter = st.selectbox("Filtrar BBDD por Usuario:", ["Todos los Usuarios"] + list(df_rep["Usuario"].unique()))
            df_export = df_rep[df_rep["Usuario"] == user_filter] if user_filter != "Todos los Usuarios" else df_rep
            st.dataframe(df_export, use_container_width=True)

            csv_export = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Consolidada (CSV / Excel)",
                data=csv_export,
                file_name="Base_Datos_SST_Verifty_CUN.csv",
                mime="text/csv"
            )