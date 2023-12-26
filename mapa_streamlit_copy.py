## CARREGAR BIBLIOTECAS

import streamlit as st
import pandas as pd
import geopandas as gpd
from fiona.drvsupport import supported_drivers
# from fiona.drvsupport import supported_drivers  # Esta linha não parece ser usada
# import pandas as pd  # Já importado anteriormente
# import numpy as np  # Não parece ser usado
import fiona  # Já importado anteriormente
# from os import listdir  # Não parece ser usado
# import zipfile  # Não parece ser usado
# import time  # Não parece ser usado
# from datetime import datetime  # Não parece ser usado
# from shapely.ops import unary_union  # Não parece ser usado
# import openpyxl  # Não parece ser usado
# import glob  # Não parece ser usado
# import pickle  # Não parece ser usado
# from geopandas.tools import overlay  # Não parece ser usado
# import folium  # Já importado anteriormente
# from folium import plugins  # Já importado anteriormente
# from branca.element import MacroElement  # Não parece ser usado
# from jinja2 import Template  # Não parece ser usado
# from folium.plugins import MiniMap  # Já importado anteriormente
# from folium import Map  # Já importado anteriormente
# from folium.plugins import MarkerCluster  # Já importado anteriormente
# from folium import FeatureGroup, Marker, LayerControl, Popup  # Já importado anteriormente
# from streamlit_folium import folium_static  # Já importado anteriormente
# from folium.features import DivIcon  # Não parece ser usado
# import branca.colormap as cm  # Já importado anteriormente
# import matplotlib.pyplot as plt  # Já importado anteriormente
# from folium.plugins import MiniMap  # Já importado anteriormente
# import ipywidgets as widgets  # Não parece ser usado
# from ipywidgets import Layout  # Não parece ser usado
# from ipywidgets import fixed  # Não parece ser usado
# import atrb_mcpse  # Não parece ser usado

### Funções

def alim_validados (path):
    # Ler os arquivos Excel
    alimentadores_validados = pd.read_excel(path)
    return alimentadores_validados


path = 'ALIM VALIDADOS - 24.11.2023.xlsx'

alimentadores_validados = alim_validados(path)

### Interface STREAMLIT

st.title('Acompanhamento Inventário LIGHT')
st.subheader('''
             Esta página é dividida em duas categorias:
                1. Power BI Dash Board
                2. Visuzaliação Geográfica
             ''')
options = st.selectbox('Por favor selecione', ['Power BI Dashboard', 'Mapas Alimentadores'] )

if options == 'Power BI Dashboard':

    st.markdown('<iframe title="Status_Inventário_v2_bru" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=8aebaa75-c550-486f-ae18-1839a03375f1&autoAuth=true&ctid=5d29356d-609d-444f-a22f-9d38022b00ef" frameborder="0" allowFullScreen="true"></iframe>',unsafe_allow_html=True)

    


#### Importando dados




def read_kml_and_extract_tables(file_path):
    dic_df = {}

    for lay in fiona.listlayers(file_path):
        tbl_dict = {}
        i = 0
        gdf = gpd.read_file(file_path, driver='KML', layer=lay)

        for tbl in gdf.Description:
            tbl_dict[i] = pd.read_html(tbl)[0].set_index(0).to_dict()[1]
            i += 1

        dic_df[lay[5:]] = pd.concat([gdf, pd.DataFrame(tbl_dict).T], axis=1)

    return dic_df


pasta_Reg = 'D:/GIT/2022_23_LIGHT_Sust_Concessao/4. Execução/8. Área de risco/0.6 - Poligonais das regionais/'

supported_drivers['KML'] = 'rw'

file = 'STP_LDA_ALZIRA.kml'

result_dict = read_kml_and_extract_tables(file)

# Acesse os DataFrames por chave
gdf_trecho_mt = result_dict.get('Trecho MT', pd.DataFrame())

# Convertendo a Series 'geometry_x' para um GeoDataFrame
gdf_trecho_mt = gpd.GeoDataFrame(gdf_trecho_mt, geometry='geometry')

# Aplicando a transformação de CRS somente na coluna de geometria
gdf_trecho_mt['geometry'] = gdf_trecho_mt['geometry'].to_crs(4326)
gdf_trecho_mt = gdf_trecho_mt.set_geometry('geometry') # Define que a coluna 'geometry' é a geometria ativa

# ### AREAS DE RISCO



pasta_AR='D:/GIT/2022_23_LIGHT_Sust_Concessao/4. Execução/8. Área de risco/0.4 - Poligonais áreas de risco/'
file_suffixes = ['ACAC.json', 'ASRO.geojson', 'COMUNIDADES_DOMINADAS_PELA_MILICIA.geojson', 'COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS.geojson', 'COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO.geojson', 'COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO.geojson']

shp_AR0 =gpd.read_file(pasta_AR +'ACAC.json')
shp_AR1 =gpd.read_file(pasta_AR +'ASRO.geojson')
shp_AR2 =gpd.read_file(pasta_AR +'COMUNIDADES_DOMINADAS_PELA_MILICIA.geojson')
shp_AR3 =gpd.read_file(pasta_AR +'COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS.geojson')
shp_AR4 =gpd.read_file(pasta_AR +'COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO.geojson')
shp_AR5 =gpd.read_file(pasta_AR +'COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO.geojson')

shp_AR6 = pd.concat([shp_AR0, shp_AR1, shp_AR2, shp_AR3, shp_AR4, shp_AR5]) # cria um novo DataFrame chamado shp_AR por meio da concatenação dos DataFrames shp_AR0, shp_AR1, shp_AR2, shp_AR3, shp_AR4, e shp_AR5. Todos eles contêm informações sobre as áreas relacionadas aos grupos mencionados.
shp_AR6= shp_AR6[shp_AR6['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 

shp_AR0= shp_AR0[shp_AR0['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 
shp_AR1= shp_AR1[shp_AR1['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'.
shp_AR2= shp_AR2[shp_AR2['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'.
shp_AR3= shp_AR3[shp_AR3['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'.
shp_AR4= shp_AR4[shp_AR4['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'.
shp_AR5= shp_AR5[shp_AR5['geometry'].geom_type == 'Polygon'] #filtra o DataFrame shp_AR para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'.

#Renomeando o geo_shape para geometry

shp_AR6=shp_AR6.to_crs('EPSG:4674') # o GeoDataFrame shp_AR é modificado para utilizar o sistema de coordenadas EPSG 4674
shp_AR0=shp_AR0.to_crs('EPSG:4674') # o GeoDataFrame shp_AR0 é modificado para utilizar o sistema de coordenadas EPSG 4674
shp_AR1=shp_AR1.to_crs('EPSG:4674') # o GeoDataFrame shp_AR1 é modificado para utilizar o sistema de coordenadas EPSG 4674
shp_AR2=shp_AR2.to_crs('EPSG:4674') # o GeoDataFrame shp_AR2 é modificado para utilizar o sistema de coordenadas EPSG 4674
shp_AR3=shp_AR3.to_crs('EPSG:4674') # o GeoDataFrame shp_AR3 é modificado para utilizar o sistema de coordenadas EPSG 4674
shp_AR4=shp_AR4.to_crs('EPSG:4674') # o GeoDataFrame shp_AR4 é modificado para utilizar o sistema de coordenadas EPSG 4674
shp_AR5=shp_AR5.to_crs('EPSG:4674') # o GeoDataFrame shp_AR5 é modificado para utilizar o sistema de coordenadas EPSG 4674

#Validando as geometrias das áreas de risco
dataframes = [shp_AR0, shp_AR1, shp_AR2, shp_AR3, shp_AR4, shp_AR5, shp_AR6]

results = []  # Lista para armazenar os resultados de cada shp_AR


for i, df in enumerate(dataframes):
    valid_geometries = []  # Lista para armazenar as geometrias válidas

    for index, row in df.iterrows():
        if row['geometry'].is_valid:
            valid_geometries.append(row['geometry'])
        else:
            print(f"Geometria na linha {index} não é válida. Corrija antes de prosseguir.")

    if valid_geometries:
        unified_geometry = gpd.GeoSeries(unary_union(valid_geometries))
        temp_df = pd.DataFrame({'AR': 1, 'geo_shape': unified_geometry})
        temp_df['source'] = f'shp_AR{i}'
        results.append(temp_df)
    else:
        print(f"Nenhuma geometria válida encontrada no shp_AR{i}.")

# Cria um novo DataFrame unindo os resultados em linhas
result_df = pd.concat(results, ignore_index=True)

# # Adição do atributo Area de risco ACAC

AR0 =result_df.loc[result_df['source'] == 'shp_AR0']
AR0_geo = gpd.GeoDataFrame(AR0, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR0 = gpd.sjoin(gdf_trecho_mt, AR0_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR0['AR']=SSDMT_AR0['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR0['AR'].value_counts()

# # Adição do atributo Area de risco ASRO

AR1 =result_df.loc[result_df['source'] == 'shp_AR1']
AR1_geo = gpd.GeoDataFrame(AR0, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR1 = gpd.sjoin(gdf_trecho_mt, AR1_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR1['AR']=SSDMT_AR1['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR1['AR'].value_counts()

# # Adição do atributo Area de risco COMUNIDADES_DOMINADAS_PELA_MILICIA

AR2 =result_df.loc[result_df['source'] == 'shp_AR2']
AR2_geo = gpd.GeoDataFrame(AR2, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR2 = gpd.sjoin(gdf_trecho_mt, AR2_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR2['AR']=SSDMT_AR2['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR2['AR'].value_counts()

# # Adição do atributo Area de risco COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS

AR3 =result_df.loc[result_df['source'] == 'shp_AR3']
AR3_geo = gpd.GeoDataFrame(AR3, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR3 = gpd.sjoin(gdf_trecho_mt, AR3_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR3['AR']=SSDMT_AR3['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR3['AR'].value_counts()

# # Adição do atributo Area de risco COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO

AR4 =result_df.loc[result_df['source'] == 'shp_AR4']
AR4_geo = gpd.GeoDataFrame(AR4, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR4 = gpd.sjoin(gdf_trecho_mt, AR4_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR4['AR']=SSDMT_AR4['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR4['AR'].value_counts()

# # Adição do atributo Area de risco COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO

AR5 =result_df.loc[result_df['source'] == 'shp_AR5']
AR5_geo = gpd.GeoDataFrame(AR5, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR5 = gpd.sjoin(gdf_trecho_mt, AR5_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR5['AR']=SSDMT_AR5['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR5['AR'].value_counts()

# # Adição do atributo Area de risco TOTAL

AR6 =result_df.loc[result_df['source'] == 'shp_AR6']
AR6_geo = gpd.GeoDataFrame(AR6, geometry='geo_shape')  # Convertendo AR0 em um GeoDataFrame

SSDMT_AR6 = gpd.sjoin(gdf_trecho_mt, AR6_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

SSDMT_AR6['AR']=SSDMT_AR6['AR'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
SSDMT_AR6['AR'].value_counts()

base_completa=pd.merge(SSDMT_AR0, SSDMT_AR1, on=['Linha', 'geometry', 'Comprimento real (m)', 'Código'], suffixes=('_ACAC', '_ASRO'), how='left')
base_completa=pd.merge(base_completa, SSDMT_AR2, on=['Linha', 'geometry', 'Comprimento real (m)', 'Código'], how='left')
base_completa=pd.merge(base_completa, SSDMT_AR3, on=['Linha', 'geometry', 'Comprimento real (m)', 'Código'], suffixes=('_MI', '_ADA'), how='left')
base_completa=pd.merge(base_completa, SSDMT_AR4, on=['Linha', 'geometry', 'Comprimento real (m)', 'Código'], how='left')
base_completa=pd.merge(base_completa, SSDMT_AR5, on=['Linha', 'geometry', 'Comprimento real (m)', 'Código'], suffixes=('_CV', '_TCP'), how='left')
base_completa=pd.merge(base_completa, SSDMT_AR6, on=['Linha', 'geometry', 'Comprimento real (m)', 'Código'], how='left')

alimentadores_base_completa = pd.DataFrame
alimentadores_base_completa = base_completa[['Linha']].drop_duplicates()
alimentadores_base_completa


# ### REGIONAIS






# regionais =gpd.read_file(pasta_Reg +'Localidades Light 1.json')

# regionais= regionais[regionais['geometry'].geom_type == 'Polygon'] #filtra o DataFrame regionais para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 

# regionais['malha'].value_counts()

# regionais1= regionais[regionais['malha'] == 'VP'] #filtra o DataFrame regionais para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 
# regionais2= regionais[regionais['malha'] == 'BX'] #filtra o DataFrame regionais para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 
# regionais3= regionais[regionais['malha'] == 'LE'] #filtra o DataFrame regionais para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 
# regionais4= regionais[regionais['malha'] == 'OE'] #filtra o DataFrame regionais para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 
# regionais5= regionais[regionais['malha'] == 'CS'] #filtra o DataFrame regionais para conter apenas as linhas onde o tipo de geometria na coluna 'geometry' é igual a 'Polygon'. 

# regionais1=regionais1.to_crs('EPSG:4674') # o GeoDataFrame é modificado para utilizar o sistema de coordenadas EPSG 4674
# regionais2=regionais2.to_crs('EPSG:4674') # o GeoDataFrame é modificado para utilizar o sistema de coordenadas EPSG 4674
# regionais3=regionais3.to_crs('EPSG:4674') # o GeoDataFrame é modificado para utilizar o sistema de coordenadas EPSG 4674
# regionais4=regionais4.to_crs('EPSG:4674') # o GeoDataFrame é modificado para utilizar o sistema de coordenadas EPSG 4674
# regionais5=regionais5.to_crs('EPSG:4674') # o GeoDataFrame é modificado para utilizar o sistema de coordenadas EPSG 4674

# #Validando as geometrias das REGIONAIS
# dataframes_rg = [regionais1, regionais2, regionais3, regionais4, regionais5]

# results_rg = []  # Lista para armazenar os resultados de cada REGIONAL


# for i, df in enumerate(dataframes_rg):
#     valid_geometries_rg = []  # Lista para armazenar as geometrias válidas

#     for index, row in df.iterrows():
#         if row['geometry'].is_valid:
#             valid_geometries_rg.append(row['geometry'])
#         else:
#             print(f"Geometria na linha {index} não é válida. Corrija antes de prosseguir.")

#     if valid_geometries_rg:
#         unified_geometry = gpd.GeoSeries(unary_union(valid_geometries_rg))
#         temp_df_rg = pd.DataFrame({'malha': 1, 'geometry': unified_geometry})
#         temp_df_rg['source'] = f'regionais{i}'
#         results_rg.append(temp_df_rg)
#     else:
#         print(f"Nenhuma geometria válida encontrada no regionais{i}.")

# # Cria um novo DataFrame unindo os resultados em linhas
# results_reg = pd.concat(results_rg, ignore_index=True)

#  # Adição do atributo Regionais - vale do paraíba

# REG1 =regionais.loc[regionais['malha'] == 'VP']
# REG_geo = gpd.GeoDataFrame(REG1, geometry='geometry')  # Convertendo AR0 em um GeoDataFrame

# REG_VP = gpd.sjoin(gdf, REG_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

# REG_VP['malha']=REG_VP['malha'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
# REG_VP['malha'].value_counts()

# # Adição do atributo Regionais - baixada

# REG2 =regionais.loc[regionais['malha'] == 'BX']
# REG2_geo = gpd.GeoDataFrame(REG2, geometry='geometry')  # Convertendo AR0 em um GeoDataFrame

# REG_BX = gpd.sjoin(gdf, REG2_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

# REG_BX['malha']=REG_BX['malha'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
# REG_BX['malha'].value_counts()

# # Adição do atributo Regionais - leste

# REG3 =regionais.loc[regionais['malha'] == 'LE']
# REG3_geo = gpd.GeoDataFrame(REG3, geometry='geometry')  # Convertendo AR0 em um GeoDataFrame

# REG_LE = gpd.sjoin(gdf, REG3_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

# REG_LE['malha']=REG_LE['malha'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
# REG_LE['malha'].value_counts()

# # Adição do atributo Regionais - CENTRO SUL

# REG5 =regionais.loc[regionais['malha'] == 'CS']
# REG5_geo = gpd.GeoDataFrame(REG5, geometry='geometry')  # Convertendo AR0 em um GeoDataFrame

# REG_CS = gpd.sjoin(gdf, REG5_geo, how='left', op='intersects') #Realiza uma junção espacial entre dois GeoDataFrames (df_SSDMT_centroids e shp_AR_un), mantendo todas as linhas do GeoDataFrame df_SSDMT_centroids e adicionando informações do GeoDataFrame shp_AR_un se houver interseção espacial.

# REG_CS['malha']=REG_CS['malha'].fillna(0) #preenche os valores ausentes na coluna 'AR' com 0
# REG_CS['malha'].value_counts()


### MAPAS

basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps'#,
        #overlay = True,
        #control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite'#,
        #overlay = True,
        #control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain'#,
        #overlay = True,
        #control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite'#,
        #overlay = True,
        #control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite'#,
        #overlay = True,
        #control = True
    ),
    'CartoDB positron': folium.TileLayer(
        tiles = 'CartoDB positron',
        attr = 'CartoDB',
        name = 'Light Map'#,
        #overlay = True,
        #control = True
    )  
}

#===============================================================================
# FILTROS MAPA
#===============================================================================
## FILTRO DE REGIONAIS
if options == 'Mapas Alimentadores':
    regional = st.sidebar.selectbox(
        'Regional',
        alimentadores_validados['Regional'].unique()
    )


if options == 'Mapas Alimentadores':
    st.write(f"Regional selecionada: {regional}")
# Filtrar a rede para obter o polígono correspondente ao alimentador atual
rede = base_completa[base_completa['Linha'].isin(alimentadores_validados['Alimentador'])]

    # Adicionar a coluna 'Regional' ao DataFrame resultante
rede_regional = pd.merge(rede, alimentadores_validados[['Alimentador', 'Regional']], left_on='Linha', right_on='Alimentador', how='left')

# Certifique-se de que regional é uma lista, mesmo que tenha apenas um valor
regional = [regional] if isinstance(regional, str) else regional

# Agora você pode usar a variável 'regional' para filtrar o DataFrame
regiao_df = rede_regional[rede_regional['Regional'].isin(regional)]

if options == 'Mapas Alimentadores':
    alimentadores = st.sidebar.selectbox(
        'Alimentador',
        regiao_df['Alimentador'].unique()
    )

### Centroides Localidades 
sim_geo = gpd.GeoSeries(regiao_df['geometry'])
geo_json_data = regiao_df.to_json()
centroides = regiao_df.iloc[[0]].to_crs(22182).centroid.to_crs(4326)
centroide=regiao_df.iloc[[0]].to_crs(22182).centroid.to_crs(4326)   
    
    # Criar o mapa folium
mapa = folium.Map(location=[centroide.y,centroide.x ], zoom_start=13, width=1900, height=900)




for _, basemap in basemaps.items():
    basemap.add_to(mapa)

    
    folium.Choropleth(geo_data=shp_AR1, fill_color='orange', name='ASRO').add_to(mapa)
    folium.Choropleth(geo_data=shp_AR2, fill_color='beige', name='COMUNIDADES_DOMINADAS_PELA_MILICIA').add_to(mapa)
    folium.Choropleth(geo_data=shp_AR3, fill_color='pink', name='COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS').add_to(mapa)
    folium.Choropleth(geo_data=shp_AR4, fill_color='yellow', name='COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO').add_to(mapa)
    folium.Choropleth(geo_data=shp_AR5, fill_color='salmon', name='COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO').add_to(mapa)
    # folium.Choropleth(geo_data=regionais1, fill_color='blue', fill_opacity=0.2, name='Vale do Paraíba').add_to(mapa)
    # folium.Choropleth(geo_data=regionais2, fill_color='green', fill_opacity=0.2, name='Baixada').add_to(mapa)
    # folium.Choropleth(geo_data=regionais3, fill_color='red', fill_opacity=0.2, name='Leste').add_to(mapa)
    # folium.Choropleth(geo_data=regionais4, fill_color='purple', fill_opacity=0.2, name='Oeste').add_to(mapa)
    # folium.Choropleth(geo_data=regionais5, fill_color='gray', fill_opacity=0.2, name='Centro Sul').add_to(mapa)

if options == 'Mapas Alimentadores':
    folium.GeoJson(regiao_df, name=f'Regional: {regiao_df}').add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

if options == 'Mapas Alimentadores':
    folium_static( mapa )
mapa.save("mapa_teste.html")