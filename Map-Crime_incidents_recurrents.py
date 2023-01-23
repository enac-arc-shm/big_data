from reportlab.lib.pagesizes import letter
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import locale
import numpy as np



path_csv = "Data/Map-Crime_Incidents-Previous_Three_Months.csv"
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
    return df[['Category','Resolution' ,'X', 'Y']]


def modelo_analisis(df):
    count_crimes = {}
    count_crimes_none = {}
    list_category = df['Category'].unique().tolist()
    for category in list_category:
        df_category = df.query(f"Category == '{category}'")
        if len(df_category.index) > 1500:
            count_crimes[category] = len(df_category.index)
            df_resoulution = df_category[df_category['Resolution'] == 'NONE']
            count_crimes_none[category] = len(df_resoulution.index)
    return count_crimes, count_crimes_none

def grafica_barras(data_total, data_none):
    labels = data_total.keys()
    total_crimes = data_total.values()
    crimes_none = data_none.values()
    x = np.arange(len(labels))
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, total_crimes, width, label='Crimes', color='black')
    rects2 = ax.bar(x + width/2, crimes_none, width, label='No resolution', color='red')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count crimes')
    ax.set_title('Total vs no resoults')
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    #fig = plt.figure(figsize=(15, 15))
    fig.tight_layout()
    plt.gcf().set_size_inches(10, 5)
    plt.savefig("Data/img/Map-Crime_incidents_recurrents_fig_2.png")
    plt.close('all')
    

def grafica_circular(data):
    values =  data.values()
    labels =  data.keys()
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
    plt.pie(values, labels=labels, autopct="%0.1f %%", colors=colores)
    plt.axis("equal")
    plt.savefig("Data/img/Map-Crime_incidents_recurrents_fig_1.png")
    plt.close('all')


def generar_informe(count_crimes, count_crimes_none):
    name =  "Data/informes/informe_Map-Crime_incidents_recurrents.pdf"

    grafica_circular(count_crimes)
    grafica_barras(count_crimes, count_crimes_none)
    pdf.add_page()
    pdf.set_font("Arial", size = 25)
    pdf.cell(200, 10, txt = "INFORME", ln = 1, align = 'C')
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "MAP crime incidents", ln = 2, align = 'C')
    pdf.image("Data/img/Map-Crime_incidents_recurrents_fig_1.png", 25,35,150)
    pdf.image("Data/img/Map-Crime_incidents_recurrents_fig_2.png", 25,150,150)
    pdf.add_page()
    pdf.cell(200, 150, txt =  "", ln = 1)
    pdf.cell(200, 5, txt =  "TOMA DE DECISIONES:", ln = 2)
    pdf.cell(200, 5, txt =  "De acuerdo a los resultados obtenidos, nos damos cuenta que en la mayoría de casos de crimen según la zona, no son resueltos. ", ln = 3)
    pdf.cell(200, 5, txt =  "El crimen más común es el de larceny/theft, y este mismo crimen, es el que menos resoluciones tiene, por lo que, deberían tomar acciones ante este.", ln = 4)
    pdf.cell(200, 5, txt =  f"Fecha: {get_date()}", ln = 5)
    pdf.output(name)

if __name__ == '__main__':
    data = recopilar_datos()
    data_prepared = preparar_datos(data)
    count_crimes, count_crimes_none = modelo_analisis(data_prepared)
    generar_informe(count_crimes, count_crimes_none)
    