import numpy as np
import matplotlib.pyplot as plt
import psicro as ps
from scipy.spatial import ConvexHull
import calendar

def graficar_carta_psicrometrica(temp_r, hr_c, data_frame,altura,linea1_visible,lineas2_visible, lineas3_visible, lineas4_visible):
    
    Ra = 287.055
    # Crear la figura y el eje
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Crear matrices de temperatura y HR
    temp_matrix, hr_matrix = np.meshgrid(temp_r, hr_c)
    # Calcular la humedad específica y ajustar la escala
    w_matrix = ps.humedad_especifica(temp_matrix, hr_matrix / 100) * 1000
    
    # GRafico delíneas constantes de HR utilizando w_matrix
    lineas4 = ax1.plot(temp_r, w_matrix.T, linestyle='dashed', color='white', alpha=1,visible= lineas4_visible)
   
    # Gráfico de Tbs vs W
    ax1.plot(data_frame["T2M"], data_frame["W (kg va / kg as)"] * 1000, marker='o', linestyle='', color='magenta', label="Datos Tbs vs W", visible= True)
    # Obtener puntos para el casco convexo
    points = np.column_stack((data_frame["T2M"], data_frame["W (kg va / kg as)"] * 1000))
    hull = ConvexHull(points)
    #Dibujar el casco convexo alrededor de los puntos o nube de puntos 
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-', alpha=1,color = 'red')

   
    # Encontrar los índices donde la humedad relativa es igual a 100 en la matriz w_matrix
    valores_maximos = np.amax(w_matrix.T, axis=1)
    #lineas de temperature
    lineas2 = plt.vlines(temp_r, ymin=0, ymax=valores_maximos, colors='white', linestyles='-', label='temperaturas', visible= lineas2_visible)

    #para las lineas de humedad de 5:85:5
    valores_w = np.arange(5,86,5)   
    tem_w  = [3.897,14.033,20.303,24.903,28.572,31.612,34.235,36.510,38.527,40.374,42.051,43.560,44.964,46.257,47.482,48.628,49.711] 
    lineas1 = ax1.hlines(valores_w, xmin=tem_w,xmax=50 ,colors = 'white',linestyle='-',label ="w", visible= linea1_visible)
    

    #humedad especifica
    
    #Ve = np.arange(0.78,0.93,0.01)
    #w = [4,5,6.5,7.5,9,11,13,15,17.5,20,23,26,29]
    #w = w/1000
    #print(Ve)
    #valores_maximos = ps.TBS(Ve,Ra,0,patm)
    
    #print(valores_maximos)

    #Lineas de temperatura de bulbo humedo ##########
    patm = ps.presion_atm(altura)
    tw = np.arange(0.000001, 50, 1)
    print(tw)
    twK = ps.Grados_Kelvin(tw)
    psv = ps.PresionVaporSaturada(twK)
    print(psv)
    yasat = ps.razonDehumedadSaturada(psv,patm)
    print(yasat)
    calorLa = np.array([597.452,596.883,596.315,595.747,595.18,594.614,594.047,593.481,592.915,592.35,
                        591.784,591.219,590.654,590.089,589.523,588.958,588.393,587.828,587.263,586.698,
                        586.132,585.567,585.001,584.435,583.869,583.303,582.736,582.17,581.603,581.035,
                        580.468,579.9,579.332,578.763,578.195,577.625,577.056,576.486,575.915,575.345,
                        574.773,574.202,573.63,573.057,572.484,571.91,571.336,570.761,570.186,569.61])
    Ya = np.zeros(50)
    Tg = ps.TG(yasat,calorLa,tw)
    

    x1, x2 = tw, Tg
    y1, y2 = yasat*1000, Ya

    lineas3 = ax1.plot([x1, x2], [y1, y2], 'white',linestyle= "-", visible = lineas3_visible)
   

    plt.xlim(-1,50.5)
    ax1.set_xlabel("Temperatura (°C)")
    ax1.set_ylabel("Razón de humedad (g/kg)")
    ax1.set_title("Carta Psicrométrica")
    ax1.legend(loc='upper left')
    ax1.grid(True)
     

    return fig, lineas1, lineas2, lineas3, lineas4 

def graficas(df):
    df['FECHA'] = df['MO'].apply(lambda x: calendar.month_name[x])
    
    plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico según tus necesidades
    plt.plot(df['FECHA'], df['T2M'], label='Temperatura diaria', marker='o', linestyle='-', color='b')
    plt.title('Temperatura diaria')
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Gráfico de dispersión
    plt.figure(figsize=(10, 6))
    plt.scatter(df['FECHA'], df['T2M'], label='Temperatura diaria', color='r')
    plt.title('Temperatura diaria')
    plt.xlabel('Fecha')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.grid(True)
    plt.show()

def histograma(df):
    df['FECHA'] = df['MO'].apply(lambda x: calendar.month_name[x])

# Gráfico de climograma
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Temperatura en el eje y izquierdo
    color = 'tab:blue'
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Temperatura (°C)', color=color)
    ax1.plot(df['FECHA'], df['T2M'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Crea un segundo eje y para la radiación en el eje derecho
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Radiación (W/m^2)', color=color)
    ax2.plot(df['FECHA'], df['CLRSKY_SFC_PAR_TOT'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Ajusta el diseño del gráfico
    fig.tight_layout()
    plt.title('Climograma: Temperatura y Radiación')
    plt.show()