from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import locale



def get_date():
    locale.setlocale(locale.LC_ALL, '')
    fecha_actual = datetime.datetime.now()
    return(fecha_actual.strftime('%A, %-d de %B de %Y'))


def recopilar_datos():
    fuente_datos = input("Ingresa la ruta del archivo csv: ")
    #fuente_datos = "Data/malicious_phish.csv"
    df = pd.DataFrame(pd.read_csv(fuente_datos))
    return df
    

def preparar_datos(df):
    df.drop('url', axis = "columns")
    modelo_analisis(df)


def modelo_analisis(df):
    lista_resultados = []

    benign = df.query("type == 'benign'")
    total_benign = benign.count()
    lista_resultados +=  ["benign", total_benign ]

    defacement = df.query("type == 'defacement'")
    total_defacement = defacement.count()
    lista_resultados +=  ["defacement", total_defacement ]

    phishing = df.query("type == 'phishing'")
    total_phishing = phishing.count()
    lista_resultados +=  ["phishing", total_phishing ]

    malware = df.query("type == 'malware'")
    total_malware = malware.count()
    lista_resultados +=  ["malware", total_malware ]
    grafica_barras(df,lista_resultados)
    grafica_circular(df,lista_resultados)
    
def grafica_barras(df, resultados):
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
    valor_x = df['type'].unique()
    valor_y = df['type'].value_counts().tolist()
    plt.bar(valor_x, valor_y, color = colores)
    plt.savefig("Data/img/figura1.png")
    plt.close('all')
    

def grafica_circular(df, resultados):
    values =  df['type'].value_counts().tolist()
    labels =  df['type'].unique()
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
    desfase = (0, 0, 0, 0.1)
    plt.pie(values, labels=labels, autopct="%0.1f %%", colors=colores, explode=desfase)
    plt.axis("equal")
    plt.savefig("Data/img/figura2.png")
    plt.close('all')


def generar_informe(df):
    values =  df['type'].value_counts().tolist()
    labels =  df['type'].unique().tolist()
    name = "Data/informes/"
    name += input("Ingrese el nombre del informe: ")
    image_path_figure1 = 'Data/img/figura1.png'
    image_path_figure2 = 'Data/img/figura2.png'
    my_canvas = canvas.Canvas(name, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica', 30)
    my_canvas.drawString(120, 750, 'Reporte analisis de malware ')
    my_canvas.drawImage(image_path_figure1, 40, 400, width=250, height=250)
    my_canvas.drawImage(image_path_figure2, 340, 400, width=250, height=250)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(30, 250, 'INFORM OFICIAL ')
    my_canvas.drawString(410, 250, get_date())
    my_canvas.line(380, 247, 580, 247)
    y = 215
    for label in labels:
        my_canvas.drawString(30, y, label)
        y-=20
    y = 215
    total = 0
    for value in values: 
        my_canvas.drawString(550, y, str(value))
        y-=20
        total += value
    my_canvas.drawString(265, 125, 'TOTAL ANALIZADO:')
    my_canvas.drawString(500, 125, str(total))
    my_canvas.line(378, 123, 580, 123)
    my_canvas.drawString(30, 73, 'RESULTADO: CREAR UN SISTEMA DE PREVENCIÓN PRINCIPALMENTE ORIENTADO A PHISHING')
    my_canvas.drawString(30, 43, 'CREADO POR:')
    my_canvas.line(120, 40, 580, 40)
    my_canvas.drawString(120, 43, "SERGIO HERNANDEZ MARTINEZ")
    my_canvas.save()


if __name__ == '__main__':
    data = recopilar_datos()
    #preparar_datos(data)
    modelo_analisis(data)
    generar_informe(data)
    
