from reportlab.lib.pagesizes import letter
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import locale



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
    df = df[df['Category'] == 'ASSAULT']
    df = df[df['DayOfWeek'] == 'Sunday']
    df_PdDistrict = df[df.PdDistrict.isin(["RICHMOND", "SOUTHERN", "MISSION"])]
    #print(df_PdDistrict[['Category', 'DayOfWeek','PdDistrict']])  
    return df_PdDistrict[['PdDistrict', 'X', 'Y', 'Location']]


def modelo_analisis(df):
    df_data_MISSION = df.query("PdDistrict == 'MISSION'")
    df_data_RICHMOND = df.query("PdDistrict == 'RICHMOND'")
    df_data_SOUTHERN = df.query("PdDistrict == 'SOUTHERN'")
    #print(df_data_MISSION['PdDistrict'].value_counts())
    return df_data_MISSION, df_data_RICHMOND, df_data_SOUTHERN
    
def grafica_barras(df):
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
    valor_x = df['PdDistrict'].unique()
    valor_y = df['PdDistrict'].value_counts().tolist()
    plt.bar(valor_x, valor_y, color = colores)
    plt.savefig("Data/img/Map-Crime_Incidents_fig_1.png")
    plt.close('all')
    

def grafica_circular(df):
    values =  df['PdDistrict'].value_counts().tolist()
    labels =  df['PdDistrict'].unique()
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
    desfase = (0, 0, 0, 0.1)
    #print(values, labels)
    plt.pie(values, labels=labels, autopct="%0.1f %%", colors=colores)
    #plt.show()
    plt.axis("equal")
    plt.savefig("Data/img/Map-Crime_Incidents_fig_2.png")
    plt.close('all')


def generar_informe(df, MISSION, RICHMOND, SOUTHERN):
    grafica_barras(df)
    grafica_circular(df)

    name =  "Data/informes/informe_Map-Crime_Incidents.pdf"
    pdf.add_page()
    pdf.set_font("Arial", size = 25)
    pdf.cell(200, 10, txt = "INFORME", ln = 1, align = 'C')
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "MAP crime incidents", ln = 2, align = 'C')
    pdf.image("Data/img/Map-Crime_Incidents_fig_1.png", 25,35,150)
    pdf.image("Data/img/Map-Crime_Incidents_fig_2.png", 25,150,150)
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    #print(MISSION['PdDistrict'].value_counts())
    for registro in range(int(MISSION['PdDistrict'].value_counts())):
        string_registro = ""
        for elemento in MISSION.iloc[registro]:
            string_registro += str(elemento)
            string_registro += "    "
        pdf.cell(200, 10, txt =  string_registro, ln = registro)
        #print(string_registro)
    for registro in range(int(RICHMOND['PdDistrict'].value_counts())):
        string_registro = ""
        for elemento in RICHMOND.iloc[registro]:
            string_registro += str(elemento)
            string_registro += "    "
        pdf.cell(200, 10, txt =  string_registro, ln = registro)
        #print(string_registro)

    for registro in range(int(SOUTHERN['PdDistrict'].value_counts())):
        string_registro = ""
        for elemento in SOUTHERN.iloc[registro]:
            string_registro += str(elemento)
            string_registro += "    "
        pdf.cell(200, 10, txt =  string_registro, ln = registro)
        #print(string_registro)
    pdf.output(name)

if __name__ == '__main__':
    data = recopilar_datos()
    data_prepared = preparar_datos(data)
    df_MISSION, df_RICHMOND, df_SOUTHERN =  modelo_analisis(data_prepared)
    generar_informe(data_prepared, df_MISSION, df_RICHMOND, df_SOUTHERN)
    