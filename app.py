import streamlit as st
import pandas as pd
import time
from datetime import datetime
from io import BytesIO
from openpyxl import Workbook

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Rugby Analysis Pro", layout="wide")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    .crono-text { font-size: 50px !important; font-weight: bold; text-align: center; color: #ff4b4b; }
    .jugador-text { font-size: 30px !important; text-align: center; background-color: #262730; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if 'eventos' not in st.session_state:
    st.session_state.eventos = []
if 'tiempo_inicio' not in st.session_state:
    st.session_state.tiempo_inicio = 0
if 'corriendo' not in st.session_state:
    st.session_state.corriendo = False
if 'jugador_actual' not in st.session_state:
    st.session_state.jugador_actual = ""

# --- FUNCIONES DE LÓGICA ---
def agregar_evento(tipo, jugador=None):
    tiempo = int(st.session_state.tiempo_inicio) # Simplificado para el ejemplo
    nuevo_evento = {
        "tiempo": time.strftime('%M:%S', time.gmtime(st.session_state.tiempo_inicio)),
        "tipo": tipo,
        "jugador": jugador if jugador else "Equipo"
    }
    st.session_state.eventos.append(nuevo_evento)

def generar_excel():
    output = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Análisis de Partido"
    
    # Encabezados
    ws.append(["Tiempo", "Evento", "Jugador"])
    for e in st.session_state.eventos:
        ws.append([e['tiempo'], e['tipo'], e['jugador']])
        
    wb.save(output)
    return output.getvalue()

# --- INTERFAZ ---
st.title("🏉 Panel de Análisis de Rugby")

col_info, col_controles, col_historial = st.columns([1, 2, 1])

with col_info:
    st.subheader("⏱️ Tiempo y Jugador")
    
    # Simulación de cronómetro (Streamlit refresca la página, para un crono real 1:1 se usa un componente JS, pero esto es funcional)
    st.markdown(f'<p class="crono-text">{time.strftime("%M:%S", time.gmtime(st.session_state.tiempo_inicio))}</p>', unsafe_allow_html=True)
    
    if st.button("▶️ Iniciar / Pausar"):
        st.session_state.corriendo = not st.session_state.corriendo
        # Aquí podrías añadir lógica de tiempo real con un loop, pero para análisis manual basta con marcar el punto
    
    if st.button("🔄 Reset"):
        st.session_state.tiempo_inicio = 0
        st.session_state.eventos = []

    st.markdown("---")
    st.session_state.jugador_actual = st.text_input("Dorsal Jugador:", value=st.session_state.jugador_actual)
    st.markdown(f'<p class="jugador-text">JUGADOR: {st.session_state.jugador_actual if st.session_state.jugador_actual else "-"}</p>', unsafe_allow_html=True)

with col_controles:
    st.subheader("⚡ Acciones Rápidas")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Placaje Pos"): agregar_evento("placaje_positivo", st.session_state.jugador_actual)
        if st.button("❌ Placaje Neg"): agregar_evento("placaje_negativo", st.session_state.jugador_actual)
        if st.button("💨 Avant"): agregar_evento("avant", st.session_state.jugador_actual)
    
    with c2:
        if st.button("🏉 Ensayo Juego"): agregar_evento("ensayo_juego", st.session_state.jugador_actual)
        if st.button("🏗️ Ensayo Maul"): agregar_evento("ensayo_maul")
        if st.button("⚠️ Penal"): agregar_evento("penal", st.session_state.jugador_actual)

    with c3:
        if st.button("🚀 Accion Pos"): agregar_evento("accion_positiva", st.session_state.jugador_actual)
        if st.button("🔻 Accion Neg"): agregar_evento("accion_negativa", st.session_state.jugador_actual)
        if st.button("🧹 Borrar Jugador"): st.session_state.jugador_actual = ""

    st.subheader("🏟️ Formaciones Fijas")
    f1, f2 = st.columns(2)
    with f1:
        if st.button("🟢 Scrum Ganado"): agregar_evento("scrum_ganado")
        if st.button("🔴 Scrum Perdido"): agregar_evento("scrum_perdido")
    with f2:
        if st.button("🟢 Lineout Ganado"): agregar_evento("lineout_ganado")
        if st.button("🔴 Lineout Perdido"): agregar_evento("lineout_perdido")

with col_historial:
    st.subheader("📋 Historial")
    if st.session_state.eventos:
        df = pd.DataFrame(st.session_state.eventos).iloc[::-1] # Ver últimos primero
        st.table(df)
        
        excel_data = generar_excel()
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name=f"Analisis_Rugby_{datetime.now().strftime('%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No hay eventos registrados aún.")