# Tratamiento de datos
# ==============================================================================
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y análisis
# ==============================================================================
import statsmodels.api as sm
import pingouin as pg
from scipy import stats
from scipy.stats import pearsonr

# Configuración matplotlib
# ==============================================================================
plt.style.use('ggplot')

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

# Display information 
# ==============================================================================
from IPython.display import display


def correlacion_lineal():
    def generar_grafico_dispersion():
        # Gráfico
        # ==============================================================================
        fig, ax = plt.subplots(1, 1, figsize=(6,4))
        ax.scatter(x=datos.height, y=datos.weight, alpha= 0.8)
        ax.set_xlabel('Altura')
        ax.set_ylabel('Peso')
        plt.show()

    def generar_grafico_distibucion_variables():
        # Gráfico distribución variables
        # ==============================================================================
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

        axs[0].hist(x=datos.height, bins=20, color="#3182bd", alpha=0.5)
        axs[0].plot(datos.height, np.full_like(datos.height, -0.01), '|k', markeredgewidth=1)
        axs[0].set_title('Distribución altura (height)')
        axs[0].set_xlabel('height')
        axs[0].set_ylabel('counts')

        axs[1].hist(x=datos.weight, bins=20, color="#3182bd", alpha=0.5)
        axs[1].plot(datos.weight, np.full_like(datos.weight, -0.01), '|k', markeredgewidth=1)
        axs[1].set_title('Distribución peso (weight)')
        axs[1].set_xlabel('weight')
        axs[1].set_ylabel('counts')

        plt.tight_layout()
        plt.show()

    def generar_grafico_q_q():
        # Gráfico Q-Q
        # ==============================================================================
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

        sm.qqplot(
            datos.height,
            fit   = True,
            line  = 'q',
            alpha = 0.4,
            lw    = 2,
            ax    = axs[0]
        )
        axs[0].set_title('Gráfico Q-Q height', fontsize = 10, fontweight = "bold")
        axs[0].tick_params(labelsize = 7)

        sm.qqplot(
            datos.height,
            fit   = True,
            line  = 'q',
            alpha = 0.4,
            lw    = 2,
            ax    = axs[1]
        )
        axs[1].set_title('Gráfico Q-Q height', fontsize = 10, fontweight = "bold")
        axs[1].tick_params(labelsize = 7)
        plt.show()

    
    def normalidad_residuos_Shapiro():
        # Normalidad de los residuos Shapiro-Wilk test
        # ==============================================================================
        shapiro_test = stats.shapiro(datos.height)
        print(f"Variable height: {shapiro_test}")
        shapiro_test = stats.shapiro(datos.weight)
        print(f"Variable weight: {shapiro_test}")

    def normalidad_residuos_Agostino():
        # Normalidad de los residuos D'Agostino's K-squared test
        # ==============================================================================
        k2, p_value = stats.normaltest(datos.height)
        print(f"Variable height: Estadítico = {k2}, p-value = {p_value}")
        k2, p_value = stats.normaltest(datos.weight)
        print(f"Variable weight: Estadítico = {k2}, p-value = {p_value}")

    def trasformacion_logaritmica_datos():
        # Transformación logarítmica de los datos
        # ==============================================================================
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))

        sm.qqplot(
            np.log(datos.height),
            fit   = True,
            line  = 'q',
            alpha = 0.4,
            lw    = 2,
            ax    = ax
        )
        ax.set_title('Gráfico Q-Q log(height)', fontsize = 13)
        ax.tick_params(labelsize = 7)


        shapiro_test = stats.shapiro(np.log(datos.height))
        print(f"Variable height: {shapiro_test}")
        plt.show()

    def correlacion_pandas():
        # Cálculo de correlación con Pandas
        # ==============================================================================
        print('Correlación Pearson: ', datos['weight'].corr(datos['height'], method='pearson'))
        print('Correlación spearman: ', datos['weight'].corr(datos['height'], method='spearman'))
        print('Correlación kendall: ', datos['weight'].corr(datos['height'], method='kendall'))

    def correlacion_scipy():
        # Cálculo de correlación y significancia con Scipy
        # ==============================================================================
        r, p = stats.pearsonr(datos['weight'], datos['height'])
        print(f"Correlación Pearson: r={r}, p-value={p}")

        r, p = stats.spearmanr(datos['weight'], datos['height'])
        print(f"Correlación Spearman: r={r}, p-value={p}")

        r, p = stats.kendalltau(datos['weight'], datos['height'])
        print(f"Correlación Pearson: r={r}, p-value={p}")

    def correlacion_pingouin():
        # Cálculo de correlación, significancia e intervalos con pingouin
        # ==============================================================================
        display(pg.corr(datos['weight'], datos['height'], method='pearson'))
        display(pg.corr(datos['weight'], datos['height'], method='spearman'))
        display(pg.corr(datos['weight'], datos['height'], method='kendall'))


    url = ('https://raw.githubusercontent.com/JoaquinAmatRodrigo/' +
       'Estadistica-machine-learning-python/master/data/Howell1.csv')
    datos = pd.read_csv(url)

    # Se utilizan únicamente información de individuos mayores de 18 años.
    datos = datos[datos.age > 18]

    #Probar funciones 
    generar_grafico_dispersion()
    generar_grafico_distibucion_variables()
    generar_grafico_q_q()
    trasformacion_logaritmica_datos()
    correlacion_pingouin()
    

def Jackknife_correlation():
    def grafica_data_inicial():
        # Gráfico
        # ==============================================================================
        fig, ax = plt.subplots(1, 1, figsize=(6,4))
        ax.plot(a, label='A')
        ax.plot(b, label='B')
        ax.set_xlabel('ID muestra')
        ax.set_ylabel('Concentración')
        ax.set_title('Concentración sustancias A y B en las muestras')
        ax.legend()
        plt.show()

    def correlacion_pearson_ourlier():
        # Correlación con outlier
        r, p = stats.pearsonr(a, b)
        print(f"Correlación Pearson con outlier: r={r}, p-value={p}")

    def correlacion_pearson_nourlier():
        # Correlación sin outlier
        r, p = stats.pearsonr(np.delete(a, 5), np.delete(b, 5))
        print(f"Correlación Pearson sin outlier: r={r}, p-value={p}")

    # Función Jackknife correlation
    # ==============================================================================
    def correlacion_jackknife(x, y):
        '''
        Esta función aplica el método de Jackknife para el cálculo del coeficiente
        de correlación de Pearson.
        
        
        Parameters
        ----------
        x : 1D np.ndarray, pd.Series 
            Variable X.
            
        y : 1D np.ndarray, pd.Series
            Variable y.     

        Returns 
        -------
        correlaciones: 1D np.ndarray
            Valor de correlación para cada iteración de Jackknife
        '''
        
        n = len(x)
        valores_jackknife = np.full(shape=n, fill_value=np.nan, dtype=float)
        
        for i in range(n):
            # Loop para excluir cada observación y calcular la correlación
            r = stats.pearsonr(np.delete(x, i), np.delete(y, i))[0]
            valores_jackknife[i] = r

        promedio_jackknife = np.nanmean(valores_jackknife)
        standar_error = np.sqrt(((n - 1) / n) * \
                        np.nansum((valores_jackknife - promedio_jackknife) ** 2))
        bias = (n - 1) * (promedio_jackknife - stats.pearsonr(x, y)[0])
        
        resultados = {
            'valores_jackknife' : valores_jackknife,
            'promedio'          : promedio_jackknife,
            'se'                : standar_error,
            'bias'              : bias
        }
        
        return resultados

    def correlacion_jackknife_apply():
        correlacion = correlacion_jackknife(x=a, y=b)
        print(f"Correlación jackknife: {correlacion['promedio']}")
        print(f"Error estándar: {correlacion['se']}")
        print(f"Error bias: {correlacion['bias']}")
        print(f"Valores_jackknife: {correlacion['valores_jackknife']}")

        # Grafia del cambio que se produce en el coeficiente 
        # ==============================================================================
        variacion_corr = correlacion['valores_jackknife'] - stats.pearsonr(a, b)[0]
        fig, ax = plt.subplots(1, 1, figsize=(6,4))
        ax.plot(variacion_corr)
        ax.set_xlabel('ID muestra')
        ax.set_ylabel('Variación correlación')
        plt.show()

    # Datos simulados de dos variables A y B
    a = np.array([12,9,6,7,2,5,4,0,1,8])
    b = np.array([3,5,1,9,5,3,7,2,10,5])

    # Se introduce un outlier
    a[5] = 20
    b[5] = 16

    correlacion_pearson_ourlier()
    correlacion_pearson_nourlier()
    correlacion_jackknife_apply()


def matriz_Correlaciones():

    def tidy_corr_matrix(corr_mat):
        '''
        Función para convertir una matriz de correlación de pandas en formato tidy.
        '''
        corr_mat = corr_mat.stack().reset_index()
        corr_mat.columns = ['variable_1','variable_2','r']
        corr_mat = corr_mat.loc[corr_mat['variable_1'] != corr_mat['variable_2'], :]
        corr_mat['abs_r'] = np.abs(corr_mat['r'])
        corr_mat = corr_mat.sort_values('abs_r', ascending=False)
        
        return(corr_mat)

    def Heatmap_matriz_correlaciones():
        # Heatmap matriz de correlaciones
        # ==============================================================================
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

        sns.heatmap(
            corr_matrix,
            annot     = True,
            cbar      = False,
            annot_kws = {"size": 8},
            vmin      = -1,
            vmax      = 1,
            center    = 0,
            cmap      = sns.diverging_palette(20, 220, n=200),
            square    = True,
            ax        = ax
        )

        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation = 45,
            horizontalalignment = 'right',
        )

        ax.tick_params(labelsize = 10)
        plt.show()

    # Datos
    # ==============================================================================
    url = ('https://raw.githubusercontent.com/JoaquinAmatRodrigo/' +
        'Estadistica-machine-learning-python/master/data/SaratogaHouses.csv')
    datos = pd.read_csv(url, sep=",")

    # Se renombran las columnas para que sean más descriptivas
    datos.columns = ["precio", "metros_totales", "antiguedad", "precio_terreno",
                    "metros_habitables", "universitarios", "dormitorios", 
                    "chimenea", "banyos", "habitaciones", "calefaccion",
                    "consumo_calefacion", "desague", "vistas_lago",
                    "nueva_construccion", "aire_acondicionado"]
        
    # Variables numéricas
    datos = datos.select_dtypes(include=['float64', 'int'])

    # Matriz de correlación
    # ==============================================================================
    corr_matrix = datos.corr(method='pearson')

    # Impresion
    # ==============================================================================
    print(corr_matrix)
    print(tidy_corr_matrix(corr_matrix).head(10))
    Heatmap_matriz_correlaciones()

def correlacion_parcial():
    url = ('https://raw.githubusercontent.com/JoaquinAmatRodrigo/' +
    'Estadistica-machine-learning-python/master/data/Cars93.csv')
    datos = pd.read_csv(url)
    datos['log_Price'] = np.log(datos.Price)

    # Gráfico
    # ==============================================================================
    fig, ax = plt.subplots(1, 1, figsize=(6,4))
    ax.scatter(x=datos.Weight, y=datos.log_Price, alpha= 0.8)
    ax.set_xlabel('Peso')
    ax.set_ylabel('Log(Precio)')
    plt.show()

    # Cálculo de correlación lineal
    # ==============================================================================
    print(pg.corr(x=datos['Weight'], y=datos['log_Price'], method='pearson'))


    # Cálculo de correlación lineal parcial
    # ==============================================================================
    print(pg.partial_corr(data=datos, x='Weight', y='log_Price', covar='Horsepower', method='pearson'))


if __name__ == '__main__':
    print('''
    Seleccione un metodo de correlacion:
    1.- Correlacion lineal
    2.- Jackknife_correlation
    3.- matriz_Correlaciones
    4.- correlacion_parcial
    
    ''')
    accion = int (input("[?] Option = "))
    if accion == 1:
        correlacion_lineal()

    if accion == 2:
        Jackknife_correlation()

    if accion == 3:
        matriz_Correlaciones()

    if accion == 4:
        correlacion_parcial()