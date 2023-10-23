import numpy as np
import matplotlib.pyplot as plt
import psicro as ps

def graficar_carta_psicrometrica(temp_r, hr_c, data_frame):
    
    # Crear la figura y el eje
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(12, 6))

# Crear matrices de temperatura y HR
    temp_matrix, hr_matrix = np.meshgrid(temp_r, hr_c)

# Calcular la humedad específica y ajustar la escala
    w_matrix = ps.humedad_especifica(temp_matrix, hr_matrix / 100) * 1000
    
    print(w_matrix)
    # Gráfico de Tbs vs W
    ax1.plot(data_frame["Tbs"], data_frame["W (kg va / kg as)"] * 1000, marker='o', linestyle='', color='magenta', label="Datos Tbs vs W")

   # GRafico delíneas constantes de HR utilizando w_matrix
    ax1.plot(temp_r, w_matrix.T, linestyle='-', color='white', alpha=0.5)

        # Encontrar los índices donde la humedad relativa es igual a 100 en la matriz w_matrix
    
    valores_maximos = np.amax(w_matrix.T, axis=1)
    print(valores_maximos)
    print(temp_matrix)
    
    plt.vlines(temp_r, ymin=0, ymax=valores_maximos, colors='white', linestyles='dashed', label='temperaturas')

    temp_w = np.arange(0.0000000000001,51,1)
    temp_w_matrix = np.meshgrid(temp_w)
    w_matrix2 = ps.humedad_especifica(temp_w_matrix, hr_matrix / 100) * 1000
    print(w_matrix2)

    
    #plt.hlines(valores_maximos, xmin=temp_r, xmax=50, colors='r', linestyles='dashed', label='Líneas Horizontales')

    ax1.set_xlabel("Temperatura (°C)")
    ax1.set_ylabel("Razón de humedad (g/kg)")
    ax1.set_title("Carta Psicrométrica")
    ax1.legend(loc='upper left')
    ax1.grid(True)

    return fig
