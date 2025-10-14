import streamlit as st
import random

# -------------------------
# CONFIGURACIÓN INICIAL
# -------------------------
st.set_page_config(page_title="Ideas al Vuelo", page_icon="💡")

st.title("💡 IDEAS AL VUELO")
st.caption("Un juego para despertar tu creatividad — versión Streamlit")

# -------------------------
# LISTA DE RETOS
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
# ESTADO INICIAL
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

        # 🔧 Flag para evitar la excepción: reseteo diferido de widgets
        st.session_state.reset_votos_pendiente = False

init_state()

# -------------------------
# SIDEBAR (CONFIGURACIÓN)
# -------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    st.number_input(
        "Número de rondas", min_value=1, max_value=20, step=1, format="%d",
        key="total_rondas"
    )
    st.number_input(
        "Votantes por ronda", min_value=1, max_value=200, step=1, format="%d",
        key="num_votantes"
    )
    st.divider()
    if st.button("🔄 Reiniciar juego", type="secondary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        init_state()
        st.success("Juego reiniciado.")
        st.rerun()

# -------------------------
# CAPTURA DE JUGADORES
# -------------------------
col_a, col_b = st.columns(2)
with col_a:
    st.session_state.jugador1 = st.text_input("Nombre del jugador 1", value=st.session_state.jugador1)
with col_b:
    st.session_state.jugador2 = st.text_input("Nombre del jugador 2", value=st.session_state.jugador2)

if not st.session_state.jugador1 or not st.session_state.jugador2:
    st.info("👉 Escribe los nombres de ambos jugadores para comenzar.")
    st.stop()

# -------------------------
# 🔧 RESETEO DIFERIDO DE VOTOS (antes de crear los widgets)
# -------------------------
if st.session_state.reset_votos_pendiente:
    # Aquí SÍ es seguro modificar claves de widgets antes de crearlos en esta ejecución
    st.session_state.votos1 = 0
    st.session_state.votos2 = 0
    st.session_state.reset_votos_pendiente = False

# -------------------------
# FUNCIÓN PARA ELEGIR RETO NUEVO
# -------------------------
def escoger_reto():
    disponibles = [r for i, r in enumerate(st.session_state.retos) if i not in st.session_state.retos_usados]
    if not disponibles:
        st.session_state.retos_usados = set()
        disponibles = st.session_state.retos.copy()
    reto = random.choice(disponibles)
    idx = st.session_state.retos.index(reto)
    st.session_state.retos_usados.add(idx)
    return reto

# -------------------------
# DEFINIR RETO ACTUAL
# -------------------------
if st.session_state.reto_actual is None and not st.session_state.juego_terminado:
    st.session_state.reto_actual = escoger_reto()

# -------------------------
# ENCABEZADO Y MARCADOR
# -------------------------
left, right = st.columns([2, 1])
with left:
    st.subheader(f"🧭 Ronda {st.session_state.ronda} de {st.session_state.total_rondas}")
with right:
    st.metric(st.session_state.jugador1, st.session_state.p1)
    st.metric(st.session_state.jugador2, st.session_state.p2)

st.write("### 🎯 Reto creativo")
st.info(st.session_state.reto_actual)

# -------------------------
# RESPUESTAS
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
# VOTACIÓN
# -------------------------
st.write("### 🗳️ Votación del público")
st.caption("Introduce cuántos votos obtuvo cada jugador (la suma debe coincidir con los votantes).")

vc1, vc2 = st.columns(2)
with vc1:
    st.number_input(
        f"Votos para {st.session_state.jugador1}",
        min_value=0, max_value=st.session_state.num_votantes, step=1, format="%d",
        key="votos1"
    )
with vc2:
    st.number_input(
        f"Votos para {st.session_state.jugador2}",
        min_value=0, max_value=st.session_state.num_votantes, step=1, format="%d",
        key="votos2"
    )

suma = st.session_state.votos1 + st.session_state.votos2
if suma != st.session_state.num_votantes:
    st.warning(f"La suma de votos ({suma}) debe ser exactamente {st.session_state.num_votantes}.")
    avanzar_habilitado = False
else:
    avanzar_habilitado = True

# -------------------------
# BOTONES DE ACCIÓN
# -------------------------
col_av1, col_av2, _ = st.columns([1, 1, 2])

with col_av1:
    if st.button("✅ Cerrar ronda", disabled=not avanzar_habilitado):
        # Asignar punto
        if st.session_state.votos1 > st.session_state.votos2:
            st.session_state.p1 += 1
        elif st.session_state.votos2 > st.session_state.votos1:
            st.session_state.p2 += 1

        # Avanzar
        st.session_state.ronda += 1

        # Limpiar respuestas
        st.session_state.resp1 = ""
        st.session_state.resp2 = ""

        # Marcar reseteo diferido de los widgets de voto (para la próxima ejecución)
        st.session_state.reset_votos_pendiente = True

        # Terminar o elegir nuevo reto
        if st.session_state.ronda > st.session_state.total_rondas:
            st.session_state.juego_terminado = True
        else:
            st.session_state.reto_actual = escoger_reto()

        st.rerun()

with col_av2:
    if st.button("🎲 Cambiar reto (misma ronda)"):
        st.session_state.reto_actual = escoger_reto()
        st.rerun()

# -------------------------
# RESULTADOS FINALES
# -------------------------
st.divider()
st.write("## 📊 Resultados actuales")
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
