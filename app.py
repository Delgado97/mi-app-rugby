import streamlit as st
import pandas as pd
import time
from datetime import datetime
from io import BytesIO
from openpyxl import Workbook
import streamlit.components.v1 as components

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Rugby Keyboard Pro", layout="wide")

# --- TRUCO DE TECLADO (JavaScript) ---
# Este script detecta la tecla y hace clic en el botón invisible correspondiente
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        const key = e.key.toLowerCase();
        // Mapeo de teclas a ID de botones (los crearemos abajo)
        const keyMap = {
            'q': 'btn_placaje_pos',
            'w': 'btn_placaje_neg',
            'a': 'btn_avant',
            's': 'btn_ensayo_juego',
            'p': 'btn_penal',
            'l': 'btn_line_ganado',
            'k': 'btn_line_perdido'
        };
        
        if (keyMap[key]) {
            const btn = doc.getElementById(keyMap[key]);
            if (btn) btn.click();
        }
    });
    </script>
    """,
    height=0,
)

# --- ESTADO DE SESIÓN ---
if 'eventos' not in st.session_state: st.session_state.eventos = []
if 'jugador_actual' not in st.session_state: st.session_state.jugador_actual = ""

def agregar_evento(tipo, jugador=None):
    nuevo = {
        "hora": datetime.now().strftime('%H:%M:%S'),
        "tipo": tipo,
        "jugador": jugador if jugador else "Equipo"
    }
    st.session_state.eventos.append(nuevo)

# --- INTERFAZ ---
st.title("🏉 Rugby Analysis - Keyboard Mode")

# Instrucciones de teclas para que no se te olviden
st.info("⌨️ **Atajos:** Q: Placaje+ | W: Placaje- | A: Avant | S: Ensayo | L: Line+ | K: Line- | P: Penal")

col_main, col_hist = st.columns([2, 1])

with col_main:
    # Input de jugador (se mantiene igual)
    st.session_state.jugador_actual = st.text_input("Dorsal Jugador (escríbelo y déjalo ahí):", value=st.session_state.jugador_actual)
    
    st.subheader("Acciones (Puedes usar teclado o clic)")
    c1, c2, c3 = st.columns(3)
    
    # Creamos los botones con una "ayuda" de HTML para que el JavaScript los encuentre por ID
    with c1:
        if st.button("✅ Placaje Pos (Q)", key="btn_placaje_pos"): 
            agregar_evento("Placaje +", st.session_state.jugador_actual)
        if st.button("❌ Placaje Neg (W)", key="btn_placaje_neg"): 
            agregar_evento("Placaje -", st.session_state.jugador_actual)
            
    with c2:
        if st.button("💨 Avant (A)", key="btn_avant"): 
            agregar_evento("Avant", st.session_state.jugador_actual)
        if st.button("🏉 Ensayo (S)", key="btn_ensayo_juego"): 
            agregar_evento("Ensayo", st.session_state.jugador_actual)

    with c3:
        if st.button("⚠️ Penal (P)", key="btn_penal"): 
            agregar_evento("Penal", st.session_state.jugador_actual)
        if st.button("🟢 Line Ganado (L)", key="btn_line_ganado"): 
            agregar_evento("Line Ganado")
        if st.button("🔴 Line Perdido (K)", key="btn_line_perdido"): 
            agregar_evento("Line Perdido")

with col_hist:
    st.subheader("📋 Historial")
    if st.session_state.eventos:
        df = pd.DataFrame(st.session_state.eventos).iloc[::-1]
        st.table(df)
        
        # Botón de reset
        if st.button("Limpiar Todo"):
            st.session_state.eventos = []
            st.rerun()
    else:
        st.write("Esperando acciones...")
