import streamlit as st
import pandas as pd
import re
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Predicción Cable Drop", layout="centered")

st.title("Predicción de Material")

with open('modelo_regresion_lineal.sav', 'rb') as file:
    model = pickle.load(file)

st.success("Modelo cargado correctamente.")

uploaded_file = st.file_uploader("Sube tu archivo Excel (.xlsx)", type=['xlsx'])

def limpiar_dataframe(df):

    df['COD_TIPO_TRABAJO'] = df['TIPO_TRABAJO'].apply(lambda x: int(re.findall(r'\d+', str(x))[0]))
    df['DISTANCIA_UBICACION'] = df['DISTANCIA_UBICACION'].apply(
    lambda x: int(float(str(x).replace(",", "."))) if isinstance(x, (int, float, str)) else x)
    
    df['CABLE_DROP'] = df['CABLE_DROP']
    df['MAESTRO'] = df['MAESTRO']
    df['ORDEN'] = df['ORDEN']
    
    return df[['COD_TIPO_TRABAJO', 'DISTANCIA_UBICACION', 'CABLE_DROP', 'MAESTRO', 'ORDEN']]

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df_clean = limpiar_dataframe(df)
    
    st.subheader("Datos procesados:")
    st.dataframe(df_clean)
    
    X_pred = df_clean[['COD_TIPO_TRABAJO', 'DISTANCIA_UBICACION']]
    y_pred = model.predict(X_pred)
    df_clean = df_clean.copy()

    df_clean['CABLE_DROP_PREDICT'] = y_pred

    df_clean['CABLE_DROP_PREDICT'] = df_clean['CABLE_DROP_PREDICT'].astype(int)
    df_clean['ERROR_ABSOLUTO'] = abs(df_clean['CABLE_DROP_PREDICT'] - df_clean['CABLE_DROP']).astype(int)

    df_clean['INSTALACION_ANORMAL'] = df_clean['ERROR_ABSOLUTO'].apply(lambda x: 2 if x > 70 else (1 if x > 32 else 0))

    st.subheader("Resultados con validación de anomalía:")
    st.dataframe(df_clean)
    
    labels = ["Mal Uso de la Aplicacion", "Descarga normal", "Descarga excesiva"]
    sizes = df_clean["INSTALACION_ANORMAL"].value_counts()
    colors = ["#BB1717", "#2E7D32", "#E57200"]

    labels = [f"{label} {size:.1f}%" for label, size in zip(labels, sizes / sizes.sum() * 100)]

    figura, ax = plt.subplots(figsize=(7, 7))
    ax.pie(sizes, labels=labels, autopct="", colors=colors)  # Se deja vacío el `autopct` para evitar los textos dentro del gráfico
    ax.set_title("Mal uso de la aplicación VS Descarga normal de cable VS Descarga excesiva de cable")
    st.pyplot(figura)

    categoria_seleccionada = st.selectbox(
        "Selecciona una categoría",
        options=["Mal Uso de la Aplicación", "Descarga normal de cable", "Descarga excesiva de cable"]
    )

    categoria_map = {
        "Mal Uso de la Aplicación": 2,
        "Descarga normal de cable": 0,
        "Descarga excesiva de cable": 1
    }
    valor_categoria = categoria_map[categoria_seleccionada]

    df_filtrado = df_clean[df_clean["INSTALACION_ANORMAL"] == valor_categoria]

    if not df_filtrado.empty:
        maestro_counts = df_filtrado["MAESTRO"].value_counts().reset_index()
        maestro_counts.columns = ["MAESTRO", "Total"]

        fig, ax = plt.subplots(figsize=(12, 15))
        sns.barplot(data=maestro_counts, x="Total", y="MAESTRO", ax=ax, palette="coolwarm")
        ax.set_title(f"Maestros en categoría: {categoria_seleccionada}", fontsize=20)
        ax.set_xlabel("Total de Instalaciones")
        ax.set_ylabel("Maestro")

    st.pyplot(fig)

    output_file = 'resultado_prediccion.xlsx'
    df_clean.to_excel(output_file, index=False)
    
    with open(output_file, "rb") as file:
        st.download_button("Descargar resultados en Excel", data=file, file_name=output_file)

else:
    st.info("Por favor sube un archivo .xlsx para comenzar.")
  
    
st.subheader("Ingresar datos manualmente:")
cod_trabajo_input = st.selectbox(
    "Código tipo trabajo",
    options=[10128, 10127, 10073, 10148, 10065])
distancia_input = st.number_input("Distancia de ubicación (metros)", value=200)
cable_real_input = st.number_input("CABLE_DROP real (opcional)", value=220)

if st.button("Predecir y validar instalación"):
    X_pred = pd.DataFrame([[cod_trabajo_input, distancia_input]], columns=['COD_TIPO_TRABAJO', 'DISTANCIA_UBICACION'])
    pred = model.predict(X_pred)[0]
    error_abs = abs(pred - cable_real_input)
    anomalia = 1 if error_abs > 32 else 0

    st.write(f"**Predicción de CABLE_DROP:** {int(pred)} metros")
    st.write(f"**Margen de Error :** {error_abs:.2f} metros")
    st.write(f"**¿Instalación Anormal?:** {'Sí' if anomalia == 1 else 'No'}")
