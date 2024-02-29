import streamlit as st
import geopandas as gpd
import pandas as pd
import fiona
from fiona.drvsupport import supported_drivers
import folium
from folium import Map, FeatureGroup, Marker, LayerControl, Popup
from streamlit_folium import folium_static
from folium import Choropleth, GeoJson, plugins
from folium import GeoJson
from branca.element import MacroElement
from jinja2 import Template
import branca
from shapely.ops import unary_union
import os
#import json
#from shapely.geometry import mapping
from shapely import wkt
import streamlit_authenticator as stauth


path_resultados = "BASE_DADOS/"

@st.cache_data
def load_data():
    resultados_fme = pd.read_pickle(path_resultados + '16-02-24_Trechos_alimentadores.pkl')
    return resultados_fme

@st.cache_data
def load_trafo():
    resultados_trafo = pd.read_pickle(path_resultados + 'trafo.pkl')
    return resultados_trafo

@st.cache_data
def load_SE():
    resultados_SE = pd.read_pickle(path_resultados + 'SE.pkl')
    return resultados_SE

# Leitura AR

shp_AR0 = pd.read_pickle(path_resultados + "shp_AR0.pkl")
shp_AR1 = pd.read_pickle(path_resultados + "shp_AR1.pkl")
shp_AR2 = pd.read_pickle(path_resultados + "shp_AR2.pkl")
shp_AR3 = pd.read_pickle(path_resultados + "shp_AR3.pkl")
shp_AR4 = pd.read_pickle(path_resultados + "shp_AR4.pkl")
shp_AR5 = pd.read_pickle(path_resultados + "shp_AR5.pkl")


# Mapas
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps'
    ),
    'Google Satellite': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite'
    ),
    'Google Terrain': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Terrain'
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite'
    ),
    'Esri Satellite': folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite'
    ),
    'CartoDB positron': folium.TileLayer(
        tiles='CartoDB positron',
        attr='CartoDB',
        name='Light Map'
    )
}

# Setando pagina do stream lit

st.set_page_config(layout="wide")#, page_icon = "D:/2023_Light_Dash/logo.png")

# Carrega os dados
resultados_fme = load_data()
resultados_trafo = load_trafo()
resultados_SE = load_SE()



alimentadores = st.multiselect(
    'Linha',
    resultados_fme['ALIMENTADOR'].unique(),
    default=None,
    help="Selecione a(s) linha(s) ..."
)

if alimentadores:  # Verifica se a lista não está vazia antes de aplicar o filtro
    regiao_df = resultados_fme[resultados_fme['ALIMENTADOR'].isin(alimentadores)]

trafo = st.multiselect(
    'TRANSFORMADORES',
    resultados_trafo['LINHA'].unique(),
    default=None,
    help="Selecione a(s) linha(s) ..."
)

if alimentadores:  # Verifica se a lista não está vazia antes de aplicar o filtro
    regiao_TRAFO = resultados_trafo[resultados_trafo['LINHA'].isin(trafo)]

    
SE = st.multiselect(
    'SUBESTAÇÃO',
    resultados_SE['NOME'].unique(),
    default=None,
    help="Selecione a(s) linha(s) ..."
)

if alimentadores:  # Verifica se a lista não está vazia antes de aplicar o filtro
    regiao_SE = resultados_SE[resultados_SE['NOME'].isin(SE)]

# Centroides Localidades
centroide = regiao_df.to_crs(22182).centroid.to_crs(4326).iloc[[0]]

# Criar o mapa folium
mapa = folium.Map(location=[centroide.y, centroide.x], zoom_start=13)

# Adicionar basemaps ao mapa usando um loop
for name, tile_layer in basemaps.items():
    tile_layer.add_to(mapa)

# Adição de Choropleths
colors = ['orange', 'beige', 'pink', 'yellow', 'salmon']

for name, shp_data, color in zip(['ASRO', 'COMUNIDADES_DOMINADAS_PELA_MILICIA', 'COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS', 'COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO', 'COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO'], [shp_AR1, shp_AR2, shp_AR3, shp_AR4, shp_AR5], colors):
    folium.Choropleth(geo_data=shp_data, fill_color='pink', name=name).add_to(mapa)

GeoJson(regiao_df, name=f'{alimentadores}').add_to(mapa)



GeoJson(regiao_TRAFO, name=f'{trafo}').add_to(mapa)

# Adicionar popups aos marcadores
for idx, row in regiao_TRAFO.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],  # Substitua pelas suas coordenadas
        popup=row['MATRICULA']  # Adicione o número da matrícula como popup
    ).add_to(mapa)

GeoJson(regiao_SE, name=f'{SE}', style_function=lambda x: {'fillColor': 'red', 'fillOpacity': 0.6}, tooltip=SE).add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# Adicionar controle de tela cheia
plugins.Fullscreen().add_to(mapa)

if st.button("Baixar Mapa como HTML"):
            # Caixa de texto para inserir o caminho
            caminho_salvar = st.text_input("Arquivo:", value= SE[0] + ".html")

            if caminho_salvar:
                # Adicionar o arquivo temporário para download
                st.download_button(
                    label="Clique para baixar",
                    data=mapa.get_root().render(),
                    file_name=os.path.join(caminho_salvar),
                    key="download_mapa_html"
                )

# Exibir mapa 
folium_static(mapa, width=1300, height=600)
