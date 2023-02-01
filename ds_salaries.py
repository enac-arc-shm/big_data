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
    return df[['job_title','experience_level','salary_in_usd', 'employee_residence']]


def modelo_analisis(df):
    mean_levels = {}
    max = 0
    min = 10000000
    country_max = ''
    country_min = ''
    df_query = df.query("job_title == 'Data Scientist'")
    experiencie_level = df_query['experience_level'].unique().tolist()
    for level in experiencie_level:
        df_salary_query = df.query(f"experience_level == '{level}'")
        mean_levels[level] = df_salary_query['salary_in_usd'].mean()

    countries = df['employee_residence'].unique().tolist()
    for country in countries:
        df_mean_country = df.query(f"employee_residence == '{country}'")
        if df_mean_country['salary_in_usd'].mean() > max:
            max = df_mean_country['salary_in_usd'].mean()
            country_max = country
        if df_mean_country['salary_in_usd'].mean() < min:
            min = df_mean_country['salary_in_usd'].mean()
            country_min = country
        print(f"{country} {df_mean_country['salary_in_usd'].mean()}")
    info = {
        'Promedio general':df['salary_in_usd'].mean(),
        f'País con mas ingresos  {country_max}':max,
        f'País con menos ingresos  {country_min}':min
    }
    return mean_levels, info

def grafica_barras(data):
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
    valor_x = data.keys()
    valor_y = data.values()
    plt.bar(valor_x, valor_y, color = colores)
    plt.savefig("Data/img/ds_salaries_fig_1.png")
    plt.close('all')


def generar_informe(mean_levels, info):
    name =  "Data/informes/informe_ds_salaries.pdf"
    grafica_barras(mean_levels)
    #grafica_barras(count_crimes, count_crimes_none)
    pdf.add_page()
    pdf.set_font("Arial", size = 25)
    pdf.cell(200, 10, txt = "INFORME", ln = 1, align = 'C')
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Salary tecnological jobs statistic", ln = 2, align = 'C')
    pdf.image("Data/img/ds_salaries_fig_1.png", 25,35,150)
    pdf.add_page()
    n = 1
    for key, data in info.items():
         pdf.cell(200, 5, txt =  f"{key} ---->      ${data}", ln = n)
         n+=1
    pdf.cell(200, 30, txt =  "------------------------------------------------------------------------------------------------------------", ln = 20)
    pdf.cell(200, 20, txt =  "TOMA DE DECISIONES:", ln = 20)
    pdf.cell(200, 5, txt =  "De acuerdo a los resultados obtenidos, nos damos cuenta que en el promedio de  ", ln = 5)
    pdf.cell(200, 5, txt =  "salario dado para el nivel SE con respecto a los otros niveles es visiblemente ", ln = 6)
    pdf.cell(200, 5, txt =  "mayor en comparación a MI y EN siendo este ultimo el más bajo de los 3.", ln = 7)  
    pdf.cell(200, 5, txt =  "Por otro lado nos podemos dar cuenta que la diferencia de salarios entre los  ", ln = 8)   
    pdf.cell(200, 5, txt =  "diferentes paises es muy notable principalmente en la comparación del país  ", ln = 9)   
    pdf.cell(200, 5, txt =  "con mejor salario en comparación con el peor, es por tanto que debemos de ", ln = 10)   
    pdf.cell(200, 5, txt =  "centrar la atención en por que esta diversidad en los salarios, en la calidad", ln = 11)   
    pdf.cell(200, 5, txt =  "u otros aspectos que pueden verse implicados", ln = 12)   
    pdf.cell(200, 5, txt =  f"Fecha: {get_date()}", ln = 13)
    pdf.output(name)


def generar_mapa(df):
    map_crime = folium.Map(location = [df['Y'].mean(), df['X'].mean()], zoom_start=15)
    list_category = df['Category'].unique().tolist()
    colors = ['red', 'black', 'blue', 'green', 'gray', 'purple', 'orange']
    icons = ['glyphicon-usd', 'glyphicon-folder-open', 'glyphicon-dashboard', 'glyphicon-thumbs-down', 'glyphicon-remove', 'glyphicon-remove-sign', 'glyphicon-remove-circle']
    contador = 0
    for category in list_category:
        df_category = df.query(f"Category == '{category}'")
        if len(df_category.index) > 1500:
            folium.Marker([df_category['Y'].mean(), df_category['X'].mean()], popup=f"Concurrencia de criemenes de {category}", icon=folium.Icon(icon=f'{icons[contador]}', color=f'{colors[contador]}')).add_to(map_crime)
            folium.CircleMarker([df_category['Y'].mean(), df_category['X'].mean()], radius = 80, color = f'{colors[contador]}' ,popup=f"Concurrencia de criemenes de {category}", fill_color=f'{colors[contador]}').add_to(map_crime)
            contador += 1
    map_crime.save('Data/HTML/Map-Crime_incidents_recurrents.html')


if __name__ == '__main__':
    data = recopilar_datos()
    data_prepared = preparar_datos(data)
    mean_levels, info = modelo_analisis(data_prepared)
    generar_informe(mean_levels, info)
    

