import requests
import folium
from folium import plugins
from folium.plugins import FloatImage

titulo = 'Mapa de Cadastros Realizados pela Secretaria de Agricultura'
titulo_html = '''
             <h3 align="center" style="font-size:20px"><b>{}</b></h3>
             '''.format(titulo)

mapa = folium.Map(location=[-13.34, -39.68], zoom_start=11, control_scale=True)
folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr= 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                 name= 'Esri.WorldImagery').add_to(mapa)

mapa.get_root().html.add_child(folium.Element(titulo_html))

url = ('https://raw.githubusercontent.com/cleitoncajueiro/mapa_cadastros_ubaira/main/Rosa%20dos%20Ventos.png')
FloatImage(url, bottom=0, left=90, width = '10%',).add_to(mapa)

imoveis = requests.get(
    "https://raw.githubusercontent.com/cleitoncajueiro/mapa_cadastros_ubaira/main/Clientes_secretaria.geojson"
).json()

ubaira = requests.get(
    "https://raw.githubusercontent.com/cleitoncajueiro/mapa_cadastros_ubaira/main/Ubaira.geojson"
).json()

bahia = requests.get(
    "https://raw.githubusercontent.com/cleitoncajueiro/mapa_cadastros_ubaira/main/Bahia.geojson"
).json()

folium.GeoJson(
    imoveis,
    name="Imóveis Rurais",
    tooltip='Imóvel',
    style_function=lambda feature: {
        'fillColor': 'green',  # Cor verde
        'color': 'green',  # Borda verde
        'weight': 4,  # Espessura da borda
        'fillOpacity': 0.2  # Transparente
    }
).add_to(mapa)

folium.GeoJson(
    ubaira,
    name="Ubaíra",
    style_function=lambda feature: {
        'fillColor': 'yellow',  # Cor amarela
        'color': 'yellow',  # Borda amarela
        'weight': 2,  # Espessura da borda
        'fillOpacity': 0  # Transparente
    }
).add_to(mapa)

folium.GeoJson(
    bahia,
    name="Limites De Municipios da Bahia",
    style_function=lambda feature: {
        'fillColor': 'gray',  # Cor cinza
        'color': 'gray',  # Borda cinza
        'weight': 1,  # Espessura da borda
        'fillOpacity': 0  # Transparente
    }
).add_to(mapa)

folium.LayerControl().add_to(mapa)

mapa.add_child(folium.LatLngPopup())

mapa.save('index.html')
