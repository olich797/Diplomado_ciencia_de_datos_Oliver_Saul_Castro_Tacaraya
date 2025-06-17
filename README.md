# Diplomado_ciencia_de_datos
Predicción de Cable Drop
Esta aplicación desarrollada con Streamlit permite predecir la cantidad de cable a instalar ("Cable Drop") 
en instalaciones de telecomunicaciones, utilizando un modelo de regresión lineal previamente entrenado. 
Además, detecta casos de mal uso de la aplicacion de la empresa,  en la instalación y ofrece análisis gráficos interactivos.

Funcionalidades principales
- Carga y limpieza automática de datos desde archivos Excel.
- Predicción de Cable Drop a partir del tipo de trabajo y la distancia de ubicación.
- Cálculo del error absoluto y validación de instalaciones anómalas.
- Visualización de distribución de casos con gráficos de pastel y barras.
- Interfaz para ingresar datos manualmente y validar casos específicos.
- Opción para descargar los resultados en un archivo Excel.

Requisitos
- Python 3.8 o superior

Librerías:
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- streamlit
- openpyxl
Instala todo con:
pip install -r requirements.txt

Uso
- Ejecuta la app con:
streamlit run sistema_prediccion.py
- Carga un archivo .xlsx con las columnas necesarias: TIPO_TRABAJO, DISTANCIA_UBICACION, CABLE_DROP, 
MAESTRO, ORDEN o en su defecto usar el archivo excel "datos prueba.xlsx".
- Explora los resultados, identifica instalaciones anómalas y descarga el archivo con las predicciones.

Modelo
El modelo de regresión lineal fue entrenado previamente usando datos históricos de instalaciones,
 y se carga automáticamente desde modelo_regresion_lineal.sav.
