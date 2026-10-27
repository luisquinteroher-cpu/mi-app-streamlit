import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="SST 5.0 + IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main-title {font-size:32px; font-weight:bold; color:#1E3A8A;}
    .sub-title {font-size:18px; color:#4B5563;}
    .highlight-box {background-color:#F3F4F6; padding:15px; border-radius:10px; border-left:5px solid #10B981;}
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="main-title">🛡️ Integración de IA en Seguridad y Salud en el Trabajo (SST 5.0)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Proyecto de Práctica en Investigación | Dirección Nacional de Investigación - CUN</p>', unsafe_allow_html=True)
st.write("---")

# Menú lateral de navegación
st.sidebar.image("https://cun.edu.co/assets/img/logo-cun.png", width=180)
st.sidebar.title("Navegación del Proyecto")
opcion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "📌 Inicio y Presentación",
        "🧠 Taxonomía Tecnológica IA",
        "📐 Gobernanza y Normativa ISO",
        "📚 Matriz de Literatura"
    ]
)

st.sidebar.write("---")
st.sidebar.info("""
**Investigador:** Luis Eduardo Quintero H.  
**Programa:** Ingeniería de Sistemas  
**Tutor:** Luis Alberto León López  
**Periodo:** Ago - Oct 2026  
""")

# ==========================================
# 1. INICIO Y PRESENTACIÓN
# ==========================================
if opcion == "📌 Inicio y Presentación":
    st.header("🌱 Bienvenida al Semillero de SST Inteligente")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        Esta plataforma web sintetiza los avances y resultados alcanzados durante la práctica técnica en investigación enfocada en la 
        **Integración de la Inteligencia Artificial en la Seguridad y Salud en el Trabajo (SST 5.0)**.
        
        El objetivo principal fue analizar la transición desde un paradigma **reactivo** (basado en inspecciones manuales y análisis post-accidente) 
        hacia un modelo **cognitivo y predictivo**, apoyado en sensores IoT, visión artificial y sistemas *Human-in-the-Loop*.
        """)
        
        with st.expander("🎯 Objetivos de la Práctica"):
            st.markdown("""
            * **General:** Analizar la integración de la IA en la SST mediante una revisión sistemática de literatura para identificar beneficios, oportunidades y barreras de gobernanza.
            * **Específicos:**
              1. Ejecutar un protocolo riguroso de búsqueda sistemática en bases de datos científicas.
              2. Consolidar una Matriz de Control con artículos seleccionados.
              3. Diseñar una propuesta de arquitectura de gobernanza ética y multinivel (*Human-in-the-Loop*).
            """)

    with col2:
        st.markdown("""
        <div class="highlight-box">
        <h4>📋 Ficha Técnica</h4>
        <b>Estudiante:</b> Luis Eduardo Quintero<br>
        <b>Institución:</b> CUN<br>
        <b>Modalidad:</b> Práctica en Investigación<br>
        <b>Calificación Final:</b> 5.0 / 5.0 ⭐
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 2. TAXONOMÍA TECNOLÓGICA IA
# ==========================================
elif opcion == "🧠 Taxonomía Tecnológica IA":
    st.header("🧠 Aplicaciones de la Inteligencia Artificial en SST")
    st.write("Explora cómo las diferentes disciplinas de la IA transforman la prevención de riesgos laborales:")

    categoria = st.selectbox(
        "Selecciona un Dominio Tecnológico:",
        [
            "Visión por Computador (CV)",
            "Sensórica e IoT (Wearables)",
            "Analítica Predictiva & ML",
            "IA Generativa & NLP"
        ]
    )

    if categoria == "Visión por Computador (CV)":
        st.subheader("👁️ Visión por Computador y Detección de Objetos")
        st.write("**Modelos Clave:** YOLOv5, YOLOv8, Faster R-CNN")
        st.markdown("""
        * **Monitoreo de EPP:** Verificación automatizada en tiempo real del uso de cascos, chalecos y guantes mediante cámaras CCTV.
        * **Invasión de Zonas de Peligro:** Alertas instantáneas cuando un trabajador ingresa al radio de operación de maquinaria pesada o brazos robóticos.
        * **Estimación de Pose (3D):** Evaluación de ergonomía en tiempo real para detectar posturas forzadas.
        """)
        
    elif categoria == "Sensórica e IoT (Wearables)":
        st.subheader("⌚ Sensors Inteligentes y Fusión Sensorial")
        st.write("**Dispositivos:** IMU, EEG, ECG, Parches fisiológicos")
        st.markdown("""
        * **Gestión de Fatiga:** Detección biomecánica y cardíaca de somnolencia o agotamiento térmico en jornadas exigentes.
        * **Prevención de Trastornos Musculoesqueléticos:** Alertas táctiles/sonoras ante levantamiento incorrecto de cargas.
        """)

    elif categoria == "Analítica Predictiva & ML":
        st.subheader("📊 Analítica Predictiva y Aprendizaje Automático")
        st.write("**Algoritmos:** Random Forest, XGBoost, Redes LSTM")
        st.markdown("""
        * **Mantenimiento Predictivo:** Anticipación de fallas mecánicas en maquinaria para evitar colapsos y reducir tiempos de parada (downtime en 20-30%).
        * **Análisis Causa Raíz (RCA):** Identificación de patrones en históricos de incidentes laborales.
        """)

    elif categoria == "IA Generativa & NLP":
        st.subheader("💬 IA Generativa y Procesamiento de Lenguaje Natural")
        st.write("**Modelos:** LLMs, Transformers, Modelos de Difusión")
        st.markdown("""
        * **Minería de Reportes:** Análisis automatizado de textos narrativos de incidentes (ej. bases de datos OSHA).
        * **Simulación de Escenarios:** Generación sintética de eventos *near-miss* para entrenamiento virtual.
        """)

# ==========================================
# 3. GOBERNANZA Y NORMATIVA ISO
# ==========================================
elif opcion == "📐 Gobernanza y Normativa ISO":
    st.header("📐 Arquitectura de Gobernanza e Integración Normativa")
    
    st.subheader("🛡️ Estándares Internacionales de Seguridad en Robótica")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**ISO 10218-1/2:** Define los requisitos de seguridad e integridad física para instalaciones y robots industriales.")
    with col2:
        st.info("**ISO/TS 15066:** Modula las operaciones colaborativas con cobots, estableciendo límites biomecánicos de fuerza y presión (140 N - 290 N).")

    st.write("---")
    st.subheader("⚙️ Simulador de Verificación en Tiempo Real (Runtime Assurance)")
    st.write("Simula la respuesta del sistema ante la detección de fuerza o cercanía en un entorno robótico colaborativo:")

    fuerza = st.slider("Fuerza de impacto detectada (Newtons):", min_value=50, max_value=400, value=120)

    if fuerza <= 140:
        st.success(f"✅ Fuerza dentro del rango seguro ({fuerza} N). Operación normal continuada.")
    elif 140 < fuerza <= 290:
        st.warning(f"⚠️ Alerta Biomecánica ({fuerza} N). Reduciendo velocidad del cobot y emitiendo advertencia táctil.")
    else:
        st.error(f"🚨 LÍMITE DE SEGURIDAD SUPERADO ({fuerza} N). Activando parada de emergencia determinista (Capa Intermedia / CBF).")

# ==========================================
# 4. MATRIZ DE LITERATURA
# ==========================================
elif opcion == "📚 Matriz de Literatura":
    st.header("📚 Matriz de Control y Análisis de Artículos")
    st.write("Muestra de los artículos procesados en la revisión sistemática de literatura durante la práctica:")

    # Datos de ejemplo basados en el semillero
    datos_articulos = {
        "Título del Artículo": [
            "Computer Vision for PPE Detection in Construction",
            "IoT Wearables for Occupational Ergonomics",
            "Generative AI in Safety Incident Reporting",
            "Human-Robot Collaboration Safety via ISO/TS 15066"
        ],
        "Tecnología IA": ["Visión por Computador (YOLOv8)", "IoT & IMU Sensors", "LLMs / NLP", "Control Determinista / CBF"],
        "Dominio SST": ["Seguridad Física / EPP", "Ergonomía / TME", "Gestión de Incidentes", "Robótica Colaborativa"],
        "Aporte Clave": ["Precisión del 95% en detección", "Reducción del fatiga en 12 semanas", "Minería de texto de reportes OSHA", "Cumplimiento de límites de fuerza"]
    }

    df = pd.DataFrame(datos_articulos)
    st.dataframe(df, use_container_width=True)
    st.caption("Matriz compilada como parte de los entregables del Semillero SST Inteligente.")