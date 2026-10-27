import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="SST 5.0 + IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Estilos visuales
st.markdown("""
    <style>
    .main-title {font-size:30px; font-weight:bold; color:#1E3A8A;}
    .sub-title {font-size:16px; color:#4B5563;}
    .role-badge {background-color:#E0E7FF; color:#3730A3; padding:5px 12px; border-radius:15px; font-weight:bold;}
    .card {background-color:#F9FAFB; padding:15px; border-radius:8px; border:1px solid #E5E7EB;}
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="main-title">🛡️ Sistema de Gestión de SST 5.0 e Inteligencia Artificial</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Semillero SST Inteligente | Dirección Nacional de Investigación - CUN</p>', unsafe_allow_html=True)
st.write("---")

# Menú lateral: Selección de Rol y Navegación
st.sidebar.title("🔐 Control de Acceso y Roles")

rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario (Operario / Trabajador)",
        "🔒 Administrador (Especialista SST / Dirección)",
        "👁️ Invitado (Evaluador / Comité Semillero)"
    ]
)

st.sidebar.write("---")
st.sidebar.markdown(f"**Perfil activo:** <br><span class='role-badge'>{rol_seleccionado}</span>", unsafe_allow_html=True)
st.sidebar.write("---")

# ========================================================
# ROL 1: USUARIO (OPERARIO / TRABAJADOR)
# ========================================================
if "Usuario" in rol_seleccionado:
    st.header("👷 Panel del Trabajador - Autocuidado y Prevención")
    st.info("Bienvenido. Este espacio está diseñado para apoyar tu salud ocupacional, prevenir fatiga y garantizar la seguridad en tu puesto de trabajo.")

    tab1, tab2 = st.tabs(["🦺 Verificación de EPP (Visión por IA)", "🧘 Reporte de Fatiga y Pausas Activas"])

    with tab1:
        st.subheader("Detectores de EPP y Zonas de Riesgo")
        st.write("Simulación de detección mediante **Visión por Computador (YOLOv8)** en tu estación de trabajo:")
        
        casco = st.checkbox("Casco de seguridad colocado", value=True)
        chaleco = st.checkbox("Chaleco reflectivo colocado", value=True)
        guantes = st.checkbox("Guantes de protección", value=False)

        if casco and chaleco and guantes:
            st.success("✅ ¡Equipamiento completo! Estás listo para ingresar a la zona operativa.")
        else:
            st.warning("⚠️ Equipamiento incompleto. Se requiere uso de guantes antes de operar maquinaria.")

    with tab2:
        st.subheader("Monitoreo de Carga Biomecánica y Ergonomía")
        nivel_fatiga = st.slider("¿Cómo te sientes físicamente al inicio/mitad de jornada?", 1, 10, 3)
        
        if nivel_fatiga >= 7:
            st.error("🚨 Nivel de fatiga elevado. Se recomienda realizar una pausa activa de 10 minutos e hidratación.")
        else:
            st.success("😊 Nivel de fatiga bajo/moderado. Recuerda mantener posturas ergonómicas recomendadas por la ISO/TS 15066.")

# ========================================================
# ROL 2: ADMINISTRADOR (ESPECIALISTA SST / DIRECCIÓN)
# ========================================================
elif "Administrador" in rol_seleccionado:
    st.header("🔒 Panel de Administración y Gobernanza Algorítmica")
    st.warning("Acceso restringido para la gestión de políticas de seguridad, auditoría de cajas negras y configuración de cobots.")

    tab1, tab2 = st.tabs(["⚙️ Control Biomecánico Robótico (ISO/TS 15066)", "📊 Auditoría e Integración de Modelos"])

    with tab1:
        st.subheader("Simulador de Umbrales en Cobots / Brazos Robóticos")
        st.write("Ajuste de parámetros límite según la **ISO/TS 15066** (Límites de fuerza $140\\text{ N} - 290\\text{ N}$):")

        limite_fuerza = st.number_input("Establecer límite máximo de fuerza (Newtons):", min_value=100, max_value=350, value=200)
        fuerza_medida = st.slider("Fuerza simulada en sensor en tiempo real (N):", 50, 400, 180)

        if fuerza_medida > limite_fuerza:
            st.error(f"🚨 ALERTA DE SEGURIDAD: La fuerza de impacto ({fuerza_medida} N) supera el límite configurado ({limite_fuerza} N). Se activa la parada de emergencia determinista (Capa Intermedia / Human-in-the-Loop).")
        else:
            st.success(f"✅ Operación dentro del rango permitido ({fuerza_medida} N / {limite_fuerza} N).")

    with tab2:
        st.subheader("Configuración de Algoritmos de IA")
        st.multiselect(
            "Activar módulos de detección proactiva en planta:",
            ["Detección de EPP (YOLOv8)", "Análisis de Frecuencia Cardíaca / Wearables", "NLP en Reportes Narrativos de Incidentes", "Mantenimiento Predictivo (LSTM)"],
            default=["Detección de EPP (YOLOv8)", "NLP en Reportes Narrativos de Incidentes"]
        )

# ========================================================
# ROL 3: INVITADO (EVALUADOR / COMITÉ SEMILLERO)
# ========================================================
elif "Invitado" in rol_seleccionado:
    st.header("👁️ Modo Demostración - Proyecto de Investigación Semillero")
    st.write("Vista pública compilada para docentes, evaluadores y participantes del **Semillero de Investigación SST Inteligente**.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
        <h4>📄 Detalles del Proyecto</h4>
        <b>Título:</b> Integración de IA en la SST (SST 5.0)<br>
        <b>Practicante:</b> Luis Eduardo Quintero Hernández<br>
        <b>Programa:</b> Ingeniería de Sistemas (CUN)<br>
        <b>Tutor:</b> Luis Alberto León López<br>
        <b>Calificación:</b> 5.0 / 5.0 ⭐
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h4>🔬 Entregables Consolidados</h4>
        1. Matriz de Control de Literatura Científica<br>
        2. Borrador del Artículo de Investigación<br>
        3. Propuesta de Arquitectura Human-in-the-Loop<br>
        4. Aplicación Web Interactiva en Streamlit Cloud
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.subheader("📚 Muestra de la Matriz de Control de Literatura")
    datos_articulos = {
        "Título": ["Computer Vision for PPE", "IoT Wearables Ergonomics", "GenAI Safety Reporting", "Cobot Safety ISO/TS 15066"],
        "Tecnología": ["YOLOv8 / CNN", "Sensors IMU", "LLM / NLP", "Control Determinista"],
        "Impacto": ["95% precisión", "Reducción de fatiga", "Minería de datos OSHA", "Seguridad robótica"]
    }
    st.dataframe(pd.DataFrame(datos_articulos), use_container_width=True)

st.sidebar.info("💡 Tip: Cambia el rol en el menú lateral para probar cada interfaz.")