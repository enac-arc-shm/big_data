from reportlab.lib.pagesizes import letter
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import locale
import numpy as np
import folium

path_csv = "Data/ds_salaries.csv"
pdf = FPDF()


def get_date():
    locale.setlocale(locale.LC_ALL, '')
    fecha_actual = datetime.datetime.now()
    return(fecha_actual.strftime('%A, %-d de %B de %Y'))


def recopilar_datos():
    fuente_datos = input("Ingresa la ruta del archivo csv: ")
    fuente_datos = path_csv
    return pd.DataFrame(pd.read_csv(fuente_datos))
    

def preparar_datos(df):
    return df[['job_title','salary_in_usd', 'employee_residence']]


def modelo_analisis(df):
    data = {}
    df_mx = df.query("employee_residence == 'MX'")
    df_min = df_mx.query(f"salary_in_usd == {df_mx['salary_in_usd'].min()}")
    df_max = df_mx.query(f"salary_in_usd == {df_mx['salary_in_usd'].max()}")
    data['maximo'] = f"{df_max.iloc[0]['job_title']} --> {df_max.iloc[0]['salary_in_usd']}"
    data['minimo'] = f"{df_min.iloc[0]['job_title']} --> {df_min.iloc[0]['salary_in_usd']}"
    return data


def generar_mapa(data):
    map_crime = folium.Map(location = [23.634501, -102.552784], zoom_start=5)
    colors = ['red', 'black', 'blue', 'green', 'gray', 'purple', 'orange']
    icons = ['glyphicon-usd', 'glyphicon-folder-open', 'glyphicon-dashboard', 'glyphicon-thumbs-down', 'glyphicon-remove', 'glyphicon-remove-sign', 'glyphicon-remove-circle']
    folium.Marker([20.66682,-103.39182], popup=data["maximo"], icon=folium.Icon(icon=f'{icons[1]}', color=f'{colors[1]}')).add_to(map_crime)
    folium.Marker([25.67507,-100.31847], popup=data["minimo"], icon=folium.Icon(icon=f'{icons[2]}', color=f'{colors[2]}')).add_to(map_crime)
    folium.Marker([19.42847,-99.12766], popup="Data scient ingener", icon=folium.Icon(icon=f'{icons[3]}', color=f'{colors[3]}')).add_to(map_crime)
    map_crime.save('Data/HTML/ds_salaries_2".html')


if __name__ == '__main__':
    data = recopilar_datos()
    data_prepared = preparar_datos(data)
    data = modelo_analisis(data_prepared)
    generar_mapa(data)

