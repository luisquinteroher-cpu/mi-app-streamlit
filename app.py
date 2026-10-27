import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Aporte Semillero - Luis Quintero", page_icon="🌱", layout="wide")

# Título y presentación
st.title("🌱 Semillero de Investigación")
st.subheader("Plataforma Interactiva - Aporte de Luis Quintero")
st.write("---")

# Sección de bienvenida interactiva
col1, col2 = st.columns(2)

with col1:
    st.header("👤 Registro de Integrante")
    nombre = st.text_input("Escribe tu nombre:")
    rol = st.selectbox("Selecciona tu rol en el semillero:", ["Estudiante", "Investigador", "Docente / Mentor"])
    
    if st.button("Registrar asistencia"):
        if nombre:
            st.success(f"¡Bienvenido/a {nombre}! Quedas registrado/a como **{rol}**.")
        else:
            st.warning("Por favor escribe tu nombre antes de registrarte.")

with col2:
    st.header("📊 Áreas de Interés e Investigación")
    intereses = st.multiselect(
        "¿Qué temas te gustaría desarrollar?",
        ["Inteligencia Artificial", "Análisis de Datos", "Desarrollo Web con Streamlit", "Machine Learning", "Procesamiento de Lenguaje Natural"]
    )
    if intereses:
        st.write("Has seleccionado:")
        for tema in intereses:
            st.write(f"- {tema}")

st.write("---")
st.info("💡 **Aporte al proyecto:** Aplicación desplegada mediante GitHub Codespaces y Streamlit Cloud.")