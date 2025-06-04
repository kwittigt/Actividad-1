# home.py
import streamlit as st
from pages import contexto
from db import get_client
import pandas as pd

# Configuración inicial de la página
st.set_page_config(page_title="DataHub – Actividad 1", layout="wide")

# Menú lateral
st.sidebar.title("Menú de Navegación")
page = st.sidebar.selectbox("Secciones", ["Inicio", "Contexto Big Data", "CRUD de Ejemplo"])

if page == "Inicio":
    st.title("Sistema DataHub – INFB6052")
    st.image(
        "https://www.ctisoluciones.com/sites/default/files/2024-10/Beneficios-Big-Data.jpg",
        use_container_width=True
    )
    st.markdown("""
    **¡Bienvenido al Sistema DataHub!**

    Este prototipo demostrativo ha sido desarrollado utilizando **Streamlit** y **MongoDB** para ilustrar conceptos clave de Big Data y la gestión básica de datos.

    Utilice el menú de navegación lateral para explorar las distintas secciones:
    - **Contexto Big Data:** Descubra los fundamentos y la importancia del Big Data en la actualidad.
    - **CRUD de Ejemplo:** Interactúe con una base de datos MongoDB mediante operaciones de creación, lectura, actualización y eliminación de registros.

    ---
    **Referencias Bibliográficas:**
    - Provost, F., & Fawcett, T. (2013). *Data Science for Business*. O'Reilly Media.
    - Marr, B. (2016). *Big Data in Practice*. Wiley.
    """)

elif page == "Contexto Big Data":
    contexto.render()

else:
    st.title("CRUD de Ejemplo - Colección `registros`")
    db = get_client()["datahub"]["registros"]

    # Selección de operación CRUD
    option = st.radio("Acción", ["Crear", "Leer", "Actualizar", "Eliminar"], horizontal=True)

    if option == "Crear":
        st.subheader("Crear nuevo registro")
        nombre = st.text_input("Nombre")
        valor = st.number_input("Valor", step=1)
        if st.button("Guardar"):
            if nombre:
                db.insert_one({"nombre": nombre, "valor": valor})
                st.success(f"Registro '{nombre}' creado exitosamente.")
            else:
                st.warning("Por favor, ingrese un nombre.")

    elif option == "Leer":
        st.subheader("Registros en la Base de Datos")
        docs = list(db.find({}, {"_id": 0}))

        if docs:
            df = pd.DataFrame(docs)
            st.write("Datos en formato tabla:")
            st.dataframe(df)

            st.subheader("Visualización de Datos")
            if 'nombre' in df.columns and 'valor' in df.columns:
                st.bar_chart(df.set_index('nombre')['valor'])
                st.caption("Gráfico de barras: Valor por Nombre")
            else:
                st.warning("No se encuentran las columnas 'nombre' o 'valor' para visualizar.")
        else:
            st.info("No hay registros en la base de datos para mostrar.")

    elif option == "Actualizar":
        st.subheader("Actualizar registro existente")
        nombre = st.text_input("Nombre del registro a actualizar")
        nuevo_valor = st.number_input("Nuevo valor", step=1)
        if st.button("Actualizar"):
            result = db.update_one({"nombre": nombre}, {"$set": {"valor": nuevo_valor}})
            if result.modified_count:
                st.success(f"Registro '{nombre}' actualizado exitosamente.")
            else:
                st.warning(f"No se encontró el registro con nombre '{nombre}'.")

    else:  # Eliminar
        st.subheader("Eliminar registro")
        nombre = st.text_input("Nombre del registro a eliminar")
        if st.button("Eliminar"):
            result = db.delete_one({"nombre": nombre})
            if result.deleted_count:
                st.success(f"Registro '{nombre}' eliminado exitosamente.")
            else:
                st.warning(f"No se encontró el registro con nombre '{nombre}'.")