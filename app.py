import streamlit as st
import random

# -------------------------
# Configuración básica
# -------------------------
st.set_page_config(page_title="Ideas al Vuelo", page_icon="💡")

st.title("💡 IDEAS AL VUELO")
st.caption("Un juego para despertar tu creatividad — versión Streamlit")

# -------------------------
# Datos base
# -------------------------
RETOS_BASE = [
    "Inventa un nuevo animal combinando dos existentes.",
    "Da un uso inesperado para una cuchara.",
    "Imagina un superpoder que nadie querría tener.",
    "Si pudieras cambiar el color del cielo, ¿cuál pondrías y por qué?",
    "Crea una nueva asignatura para el colegio.",
    "Describe cómo sería un mundo sin gravedad.",
    "Inventa una palabra nueva y di qué significa.",
    "Imagina una comida que nunca existirá en la vida real."
]

# -------------------------
# Estado inicial
# -------------------------
def init_state():
    if "jugador1" not in st.session_state:
        st.session_state.jugador1 = ""
        st.session_state.jugador2 = ""
        st.session_state.p1 = 0
        st.session_state.p2 = 0
        st.session_state.ronda = 1
        st.session_state.total_rondas = 5
        st.session_state.retos = RETOS_BASE.copy()
        st.session_state.retos_usados = set()
        st.session_state.reto_actual = None
        st.session_state.resp1 = ""
        st.session_state.resp2 = ""
        st.session_state.num_votantes = 1
        st.session_state.votos1 = 0
        st.session_state.votos2 = 0
        st.session_state.juego_terminado = False

init_state()

# -------------------------
# Sidebar (configuración)
# -------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    st.session_state.total_rondas = st.number_input(
        "Número de rondas", min_value=1, max_value=20, value=st.session_state.total_rondas, step=1
    )
    st.session_state.num_votantes = st.number_input(
        "Votantes por ronda (público)", min_value=1, max_value=200, value=st.session_state.num_votantes, step=1
    )
    st.divider()
    if st.button("🔄 Reiniciar juego", type="secondary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_state()
        st.success("Juego reiniciado.")

# -------------------------
# Captura de jugadores
# -------------------------
col_a, col_b = st.columns(2)
with col_a:
    st.session_state.jugador1 = st.text_input("Nombre del jugador 1", value=st.session_state.jugador1)
with col_b:
    st.session_state.jugador2 = st.text_input("Nombre del jugador 2", value=st.session_state.jugador2)

if not st.session_state.jugador1 or not st.session_state.jugador2:
    st.info("Escribe los nombres de ambos jugadores para comenzar.")
    st.stop()

# -------------------------
# Helper: seleccionar reto sin repetir
# -------------------------
def escoger_reto():
    disponibles = [r for i, r in enumerate(st.session_state.retos) if i not in st.session_state.retos_usados]
    if not disponibles:
        # Si se acaban, se reinicia la bolsa (evita quedarse sin reto)
        st.session_state.retos_usados = set()
        disponibles = st.session_state.retos.copy()
    reto = random.choice(disponibles)
    idx = st.session_state.retos.index(reto)
    st.session_state.retos_usados.add(idx)
    return reto

# -------------------------
# Reto actual
# -------------------------
if st.session_state.reto_actual is None and not st.session_state.juego_terminado:
    st.session_state.reto_actual = escoger_reto()

# -------------------------
# Cabecera de ronda y marcador
# -------------------------
left, right = st.columns([2, 1])
with left:
    st.subheader(f"🧭 Ronda {st.session_state.ronda} de {st.session_state.total_rondas}")
with right:
    st.metric(st.session_state.jugador1, st.session_state.p1)
    st.metric(st.session_state.jugador2, st.session_state.p2)

st.write("### 🎯 Reto")
st.info(st.session_state.reto_actual)

# -------------------------
# Respuestas
# -------------------------
st.write("### ✍️ Respuestas")
c1, c2 = st.columns(2)
with c1:
    st.session_state.resp1 = st.text_area(
        f"Respuesta de {st.session_state.jugador1}",
        value=st.session_state.resp1,
        placeholder="Escribe tu idea aquí…",
        height=150,
        key="resp1_textarea"
    )
with c2:
    st.session_state.resp2 = st.text_area(
        f"Respuesta de {st.session_state.jugador2}",
        value=st.session_state.resp2,
        placeholder="Escribe tu idea aquí…",
        height=150,
        key="resp2_textarea"
    )

# -------------------------
# Votación
# -------------------------
st.write("### 🗳️ Votación del público")
st.caption("Ajusta cuántos votos recibió cada jugador (la suma debe coincidir con la cantidad de votantes).")
vc1, vc2 = st.columns(2)
with vc1:
    st.session_state.votos1 = st.number_input(
        f"Votos para {st.session_state.jugador1}",
        min_value=0, max_value=st.session_state.num_votantes, value=st.session_state.votos1, step=1
    )
with vc2:
    st.session_state.votos2 = st.number_input(
        f"Votos para {st.session_state.jugador2}",
        min_value=0, max_value=st.session_state.num_votantes, value=st.session_state.votos2, step=1
    )

suma = st.session_state.votos1 + st.session_state.votos2
if suma != st.session_state.num_votantes:
    st.warning(f"La suma de votos ({suma}) debe ser exactamente {st.session_state.num_votantes}.")
    avanzar_habilitado = False
else:
    avanzar_habilitado = True

# -------------------------
# Avanzar ronda
# -------------------------
col_av1, col_av2, col_av3 = st.columns([1, 1, 2])
with col_av1:
    if st.button("✅ Cerrar ronda", disabled=not avanzar_habilitado):
        # Asignar punto
        if st.session_state.votos1 > st.session_state.votos2:
            st.session_state.p1 += 1
            st.success(f"🏆 {st.session_state.jugador1} gana la ronda")
        elif st.session_state.votos2 > st.session_state.votos1:
            st.session_state.p2 += 1
            st.success(f"🏆 {st.session_state.jugador2} gana la ronda")
        else:
            st.info("🤝 ¡Empate en la ronda!")

        # Pasar a la siguiente ronda o terminar
        st.session_state.ronda += 1
        st.session_state.resp1 = ""
        st.session_state.resp2 = ""
        st.session_state.votos1 = 0
        st.session_state.votos2 = 0

        if st.session_state.ronda > st.session_state.total_rondas:
            st.session_state.juego_terminado = True
        else:
            st.session_state.reto_actual = escoger_reto()

with col_av2:
    if st.button("🎲 Cambiar reto (misma ronda)"):
        st.session_state.reto_actual = escoger_reto()
        st.info("Se cambió el reto para esta misma ronda.")

# -------------------------
# Resultados finales
# -------------------------
st.divider()
st.write("## 📊 Resultados")
st.write(f"**{st.session_state.jugador1}:** {st.session_state.p1} puntos")
st.write(f"**{st.session_state.jugador2}:** {st.session_state.p2} puntos")

if st.session_state.juego_terminado:
    st.success("🎉 ¡Fin del juego!")
    if st.session_state.p1 > st.session_state.p2:
        st.write(f"🏆 **{st.session_state.jugador1} gana el juego de las ideas!**")
    elif st.session_state.p2 > st.session_state.p1:
        st.write(f"🏆 **{st.session_state.jugador2} gana el juego de las ideas!**")
    else:
        st.write("🤝 **¡Empate creativo!**")
