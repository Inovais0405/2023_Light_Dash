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
from shapely.ops import unary_union
import os
#import json
#from shapely.geometry import mapping
from shapely import wkt
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader
from PIL import Image



# Leitura e processamento dos dados


path_resultados = "BASE_DADOS/"
#alimentadores_validados = alim_validados(path_alimentadores_validados)

resultados_fme = pd.read_pickle(path_resultados + '01_13.12.2023_Extracao_Trechos_alimentadores.pkl')


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

def style_function(feature):
            # Obtém o código da propriedade do GeoJson
    codigo = feature['properties'].get('CODIGO')
            
            # Define a cor com base no status
    color = (
        'gray' if codigo in regiao_df_mapas_gdf[regiao_df_mapas_gdf['status'] == 'planejamento']['CODIGO'].values 
        else 'yellow' if codigo in regiao_df_mapas_gdf[regiao_df_mapas_gdf['status'] == 'campo']['CODIGO'].values
        else 'orange' if codigo in regiao_df_mapas_gdf[regiao_df_mapas_gdf['status'] == 'postagem']['CODIGO'].values
        else 'red' if codigo in regiao_df_mapas_gdf[regiao_df_mapas_gdf['status'] == 'conciliacao']['CODIGO'].values
        else 'green' if codigo in regiao_df_mapas_gdf[regiao_df_mapas_gdf['status'] == 'concluido']['CODIGO'].values
        else 'blue'
        )

            

    return {'color': color, 'weight': 2}






# Setando pagina do stream lit

st.set_page_config(layout="wide")#, page_icon = "D:/2023_Light_Dash/logo.png")

# Titulo heade
#

image = Image.open('logo.png')
st.image(image)

  
st.header('Inventário Light',divider='gray')
st.subheader('-  1°  Onda', divider='gray')


# Autenticador Streamlit

    #Importação Yaml
with open('Credencias.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)


    #Criar objeto autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
    #Renderizando o widget

name, authentication_status, username = authenticator.login('Login', 'main')


    #Autenticando opcao 1

if authentication_status:
    authenticator.logout('Logout', 'main')

    # Conteudo
    #st.set_page_config(layout='centered')
    st.write(f'Welcome *{name}*')

        # Titulo html
    
    
    # custom_html = """
    # <div style="max-width: 1000px; margin: 0 auto;">
    #     <div style="background-color: #009B91; padding: 20px; text-align: center; width: 100%;">
    #         <h1 style="color: white;">Inventário LIGHT - Primeira Onda</h1>
    #     </div>
    # </div>
    # """
    # st.markdown(custom_html, unsafe_allow_html=True)
    
    # Abas



        #Definição das abas
        
    tab1, tab2 = st.tabs(["Painel Gerencial", "Mapas"])

        # Power BI

    with tab1:

        Power_bi_code = '''
        <iframe title="15.12.2023_Light_Status_Inventario_v2_st" 
                width="100%" height="600" 
                src="https://app.powerbi.com/view?r=eyJrIjoiZjMyMTM2NjctZjlmMy00MTQ4LThkMTMtMjBhMTYyOWNiMjM2IiwidCI6IjVkMjkzNTZkLTYwOWQtNDQ0Zi1hMjJmLTlkMzgwMjJiMDBlZiJ9" 
                frameborder="0" 
                allowFullScreen="true">
        </iframe>
        
        '''
        st.markdown(Power_bi_code,unsafe_allow_html=True)

        # Mapas
    with tab2:
       
        regional = st.selectbox(
        'Regional',
        resultados_fme['REGIONAL'].unique()
        )

        regional = [regional] if isinstance(regional, str) else regional
        regiao_df = resultados_fme[resultados_fme['REGIONAL'].isin(regional)]

        alimentadores = st.selectbox(
            'Linha',
            regiao_df['ALIMENTADOR'].unique()
            )

        alimentadores = [alimentadores] if isinstance(alimentadores, str) else alimentadores
        regiao_df = resultados_fme[resultados_fme['ALIMENTADOR'].isin(alimentadores)]

        regiao_df_mapas = pd.read_excel('regiao_df_mapas.xlsx')

        regiao_df_mapas['geometry'] = regiao_df_mapas['geometry'].apply(wkt.loads)

        regiao_df_mapas_gdf = gpd.GeoDataFrame(regiao_df_mapas, geometry='geometry')

            

        

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
            folium.Choropleth(geo_data=shp_data, fill_color=color, name=name).add_to(mapa)

        # Adição de GeoJson para polígonos
        GeoJson(regiao_df, name=f'{alimentadores}').add_to(mapa)

        # # Função de estilo
        # def style_function(feature):
        #     codigo = feature['properties']['CODIGO']  # Obtém o código da propriedade do GeoJson
        #     color = 'red' if codigo in codigo_selected else 'blue'  # Define a cor com base na seleção

        #     return {'color': color, 'weight': 2}
        
        # # Adicionar GeoJson ao mapa com a função de estilo
        # geojson_layer = GeoJson(regiao_df.to_json(), style_function=style_function).add_to(mapa)

        if regiao_df['ALIMENTADOR'].tolist() == regiao_df_mapas_gdf['ALIMENTADOR'].tolist():
            # As séries têm os mesmos valores
            geojson_layer = GeoJson(regiao_df_mapas_gdf.to_json(), style_function=style_function).add_to(mapa)

            # Calcular o percentual de progresso
            total_codigos_alimentador = regiao_df_mapas_gdf['CODIGO'].nunique()
            codigos_selecionados = len(regiao_df_mapas_gdf[regiao_df_mapas_gdf['status'] == 'campo']['CODIGO'])
            percentual_progresso = (codigos_selecionados / total_codigos_alimentador) * 100

            # Mostrar o título com o percentual de progresso
            st.write(f"Progresso: {percentual_progresso:.2f}%")
        else:
            # As séries não têm os mesmos valores
            st.write("Não iniciou o inventário dessa Linha.")



        

        

        # Adicionar controle de camadas
        folium.LayerControl().add_to(mapa)

        # Adicionar controle de tela cheia
        plugins.Fullscreen().add_to(mapa)

        

        # Exibir mapa 
        folium_static(mapa)
    



        if st.button("Baixar Mapa como HTML"):
            # Caixa de texto para inserir o caminho
            caminho_salvar = st.text_input("Arquivo:", value= alimentadores[0] + ".html")

            if caminho_salvar:
                # Adicionar o arquivo temporário para download
                st.download_button(
                    label="Clique para baixar",
                    data=mapa.get_root().render(),
                    file_name=os.path.join(caminho_salvar),
                    key="download_mapa_html"
                )


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
    







