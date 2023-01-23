import pandas as pd
import folium

def generar_mapa(asaltos):
    map_sf = folium.Map(location=[asaltos['X'].mean(), asaltos['Y'].mean()], zoom_start=12)
    folium.Marker([asaltos['Y'].mean(), asaltos['Y'].mean()], popup=f'Nombre:San francisco').add_to(map_sf)
    map_sf.save('Data/HTML/Folium_Map-Crime.html')

def mostrar_asaltos(asaltos):
    filtros = asaltos.query("Category == 'ASSAULT' and DayOfWeek == 'Saturday' and (PdDistrict == 'RICHMOND' or PdDistrict == 'SOUTHERN' or PdDistrict == 'MISSION')")
    map_sf = folium.Map(location = [asaltos['Y'].mean(), asaltos['X'].mean()], zoom_start=12)
    for index, filtro in filtros.iterrows():
        folium.Marker([filtro['Y'], filtro['X']], popup=f"NOmbre: {filtro['PdDistrict']} \n Hora: {filtro['Time']}", icon=folium.Icon(icon='heart-empty', color='black')).add_to(map_sf)
    map_sf.save('Data/HTML/Folium_Map-Crime.html')

if __name__ == '__main__':
    asaltos = pd.read_csv("Data/Map-Crime_Incidents-Previous_Three_Months.csv")
    mostrar_asaltos(asaltos)