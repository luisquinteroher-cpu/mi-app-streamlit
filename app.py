import streamlit as st
import pandas as pd
from streamlit_js_eval import get_geolocation

# Configuración inicial de la página
st.set_page_config(
    page_title="SST 5.0 + IA - Semillero CUN",
    page_icon="🛡️",
    layout="wide"
)

# Inicializar estado para guardar los reportes enviados y sesión de login
if "reportes" not in st.session_state:
    st.session_state["reportes"] = [
        {
            "ID": "REP-001", 
            "Usuario": "Operario Planta 1", 
            "Ubicación": "Zona de Embalaje", 
            "Latitud": 4.6097, 
            "Longitud": -74.0817, 
            "Tipo Riesgo": "Ergonómico (Posturas/Cargas/Movimientos Repetitivos)", 
            "Severidad": "Media", 
            "Descripción": "Posturas forzadas por altura inadecuada de la mesa de empaque.", 
            "Estado": "En Revisión",
            "Respuesta_Admin": "Pendiente de visita técnica.",
            "Responsable": "Sin Asignar"
        },
        {
            "ID": "REP-002", 
            "Usuario": "Desarrollador IT", 
            "Ubicación": "Datacenter / Servidores", 
            "Latitud": 4.6110, 
            "Longitud": -74.0825, 
            "Tipo Riesgo": "IT - Infraestructura & Datacenter (Racks/Ruido Servidores/Calor)", 
            "Severidad": "Alta", 
            "Descripción": "Exceso de ruido en servidor secundario y sobrecalentamiento en Rack 2.", 
            "Estado": "Validado / En Gestión",
            "Respuesta_Admin": "Se programó mantenimiento preventivo de ventilación.",
            "Responsable": "Equipo de Infraestructura IT"
        }
    ]

if "admin_autenticado" not in st.session_state:
    st.session_state["admin_autenticado"] = False

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
st.markdown('<p class="main-title">🛡️ Sistema Integrado SST 5.0 + IA & Gestión de Reportes</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Proyecto de Práctica en Investigación | Dirección Nacional de Investigación - CUN</p>', unsafe_allow_html=True)
st.write("---")

# Menú lateral: Selección de Rol y Autenticación
st.sidebar.title("🔐 Control de Acceso")

rol_seleccionado = st.sidebar.selectbox(
    "Selecciona tu perfil/rol:",
    [
        "👷 Usuario / Invitado (Reporte Ciudadano / Puesto)",
        "🔒 Administrador (Acceso Restringido)"
    ]
)

st.sidebar.write("---")

# Validar login si se selecciona el Rol Administrador
if "Administrador" in rol_seleccionado:
    if not st.session_state["admin_autenticado"]:
        st.sidebar.subheader("🔑 Iniciar Sesión de Administrador")
        user_input = st.sidebar.text_input("Usuario:", key="login_user")
        pass_input = st.sidebar.text_input("Contraseña:", type="password", key="login_pass")
        
        if st.sidebar.button("Ingresar"):
            if user_input == "SysAdmin" and pass_input == "097":
                st.session_state["admin_autenticado"] = True
                st.sidebar.success("✅ Sesión iniciada correctamente")
                st.rerun()
            else:
                st.sidebar.error("❌ Usuario o contraseña incorrectos")
    else:
        st.sidebar.success("👤 Sesión Activa: SysAdmin")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["admin_autenticado"] = False
            st.rerun()

st.sidebar.markdown(f"**Perfil activo:** <br><span class='role-badge'>{rol_seleccionado}</span>", unsafe_allow_html=True)
st.sidebar.write("---")

# ========================================================
# ROL 1: USUARIO / INVITADO (CON CÁMARA Y GPS REAL)
# ========================================================
if "Usuario / Invitado" in rol_seleccionado:
    st.header("📝 Módulo de Reporte con Permisos de Cámara y GPS en Tiempo Real")
    st.info("Otorga los permisos en tu navegador para capturar fotos de evidencia y obtener tus coordenadas exactas.")

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre / Identificador del Reportante:", value="Invitado / Anónimo")
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
        descripcion = st.text_area("Descripción detallada de la condición o acto inseguro:")

    with col2:
        st.subheader("📷 Registro Fotográfico (Cámara en Vivo)")
        foto_capturada = st.camera_input("Tomar foto de la condición de riesgo:")
        if foto_capturada:
            st.success("✅ Evidencia fotográfica capturada.")

        st.subheader("📍 Geolocalización Automática")
        st.write("Solicitando coordenadas al navegador GPS:")
        loc = get_geolocation()
        
        if loc and 'coords' in loc:
            lat_real = loc['coords']['latitude']
            lon_real = loc['coords']['longitude']
            st.success(f"✅ GPS Detectado: Latitud {lat_real:.5f}, Longitud {lon_real:.5f}")
        else:
            st.warning("⚠️ No se detectaron permisos de GPS automáticos. Ingresa o ajusta manualmente las coordenadas:")
            lat_real = st.number_input("Latitud GPS:", value=4.6097, format="%.5f")
            lon_real = st.number_input("Longitud GPS:", value=-74.0817, format="%.5f")

    st.write("---")
    if st.button("🚨 Enviar Reporte de SST"):
        if "---" in tipo_riesgo:
            st.warning("⚠️ Por favor selecciona una categoría de riesgo válida (no los encabezados).")
        elif descripcion and ubicacion:
            nuevo_id = f"REP-00{len(st.session_state['reportes']) + 1}"
            nuevo_reporte = {
                "ID": nuevo_id,
                "Usuario": nombre,
                "Ubicación": ubicacion,
                "Latitud": lat_real,
                "Longitud": lon_real,
                "Tipo Riesgo": tipo_riesgo,
                "Severidad": severidad,
                "Descripción": descripcion,
                "Estado": "Pendiente (Nuevo)",
                "Respuesta_Admin": "Reporte registrado. En espera de revisión por el especialista SST.",
                "Responsable": "Por Asignar"
            }
            st.session_state["reportes"].append(nuevo_reporte)
            st.success(f"✅ ¡Reporte **{nuevo_id}** registrado exitosamente con coordenadas ({lat_real:.5f}, {lon_real:.5f})!")
        else:
            st.warning("⚠️ Por favor completa la ubicación y la descripción del reporte.")

# ========================================================
# ROL 2: ADMINISTRADOR (PROTEGIDO CON LOGIN)
# ========================================================
else:
    if not st.session_state["admin_autenticado"]:
        st.warning("🔒 Acceso Restringido")
        st.info("Por favor ingresa las credenciales de administrador en la barra lateral izquierda para continuar.")
        st.markdown("""
        * **Usuario requerido:** `SysAdmin`
        * **Contraseña requerida:** `097`
        """)
    else:
        st.header("🔒 Panel Administrador - Dashboard, Analítica e Interacción BBDD")
        
        df_rep = pd.DataFrame(st.session_state["reportes"])

        tab_dash, tab_gestion, tab_mapa, tab_export = st.tabs([
            "📊 Dashboard & Gráficos", 
            "✍️ Validar, Responder & Editar", 
            "🗺️ Mapa en Tiempo Real", 
            "💾 Almacenamiento & Exportación"
        ])

        # --- TAB 1: DASHBOARD ---
        with tab_dash:
            st.subheader("📈 Analítica Visual de Riesgos y Gestión de SST")
            
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Total Reportes BBDD", len(df_rep))
            col_m2.metric("Nuevos / Pendientes", len(df_rep[df_rep["Estado"].str.contains("Pendiente|Nuevo")]))
            col_m3.metric("Casos Atendidos/Cerrados", len(df_rep[df_rep["Estado"].str.contains("Atendido|Cerrado")]))
            col_m4.metric("Casos Alta/Crítica", len(df_rep[df_rep["Severidad"].isin(["Alta", "Crítica"])]))

            st.write("---")
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                st.markdown("##### 📌 Distribución por Severidad")
                severidad_counts = df_rep["Severidad"].value_counts()
                st.bar_chart(severidad_counts)

            with col_g2:
                st.markdown("##### 🏢 Categorías de Riesgos Reportados")
                riesgo_counts = df_rep["Tipo Riesgo"].value_counts()
                st.bar_chart(riesgo_counts)

        # --- TAB 2: EDITAR Y VALIDAR ---
        with tab_gestion:
            st.subheader("✍️ Centro de Validación y Respuesta de Incidentes")
            lista_ids = [r["ID"] for r in st.session_state["reportes"]]
            id_sel = st.selectbox("Seleccionar ID del Reporte a gestionar:", lista_ids)

            idx = next(i for i, r in enumerate(st.session_state["reportes"]) if r["ID"] == id_sel)
            rep = st.session_state["reportes"][idx]

            st.markdown(f"""
            <div class="report-card">
            <b>ID:</b> {rep['ID']} | <b>Reportante:</b> {rep['Usuario']} | <b>Ubicación:</b> {rep['Ubicación']}<br>
            <b>Categoría:</b> {rep['Tipo Riesgo']} | <b>Severidad:</b> {rep['Severidad']}<br>
            <b>Descripción:</b> {rep['Descripción']}
            </div>
            """, unsafe_allow_html=True)

            with st.form("form_gestion_admin"):
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    nuevo_estado = st.selectbox(
                        "Estado de la Solicitud / Validar:",
                        ["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"],
                        index=["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"].index(rep["Estado"]) if rep["Estado"] in ["Pendiente (Nuevo)", "En Revisión", "Validado / En Gestión", "Atendido / Cerrado", "Rechazado"] else 0
                    )
                    responsable = st.text_input("Asignar Responsable de Caso:", value=rep.get("Responsable", "Especialista SST"))

                with col_a2:
                    respuesta = st.text_area("Respuesta Oficial / Plan de Acción SST:", value=rep.get("Respuesta_Admin", ""))

                btn_guardar = st.form_submit_button("💾 Guardar Cambios en BBDD")

                if btn_guardar:
                    st.session_state["reportes"][idx]["Estado"] = nuevo_estado
                    st.session_state["reportes"][idx]["Responsable"] = responsable
                    st.session_state["reportes"][idx]["Respuesta_Admin"] = respuesta
                    st.success(f"✅ ¡El reporte **{id_sel}** ha sido actualizado correctamente en la Base de Datos!")
                    st.rerun()

        # --- TAB 3: MAPA ---
        with tab_mapa:
            st.subheader("📍 Georreferenciación en Planta")
            df_mapa = df_rep.rename(columns={"Latitud": "lat", "Longitud": "lon"})
            st.map(df_mapa[["lat", "lon"]], zoom=14)

        # --- TAB 4: ALMACENAMIENTO Y DESCARGA BBDD ---
        with tab_export:
            st.subheader("💾 Base de Datos Consolidada de Reportes")
            st.dataframe(df_rep, use_container_width=True)

            csv_data = df_rep.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos Completa (CSV / Excel)",
                data=csv_data,
                file_name="Base_Datos_Reportes_SST_CUN.csv",
                mime="text/csv"
            )