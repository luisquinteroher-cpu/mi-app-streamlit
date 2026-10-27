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

# 1. Estado Global: Activar/Desactivar Recepción de Reportes (Por defecto: True)
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

# Estilos CSS con distintivos (Badges) de estado en línea/fuera de línea
st.markdown("""
    <style>
    .main-title {font-size:30px; font-weight:bold; color:#1E3A8A; margin-bottom:0px;}
    .sub-title {font-size:15px; color:#4B5563; margin-bottom:20px;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:6px 14px; border-radius:20px; font-weight:bold;}
    
    /* Indicadores de Estado en la Esquina */
    .status-online {background-color:#DCFCE7; color:#15803D; border:1px solid #86EFAC; padding:6px 16px; border-radius:20px; font-weight:bold; display:inline-block;}
    .status-offline {background-color:#FEE2E2; color:#B91C1C; border:1px solid #FCA5A5; padding:6px 16px; border-radius:20px; font-weight:bold; display:inline-block;}
    
    .report-card-admin {background-color:#F8FAFC; padding:16px; border-radius:10px; border-left:5px solid #2563EB; margin-bottom:15px;}
    .report-card-user {background-color:#F0FDF4; padding:16px; border-radius:10px; border-left:5px solid #16A34A; margin-bottom:15px;}
    .ai-box {background-color:#F3F4F6; padding:16px; border-radius:10px; border:1px solid #D1D5DB; margin-top:10px;}
    </style>