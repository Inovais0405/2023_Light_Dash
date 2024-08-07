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
from shapely import wkt
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader
from PIL import Image

# Caminho para os arquivos de dados
path_resultados = "BASE_DADOS/"

# Função para carregar os dados dos trechos dos alimentadores.
@st.cache_data
def load_data():
    resultados_fme = pd.read_pickle(path_resultados + '16-02-24_Trechos_alimentadores.pkl')
    return resultados_fme

# Função para carregar os dados do status dos alimentadores.
@st.cache_data
def load_BI():
    status_BI = pd.read_pickle(path_resultados + 'Status_alimentador.pkl')
    return status_BI

# Leitura de vários arquivos shape que serão utilizados no mapa.
shp_AR0 = pd.read_pickle(path_resultados + "shp_AR0.pkl")
shp_AR1 = pd.read_pickle(path_resultados + "shp_AR1.pkl")
shp_AR2 = pd.read_pickle(path_resultados + "shp_AR2.pkl")
shp_AR3 = pd.read_pickle(path_resultados + "shp_AR3.pkl")
shp_AR4 = pd.read_pickle(path_resultados + "shp_AR4.pkl")
shp_AR5 = pd.read_pickle(path_resultados + "shp_AR5.pkl")

# Definição de diferentes tipos de mapas base
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

# Configuração da página do Streamlit
st.set_page_config(layout="wide")

# Carrega a imagem do logotipo e exibe no topo da página
image = Image.open('logo.png')
st.image(image)

# Adiciona o cabeçalho e o subtítulo
st.header('Inventário Light',divider='gray')
st.subheader('-  1°  Onda', divider='gray')

# Autenticação do usuário utilizando o Streamlit Authenticator

# Carregamento dos dados de credenciais de um arquivo YAML
with open('Credencias.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Criação do objeto de autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Renderização do widget de login
name, authentication_status, username = authenticator.login('Login', 'main')

# Verifica se a autenticação foi bem-sucedida
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    # Criação das abas do Streamlit
    tab1, tab2, tab3 = st.tabs(["Painel Gerencial", "Produtividade", "Mapas"])

    # Conteúdo da aba "Painel Gerencial"
    with tab1:
        Power_bi_code = '''
        <iframe title="19.01.2023_Light_Status_Inventario_v3" width="1500" height="800" src="
        https://app.powerbi.com/view?r=eyJrIjoiYTNiZDQ2OGQtNjg3NC00YjBmLTk0ZGItNzRlMzAxY2YwZDQ2IiwidCI6IjVkMjkzNTZkLTYwOWQtNDQ0Zi1hMjJmLTlkMzgwMjJiMDBlZiJ9"
        frameborder="0" allowFullScreen="true"></iframe>
        '''
        st.markdown(Power_bi_code,unsafe_allow_html=True)

    # Conteúdo da aba "Produtividade"
    with tab2:
        Power_bi_code_produtividade = '''
        <iframe title="Inventário de Ativos_produtividade" width="1500" height="800" src="https://app.powerbi.com/view?r=eyJrIjoiNGRhOTI3NjQtOTVkNi00MWYxLTk1YjUtNmYwNWRmMmE5OTMxIiwidCI6IjVkMjkzNTZkLTYwOWQtNDQ0Zi1hMjJmLTlkMzgwMjJiMDBlZiJ9" frameborder="0" allowFullScreen="true"></iframe>
        '''
        st.markdown(Power_bi_code_produtividade,unsafe_allow_html=True)

    # Conteúdo da aba "Mapas"
    with tab3:
        # Carrega os dados
        resultados_fme = load_data()
        status_BI = load_BI()
        resultados_fme = resultados_fme.merge(status_BI, on='ALIMENTADOR')

        # Adiciona um espaço em branco para mover o select box para a direita
        st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction: row-reverse}</style>', unsafe_allow_html=True)

        # Criação do select box para selecionar a "Regional"
        regional = st.selectbox(
            'Regional',
            resultados_fme['REGIONAL'].unique()
        )
        regional = [regional] if isinstance(regional, str) else regional
        regiao_df = resultados_fme[resultados_fme['REGIONAL'].isin(regional)]

        # Mapeamento de status para cores
        status_colors = {
            'Em planejamento': 'gray',
            'Em campo': 'red',
            'Em postagem': 'yellow',
            'concluido': 'green',
            'Inventário Paralisado': 'orange'
        }

        # Adiciona uma coluna com as cores correspondentes aos status
        regiao_df['cor'] = regiao_df['Macro-Status'].map(status_colors)

        # Criação do select box para selecionar o "Status"
        status = st.selectbox(
            'Status',
            (regiao_df['Macro-Status'].unique()),
            index=None,
            placeholder="Selecione Status ..."
        )
        status = [status] if isinstance(status, str) else status
        if status != "Selecione Status ..." and isinstance(status, list):
            regiao_df = regiao_df[regiao_df['Macro-Status'].isin(status)]
        
        # Criação do select box para selecionar o "Alimentador"
        alimentadores = st.selectbox(
            'Linha',
            (regiao_df['ALIMENTADOR'].unique()),
            index=None,
            placeholder="Selecione a linha ..."
        )
        alimentadores = [alimentadores] if isinstance(alimentadores, str) else alimentadores
        if alimentadores != 'Selecione a linha ...' and isinstance(alimentadores, list):
            regiao_df = regiao_df[regiao_df['ALIMENTADOR'].isin(alimentadores)]

        with st.spinner("Carregando mapa..."):
            # Calcula o centróide para centralizar o mapa
            centroide = regiao_df.to_crs(22182).centroid.to_crs(4326).iloc[[0]]
            mapa = folium.Map(location=[centroide.y, centroide.x], zoom_start=13)

            # Adicionar basemaps ao mapa
            for name, tile_layer in basemaps.items():
                tile_layer.add_to(mapa)

            # Adição de regiões com diferentes formas e cores utilizando arquivos shape
            colors = ['orange', 'beige', 'pink', 'yellow', 'salmon']
            for name, shp_data, color in zip(['ASRO', 'COMUNIDADES_DOMINADAS_PELA_MILICIA', 'COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS', 'COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO', 'COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO'], [shp_AR1, shp_AR2, shp_AR3, shp_AR4, shp_AR5], colors):
                folium.Choropleth(geo_data=shp_data, fill_color='pink', name=name).add_to(mapa)

            # Template HTML para a legenda
            legend_html = """
            {%macro html(this,kwargs)%}
            <div id='maplegend' class='maplegend' 
                style='position: fixed; z-index: 9998; background-color: rgba(255, 255, 255, 0.5);
                bottom: 12px; left: 1350px; width: 120px; height: 110px; font-size: 10.5px; border: 1px solid gray; border-radius: 6px;'>
            <a style = "color: black; margin-left: 30px;"<><b>Legenda</b></a>     
            <div class='legend-scale'>
            <ul class='legend-labels' style="list-style-type: none; padding: 0; margin: 0;">
                <li><a style='color: gray; margin-left: 2px;'>&FilledSmallSquare; </a> Em planejamento </li>
                <li><a style='color: red; margin-left: 2px;'>&FilledSmallSquare; </a>Em campo </li>
                <li><a style='color: yellow; margin-left: 2px;'>&FilledSmallSquare; </a> Em postagem </li>
                <li><a style='color: green; margin-left: 2px;'>&FilledSmallSquare; </a>Concluído </li>
                <li><a style='color: orange; margin-left: 2px;'>&FilledSmallSquare; </a>Inventário Paralisado </li>
                <li><a style='color: pink; margin-left: 2px;'>&FilledSmallSquare; </a>Áreas de Risco </li>
            </ul>
            </div>
            {% endmacro %}
            """

            # Adiciona a legenda HTML ao mapa
            macro = branca.element.MacroElement()
            macro._template = branca.element.Template(legend_html)
            mapa.add_child(macro)

            # Adicionar GeoJson ao mapa com base na coluna de cor
            GeoJson(regiao_df, style_function=lambda feature: {'color': feature['properties']['cor'], 'weight': 2}).add_to(mapa)

        # Adiciona controle de camadas ao mapa
        folium.LayerControl().add_to(mapa)

        # Adiciona o controle de tela cheia
        plugins.Fullscreen().add_to(mapa)

        # Exibe o mapa na aplicação Streamlit
        folium_static(mapa, width=1500, height=800)

        # Botão para baixar o mapa como HTML
        if st.button("Baixar Mapa como HTML"):
            caminho_salvar = st.text_input("Arquivo:", value= regional[0] + ".html")
            if caminho_salvar:
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
