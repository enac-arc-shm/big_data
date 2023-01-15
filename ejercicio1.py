import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def add_image(image_path):
    my_canvas = canvas.Canvas("canvas_image.pdf", pagesize=letter)
    my_canvas.drawImage(image_path, 30, 600, width=100, height=100)
    my_canvas.save()

def recopilar_datos():
    fuente_datos = input("Ingresa la ruta del archivo: ")
    fuente_datos = "Data/malicious_phish.csv"
    df = pd.DataFrame(pd.read_csv(fuente_datos))
    preparar_datos(df)

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
    valor_x = df['type'].unique()
    valor_y = df['type'].value_counts().tolist()
    plt.bar(valor_x, valor_y)
    plt.savefig("Data/Img/figura1.png")
    plt.close('all')

def grafica_circular(df, resultados):
    fig, ax = plt.subplots()
    ax.pie(df['type'].value_counts().tolist())
    plt.show()

def generar_informe():
    name = input("Ingrese el nombre del informe: ") 

if __name__ == '__main__':
    recopilar_datos()
    #image_path = 'snakehead.jpg'
    #add_image(image_path)
