import streamlit as st
import geopandas as gpd
import pandas as pd
# import fiona
# from fiona.drvsupport import supported_drivers
import folium
from folium import Map, FeatureGroup, Marker, LayerControl, Popup
from streamlit_folium import folium_static
from folium import Choropleth, GeoJson, plugins
from shapely.ops import unary_union
import os


pasta_ARisco = "BASE_DADOS/AR_geojson/"
pasta_pickle = "BASE_DADOS/Auditorias/AR"
def ler_area_de_risco(pasta_ARisco, pasta_pickle):
    shp_AR0 = gpd.read_file(pasta_ARisco + 'ACAC.json')
    shp_AR1 = gpd.read_file(pasta_ARisco + 'ASRO.geojson')
    shp_AR2 = gpd.read_file(pasta_ARisco + 'COMUNIDADES_DOMINADAS_PELA_MILICIA.geojson')
    shp_AR3 = gpd.read_file(pasta_ARisco + 'COMUNIDADES_DOMINADAS_PELO_AMIGOS_DOS_AMIGOS.geojson')
    shp_AR4 = gpd.read_file(pasta_ARisco + 'COMUNIDADES_DOMINADAS_PELO_COMANDO_VEMELHO.geojson')
    shp_AR5 = gpd.read_file(pasta_ARisco + 'COMUNIDADES_DOMINADAS_PELO_TERCEIRO_COMANDO_PURO.geojson')

    shp_AR0 = shp_AR0[shp_AR0['geometry'].geom_type == 'Polygon']
    shp_AR1 = shp_AR1[shp_AR1['geometry'].geom_type == 'Polygon']
    shp_AR2 = shp_AR2[shp_AR2['geometry'].geom_type == 'Polygon']
    shp_AR3 = shp_AR3[shp_AR3['geometry'].geom_type == 'Polygon']
    shp_AR4 = shp_AR4[shp_AR4['geometry'].geom_type == 'Polygon']
    shp_AR5 = shp_AR5[shp_AR5['geometry'].geom_type == 'Polygon']

    shp_AR0 = shp_AR0.to_crs('EPSG:4674')
    shp_AR1 = shp_AR1.to_crs('EPSG:4674')
    shp_AR2 = shp_AR2.to_crs('EPSG:4674')
    shp_AR3 = shp_AR3.to_crs('EPSG:4674')
    shp_AR4 = shp_AR4.to_crs('EPSG:4674')
    shp_AR5 = shp_AR5.to_crs('EPSG:4674')

    shp_AR0.to_pickle(pasta_pickle +"/shp_AR0.pkl")
    shp_AR1.to_pickle(pasta_pickle +"/shp_AR1.pkl")
    shp_AR2.to_pickle(pasta_pickle +"/shp_AR2.pkl")
    shp_AR3.to_pickle(pasta_pickle +"/shp_AR3.pkl")
    shp_AR4.to_pickle(pasta_pickle +"/shp_AR4.pkl")
    shp_AR5.to_pickle(pasta_pickle +"/shp_AR5.pkl")

    return


ler_area_de_risco(pasta_ARisco, pasta_pickle)