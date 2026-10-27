import streamlit as st
import pandas as pd
import numpy as np

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

    with st.form("form_