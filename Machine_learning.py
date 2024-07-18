import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn import preprocessing

# Title of the Streamlit app
st.title("Análisis de la Euro 2020")
st.subheader('Estadísticas y comparador de jugadores durante la competición')
st.markdown("---")
st.write('Gracias a Statsbomb, hemos podido analizar todos los eventos y datos de la Euro 2020, con el fin de poder obtener la estadísticas de cada jugador, poder visualizarlas sobre un campo de fútbol virtual y finalmente, encontrar jugadores con características similares dentro del entorno de la propia competición')
st.markdown("***") 
st.subheader(':soccer: Estudio y representación de las estadísticas de los jugadores')
st.write('Mapa virtual interactivo con el que podemos analizar todas las acciones de cualquier jugador en la Euro 2020')
# Embed URL of the Power BI report
# Replace this with your actual Power BI report embed URL
embed_url = "https://app.powerbi.com/view?r=eyJrIjoiZjg0OWNjNDEtNjhjYy00YmQ0LWE5N2QtNWJlOTc3MDM2ZDc4IiwidCI6ImJiYjEzOGJhLWZjMDYtNDM2ZS04ODhlLTAyYmVjMzFlYTIzYSIsImMiOjl9"


# HTML code to embed Power BI report
html_code = f"""
<div style="border: 2px solid black;">
    <iframe 
        width="100%" 
        height="600px" 
        src="{embed_url}" 
        frameborder="0" 
        allowFullScreen="true">
    </iframe>
</div>
"""

# Display the embedded Power BI report in Streamlit
st.markdown(html_code, unsafe_allow_html=True)






st.markdown("---")
st.subheader('🔎 Buscador de jugadores Euro 2020')
st.write('Dado un jugador y su posición, se implementa un modelo de Machine Learning que nos permite conocer a 10 futbolistas con características similares durante la Euro 2020')

df_datos_Euro2020=pd.read_csv('datos_Euro2020.csv')
df_imagenes_Euro2020=pd.read_excel('fotografias.csv')

def path_to_image_html(path):
    return f'<img src="{path}" width="60" >'

df_imagenes_Euro2020['imagen'] = df_imagenes_Euro2020['imagen'].apply(path_to_image_html)

def busqueda_jugadores(jugador,posicion):
    X=df_datos_Euro2020[df_datos_Euro2020['position']==posicion].drop(['player','position','team'],axis=1)
    jugadores=df_datos_Euro2020[(df_datos_Euro2020['position']==posicion)&(df_datos_Euro2020['player'])].drop(['position'],axis=1)
    jugadores=jugadores.set_index('player')
    scaler = preprocessing.StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    indice=jugadores.index.get_loc(jugador)
    jugador_a_comparar=X_scaled[indice]
    neigh= NearestNeighbors(n_neighbors=11, radius=0.4)
    neigh.fit(X_scaled)
    jugadores_similares=neigh.kneighbors([jugador_a_comparar], 12, return_distance=True)
    for i in jugadores_similares[1]:
        nombre_jugadores_similares=jugadores.iloc[i]
        nombre_jugadores_similares=nombre_jugadores_similares.reset_index()
        nombre_jugadores_similares=nombre_jugadores_similares[['player']]
    for i in jugadores_similares[0]:
        Coeficiente_similitud=pd.DataFrame(100-i)

    buscador_jugadores=pd.concat([nombre_jugadores_similares, Coeficiente_similitud], axis=1)
    buscador_jugadores=buscador_jugadores.drop(0,axis=0)
    buscador_jugadores=df_imagenes_Euro2020.merge(buscador_jugadores,how="inner")
    buscador_jugadores=buscador_jugadores.rename(columns={0 :'%Coeficiente_similitud','player':'Jugadores','imagen':'Imagen'}).sort_values('%Coeficiente_similitud', ascending=False).reset_index(drop=True)
    
    
    return buscador_jugadores

position = st.radio(
    "Selecciona la posición",
    df_datos_Euro2020.position.unique(),
    captions = df_datos_Euro2020.position.unique())

jugador = st.selectbox(
    "Selecciona el jugador",
    df_datos_Euro2020[df_datos_Euro2020.position == position].player.unique())



input_df = busqueda_jugadores(jugador,position)

st.subheader(f'Jugadores similares a {jugador} y su coeficiente de similitud')
st.write(input_df.to_html(escape=False), unsafe_allow_html=True)

