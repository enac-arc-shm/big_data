import folium

#leaflit libreria 

def generar_mapa():
    mapa = folium.Map(location=[45.5236, -122.6750], zoom_start=13, tiles='Mapbox')
    mapa.save('vancouber.html')

if __name__ == '__main__':
    generar_mapa()