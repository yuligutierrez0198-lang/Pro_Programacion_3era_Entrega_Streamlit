""" 
Nombre: Yuli del Carmen Gutiérrez Rodríguez
 Clase: Programación III
 Profesor: Diego Ayala
 Este programa hace uso de streamlit para crear una pagina
 que use el algoritmo de Dijkstras para mostrar la ruta más corta
"""

# ------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
from pathlib import Path

# Importamos las funciones para leer y guardar conexiones.
from io_handler import cargar_grafo, guardar_conexion


# ------------------------------------------------------------
# 2. CONFIGURACIÓN DE LA APLICACIÓN
# ------------------------------------------------------------

st.set_page_config(
    page_title="Dijkstra | Ballet Edition",
    page_icon="🩰",
    layout="wide"
)

# Definimos la ubicación del archivo CSV.
RUTA_CSV = Path(__file__).resolve().parent / "nodos.csv"


# ------------------------------------------------------------
# 3. INICIALIZACIÓN DEL GRAFO EN SESSION_STATE
# ------------------------------------------------------------

# Comprobamos si el grafo ya existe en la sesión.
# Así evitamos cargar el CSV cada vez que Streamlit actualiza
# la interfaz.

if "grafo" not in st.session_state:

    try:

        # Si el archivo no existe, lo creamos.
        if not RUTA_CSV.exists():

            with open(
                RUTA_CSV,
                "w",
                newline="",
                encoding="utf-8"
            ) as archivo:

                archivo.write("origen,destino,peso\n")

        # Cargamos el grafo desde el archivo CSV.
        st.session_state.grafo = cargar_grafo(str(RUTA_CSV))

        st.session_state.csv_cargado = True

    except FileNotFoundError:

        st.error(
            "No se encontró el archivo nodos.csv. "
            "Verifica su ubicación."
        )

        st.stop()

    except PermissionError:

        st.error(
            "No tienes permisos para acceder al archivo nodos.csv."
        )

        st.stop()

    except ValueError:

        st.error(
            "El archivo CSV contiene un peso inválido. "
            "Verifica que los pesos sean números válidos."
        )

        st.stop()

    except KeyError:

        st.error(
            "El archivo CSV tiene columnas incorrectas. "
            "Se requieren: origen, destino y peso."
        )

        st.stop()


# Inicializamos el resultado de Dijkstra.
if "resultado" not in st.session_state:

    st.session_state.resultado = None


# ------------------------------------------------------------
# 4. DISEÑO VISUAL: TEMA BALLET
# ------------------------------------------------------------

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background-color: #FFF7FA;
}

/* Título principal */
.titulo-principal {
    color: #A65D83;
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 5px;
}

/* Subtítulo */
.subtitulo {
    color: #987A9D;
    text-align: center;
    font-size: 17px;
    margin-bottom: 25px;
}

/* Encabezados */
h1, h2, h3 {
    color: #A65D83 !important;
}

/* Botones */
.stButton > button {
    background-color: #E8BBD0;
    color: #663B58;
    border-radius: 12px;
    border: 1px solid #D99BB9;
    font-weight: bold;
    padding: 8px 20px;
}

/* Efecto al pasar el cursor */
.stButton > button:hover {
    background-color: #D99BB9;
    color: white;
    border-color: #C77FA3;
}

/* Pestañas */
.stTabs [data-baseweb="tab"] {
    color: #A65D83;
    font-weight: bold;
}

/* Formularios */
div[data-testid="stForm"] {
    background-color: #FFF0F5;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #F0CADB;
}

/* Separadores */
hr {
    border-color: #E8BBD0;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# 5. ENCABEZADO DE LA APLICACIÓN
# ------------------------------------------------------------

st.markdown(
    '<div class="titulo-principal">🩰 DIJKSTRA 🩰</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Sistema de rutas y caminos mínimos | Ballet Edition'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ------------------------------------------------------------
# 6. CREACIÓN DE PESTAÑAS
# ------------------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "🌸 Calcular ruta",
    "🎀 Registrar conexiones",
    "🩰 Red de nodos"
])


# ============================================================
# PESTAÑA 1: CALCULAR LA RUTA MÁS CORTA
# ============================================================

with tab1:

    st.header("🌸 Calculadora de rutas")

    st.write(
        "Selecciona el nodo de origen y el nodo de destino "
        "para encontrar el camino más corto utilizando "
        "el algoritmo de Dijkstra."
    )

    # Obtenemos los nodos disponibles.
    nodos_disponibles = list(
        st.session_state.grafo.nodos.keys()
    )

    # Campos para capturar origen y destino.
    col1, col2 = st.columns(2)

    with col1:

        inicio = st.text_input(
            "Nodo de origen",
            placeholder="Ejemplo: A",
            key="origen_ruta"
        )

    with col2:

        destino = st.text_input(
            "Nodo de destino",
            placeholder="Ejemplo: E",
            key="destino_ruta"
        )

    # Botón para calcular la ruta.
    if st.button(
        "✨ Calcular camino más corto",
        key="calcular"
    ):

        # Limpiamos los espacios de los datos.
        inicio = inicio.strip()
        destino = destino.strip()

        # Validamos que los campos no estén vacíos.
        if not inicio or not destino:

            st.warning(
                "Debes ingresar el nodo de origen y el destino."
            )

            st.session_state.resultado = None

        # Validamos que el nodo de origen exista.
        elif inicio not in st.session_state.grafo.nodos:

            st.error(
                f"El nodo de origen '{inicio}' no existe."
            )

            st.session_state.resultado = None

        # Validamos que el nodo de destino exista.
        elif destino not in st.session_state.grafo.nodos:

            st.error(
                f"El nodo de destino '{destino}' no existe."
            )

            st.session_state.resultado = None

        else:

            try:

                # Ejecutamos el algoritmo de Dijkstra.
                costo, camino = st.session_state.grafo.dijkstra(
                    inicio,
                    destino
                )

                # Guardamos el resultado en la sesión.
                st.session_state.resultado = {
                    "inicio": inicio,
                    "destino": destino,
                    "costo": costo,
                    "camino": camino
                }

            except KeyError:

                st.error(
                    "Uno de los nodos no existe en el grafo."
                )

                st.session_state.resultado = None

            except ValueError:

                st.error(
                    "No fue posible calcular la ruta. "
                    "Verifica los datos de entrada."
                )

                st.session_state.resultado = None

    # Recuperamos el resultado guardado.
    resultado = st.session_state.resultado

    # Mostramos el resultado si existe.
    if resultado is not None:

        st.markdown("---")

        st.subheader("💗 Resultado del recorrido")

        if resultado["camino"]:

            # Mensaje de éxito.
            st.success("¡Se encontró una ruta!")

            # Mostramos el recorrido.
            st.markdown("**Camino más corto:**")

            st.markdown(
                " ➜ ".join(resultado["camino"])
            )

            # Mostramos el costo total.
            st.metric(
                label="Costo total de la ruta",
                value=f'{resultado["costo"]:g}'
            )

            # Información de los nodos.
            st.info(
                f'Ruta calculada desde '
                f'{resultado["inicio"]} hasta '
                f'{resultado["destino"]}.'
            )

        else:

            # Mensaje cuando no existe una ruta.
            st.error(
                f'No existe una ruta entre '
                f'{resultado["inicio"]} y '
                f'{resultado["destino"]}.'
            )


# ============================================================
# PESTAÑA 2: REGISTRAR NUEVAS CONEXIONES
# ============================================================

with tab2:

    st.header("🎀 Registrar una nueva conexión")

    st.write(
        "Agrega dos nodos y el peso de su conexión. "
        "Los datos se guardarán en nodos.csv y se actualizará "
        "el grafo que permanece en memoria."
    )

    # Creamos el formulario.
    with st.form("formulario_conexion"):

        col1, col2, col3 = st.columns(3)

        with col1:

            origen_nuevo = st.text_input(
                "Nodo de origen",
                placeholder="Ejemplo: A"
            )

        with col2:

            destino_nuevo = st.text_input(
                "Nodo de destino",
                placeholder="Ejemplo: B"
            )

        with col3:

            peso_nuevo = st.number_input(
                "Peso de la conexión",
                min_value=0.0,
                value=1.0,
                step=1.0
            )

        # Botón para guardar la conexión.
        guardar = st.form_submit_button(
            "💗 Guardar conexión"
        )

    # Procesamos los datos cuando se envía el formulario.
    if guardar:

        # Eliminamos espacios innecesarios.
        origen_nuevo = origen_nuevo.strip()
        destino_nuevo = destino_nuevo.strip()

        # Validamos que los nodos no estén vacíos.
        if not origen_nuevo or not destino_nuevo:

            st.warning(
                "Debes ingresar ambos nodos."
            )

        # Evitamos conexiones del mismo nodo consigo mismo.
        elif origen_nuevo == destino_nuevo:

            st.warning(
                "El origen y el destino deben ser diferentes."
            )

        else:

            grafo = st.session_state.grafo

            # Comprobamos si la conexión ya existe.
            # El grafo es no dirigido, por lo que A-B y B-A
            # representan la misma conexión.

            conexion_existente = (
                origen_nuevo in grafo.nodos
                and destino_nuevo in
                grafo.nodos[origen_nuevo].vecinos
            )

            if conexion_existente:

                st.warning(
                    "Esta conexión ya existe. "
                    "No se registró nuevamente."
                )

            else:

                try:

                    # Guardamos la conexión en el CSV.
                    guardar_conexion(
                        str(RUTA_CSV),
                        origen_nuevo,
                        destino_nuevo,
                        peso_nuevo
                    )

                    # Actualizamos el grafo en memoria.
                    grafo.agregar_conexion(
                        origen_nuevo,
                        destino_nuevo,
                        peso_nuevo
                    )

                    # Eliminamos el resultado anterior.
                    st.session_state.resultado = None

                    # Confirmamos el registro.
                    st.success(
                        "¡Conexión registrada correctamente!"
                    )

                    st.write(
                        f"**Origen:** {origen_nuevo}"
                    )

                    st.write(
                        f"**Destino:** {destino_nuevo}"
                    )

                    st.write(
                        f"**Peso:** {peso_nuevo:g}"
                    )

                    # Actualizamos la interfaz.
                    st.rerun()

                except PermissionError:

                    st.error(
                        "No tienes permisos para modificar nodos.csv."
                    )

                except FileNotFoundError:

                    st.error(
                        "No se encontró el archivo donde "
                        "se debe guardar la conexión."
                    )

                except ValueError as error:

                    st.warning(
                        f"No se pudo registrar la conexión: {error}"
                    )


# ============================================================
# PESTAÑA 3: VISUALIZAR LA RED DE NODOS
# ============================================================

with tab3:

    st.header("🩰 Visualización de la red")

    st.write(
        "Consulta los nodos y las conexiones que actualmente "
        "forman parte del grafo."
    )

    grafo = st.session_state.grafo

    # --------------------------------------------------------
    # TABLA DE NODOS
    # --------------------------------------------------------

    st.subheader("🌸 Nodos registrados")

    # Obtenemos los nombres de los nodos.
    lista_nodos = list(grafo.nodos.keys())

    # Creamos un DataFrame con Pandas.
    df_nodos = pd.DataFrame(
        lista_nodos,
        columns=["Nombre del nodo"]
    )

    # Mostramos la tabla.
    st.dataframe(
        df_nodos,
        use_container_width=True,
        hide_index=True
    )

    # Mostramos el total de nodos.
    st.metric(
        "Total de nodos",
        len(lista_nodos)
    )

    st.markdown("---")

    # --------------------------------------------------------
    # TABLA DE CONEXIONES
    # --------------------------------------------------------

    st.subheader("🎀 Conexiones registradas")

    lista_conexiones = []

    # Recorremos los nodos y sus vecinos.
    for origen, nodo in grafo.nodos.items():

        for destino, peso in nodo.vecinos.items():

            # Evitamos mostrar conexiones duplicadas.
            if origen < destino:

                lista_conexiones.append({
                    "Origen": origen,
                    "Destino": destino,
                    "Peso": peso
                })

    # Creamos el DataFrame.
    df_conexiones = pd.DataFrame(
        lista_conexiones,
        columns=["Origen", "Destino", "Peso"]
    )

    # Mostramos las conexiones.
    st.dataframe(
        df_conexiones,
        use_container_width=True,
        hide_index=True
    )

    # Mostramos el total de conexiones.
    st.metric(
        "Total de conexiones",
        len(lista_conexiones)
    )

    # --------------------------------------------------------
    # INFORMACIÓN DEL PROYECTO
    # --------------------------------------------------------

    with st.expander("💗 Información del proyecto"):

        st.write(
            "Este sistema utiliza el algoritmo de Dijkstra "
            "para encontrar el camino de menor costo entre "
            "dos nodos de una red."
        )

        st.write(
            "Los nodos representan puntos de conexión y "
            "los pesos representan el costo de desplazamiento "
            "entre ellos."
        )

        st.write(
            "La información se almacena en nodos.csv y el "
            "grafo permanece en memoria mediante "
            "st.session_state durante la sesión."
        )


# ------------------------------------------------------------
# 7. PIE DE PÁGINA
# ------------------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        color: #A65D83;
        padding: 15px;
        font-size: 14px;
    ">
        🩰 Proyecto de Programación III 🩰<br>
        Algoritmo de Dijkstra | Ballet Edition<br>
        Yuli del Carmen Gutiérrez Rodríguez
    </div>
    """,
    unsafe_allow_html=True
)
