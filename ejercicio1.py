import pandas as pd
import matplotlib.pyplot as pld


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
    presentar_datos(df,lista_resultados)
    
def presentar_datos(df, resultados):
    valor_x = df['type'].unique()
    valor_y = df['type'].value_counts().tolist()
    pld.bar(valor_x, valor_y)
    pld.show()
    pld.close('all')

if __name__ == '__main__':
    recopilar_datos()
