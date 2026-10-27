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
    page_title="SST 5.0 + Gemini IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Detectar API Key desde Secrets de Streamlit
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", None)

# Estado Global: Activar/Desactivar Recepción de Reportes (Por defecto: True)
if "recepcion_activa" not in st.session_state:
    st.session_state["recepcion_activa"] = True

# Inicializar BBDD de reportes
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
        }
    ]

if "contador_id" not in st.session_state:
    st.session_state["contador_id"] = len(st.session_state["reportes"]) + 1

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

# Estilos CSS con distintivos (Badges)
st.markdown("""
    <style>
    .main-title {font-size:30px; font-weight:bold; color:#1E3A8A; margin-bottom:0px;}
    .sub-title {font-size:15px; color:#4B5563; margin-bottom:20px;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:6px 14px; border-radius:20px; font-weight:bold;}
    
    .status-online {background-color:#DCFCE7; color:#15803D; border:1px solid #86EFAC; padding:6px 16px; border-radius:20px; font-weight:bold; display:inline-block;}
    .status-offline {background-color:#FEE2E2; color:#B91C1C; border:1px solid #FCA5A5; padding:6px 16px; border-radius:20px; font-weight:bold; display:inline-block;}
    
    .report-card-admin {background-color:#F8FAFC; padding:16px; border-radius:10px; border-left:5px solid #2563EB; margin-bottom:15px;}
    .report-card-user {background-color:#F0FDF4; padding:16px; border-radius:10px; border-left:5px solid #16A34A; margin-bottom:15px;}
    .ai-box {background-color:#F3F4F6; padding:16px; border-radius:10px; border:1px solid #D1D5DB; margin-top:10px;}
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal y Badge de Estado en Esquina
col_header, col_status = st.columns([3, 1])

with col_header:
    st.markdown('<p class="main-title">🛡️ Sistema Integrado SST 5.0 + Gemini IA</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Plataforma de Control Empresarial | Dirección Nacional de Investigación - CUN</p>', unsafe_allow_html=True)

with col_status:
    st.write("")
    if st.session_state["recepcion_activa"]:
        st.markdown('<div class="status-online">🟢 Servicio EN LÍNEA</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">🔴 Servicio FUERA DE LÍNEA</div>', unsafe_allow_html=True)

st.write("---")

# Menú Lateral
st.sidebar.title("🔐 Control de Acceso")

rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario / Invitado (Reporte & Consulta Personal)",
        "🔒 Administrador (Super Dashboard + Switch On/Off)"
    ]
)

st.sidebar.write("---")

if st.session_state["recepcion_activa"]:
    st.sidebar.success("🟢 **Recepción:** ACTIVA")
else:
    st.sidebar.error("🔴 **Recepción:** PAUSADA")

if GEMINI_KEY:
    st.sidebar.info("🤖 **Gemini IA:** Conectado")

st.sidebar.write("---")

# Login de Administrador
if "Administrador" in rol_seleccionado:
    if not st.session_state["admin_autenticado"]:
        st.sidebar.subheader("🔑 Iniciar Sesión SysAdmin")
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

# ========================================================
# ROL 1: USUARIO / INVITADO
# ========================================================
if "Usuario / Invitado" in rol_seleccionado:
    st.header("👷 Módulo de Trabajo para Usuarios & Operarios")
    
    tab_nuevo_rep, tab_mis_reportes = st.tabs(["📝 Registrar Nuevo Reporte (ID Único)", "📋 Consultar Mis Reportes Registrados"])

    with tab_nuevo_rep:
        if not st.session_state["recepcion_activa"]:
            st.error("🚫 **El servicio de recepción de reportes se encuentra temporalmente FUERA DE LÍNEA.**")
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
                        "Respuesta_Admin": "Reporte recibido. En cola de revisión por el equipo de SST.",
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
# ROL 2: ADMINISTRADOR
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
        st.header("🔒 Centro de Control Empresarial & Copilot Gemini IA")
        
        st.markdown("### 🎛️ Control Global del Servicio de Reportes")
        col_sw1, col_sw2 = st.columns([2, 2])
        
        with col_sw1:
            estado_switch = st.toggle("🟢 Prender / 🔴 Apagar recepción pública de reportes", value=st.session_state["recepcion_activa"])
            if estado_switch != st