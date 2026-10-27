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

# Estilos CSS Avanzados
st.markdown("""
    <style>
    .main-title {font-size:26px; font-weight:bold; color:#0F172A; margin-bottom:0px;}
    .sub-title {font-size:14px; color:#475569; margin-bottom:15px;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:5px 12px; border-radius:15px; font-weight:bold;}
    
    .status-online {background-color:#DCFCE7; color:#15803D; border:1px solid #86EFAC; padding:6px 14px; border-radius:20px; font-weight:bold; display:inline-block; text-align:center;}
    .status-offline {background-color:#FEE2E2; color:#B91C1C; border:1px solid #FCA5A5; padding:6px 14px; border-radius:20px; font-weight:bold; display:inline-block; text-align:center;}
    
    .report-card-admin {background-color:#F8FAFC; padding:16px; border-radius:10px; border-left:5px solid #0284C7; margin-bottom:12px;}
    .report-card-user {background-color:#F0FDF4; padding:16px; border-radius:10px; border-left:5px solid #16A34A; margin-bottom:12px;}
    .ai-box {background-color:#F8FAFC; padding:18px; border-radius:10px; border:1px solid #CBD5E1; margin-top:10px; line-height:1.6;}
    </style>
""", unsafe_allow_html=True)

# ========================================================
# ENCABEZADO CON LOGOS EN LAS ESQUINAS
# ========================================================
col_logo_app, col_header, col_logo_cun, col_status = st.columns([1, 4, 1, 1.2])

with col_logo_app:
    if os.path.exists("mi_logo.jpg"):
        st.image("mi_logo.jpg", width=90)
    else:
        st.markdown("🦉")

with col_header:
    st.markdown('<p class="main-title">🏢 Central 360° de Control Empresarial SST 5.0</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Sistema Integrado de Gestión, Gobernanza Algorítmica & Respuesta a Incidentes | Semillero CUN</p>', unsafe_allow_html=True)

with col_logo_cun:
    if os.path.exists("logo_cun.png"):
        st.image("logo_cun.png", width=90)
    else:
        st.markdown("🏛️ **CUN**")

with col_status:
    st.write("")
    if st.session_state["recepcion_activa"]:
        st.markdown('<div class="status-online">🟢 EN LÍNEA</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">🔴 PAUSADO</div>', unsafe_allow_html=True)

st.write("---")

# ========================================================
# MENÚ LATERAL CON LOGOS MÁS PEQUEÑOS Y CONTROL DE ACCESO
# ========================================================
if os.path.exists("logo_cun.png"):
    st.sidebar.image("logo_cun.png", use_container_width=True)

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
    st.sidebar.success("🟢 **Recepción Pública:** ACTIVA")
else:
    st.sidebar.error("🔴 **Recepción Pública:** PAUSADA")

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