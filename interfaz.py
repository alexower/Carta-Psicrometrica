import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import psicro as ps
import pandas as pd
import graficas as gs
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg , NavigationToolbar2Tk

def guardar_altura():
    global altura
    try:
        altura = float(altura_entry.get())
        mensaje_label.config(text="Altura registrada")
    except ValueError:
        tk.messagebox.showerror("Error", "Ingrese una altura válida (número).")

def calcular_psicrometricas(data_frame):
    tbs = data_frame['T2M'].values
    humeda_relativa = data_frame['RH2M'].values
   
    alturaM  = altura  
    # Calcula las propiedades psicrométricas
    tbs_kelvin = ps.Grados_Kelvin(tbs)

    p_atm = ps.presion_atm(alturaM)
    pvs = ps.PresionVaporSaturada(tbs_kelvin)
    pv = ps.PresionVapor(humeda_relativa / 100, pvs)
    w, ws = ps.razonDehumedad(pv, pvs, p_atm)
    u = ps.GradoSaturacion(w, ws)
    Veh = ps.volumen_Espesifico_aireHumedo(287.055, tbs_kelvin, w, p_atm)
    tpr = ps.PuntoDeRocio(tbs, pv)
    h = ps.eltalpia(tbs, w)
    tbh = ps.bulbo_humedo(p_atm, tbs, w)
    
    # Agrega las propiedades calculadas al DataFrame
    data_frame['W (kg va / kg as)'] = w
    data_frame['Ws (kg va / kg as)'] = ws
    data_frame['Pvs (Pa)'] = pvs
    data_frame['Pv (Pa)'] = pv
    data_frame['u (%)'] = u
    data_frame['Veh (m3/kg)'] = Veh
    data_frame['Tpr (°C)'] = tpr
    data_frame['h(KJ/kg)'] = h
    data_frame['tbh (°C)'] = tbh
 
    return data_frame
# Función para cargar archivo de datos
def cargar_archivo():
    global df_calculado
    global new2df
    global new3df
    archivo_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo_path:
        df = pd.read_csv(archivo_path, header=13)
        newdf = df[['T2M','RH2M']].copy()
        new2df = df[['MO','T2M']].copy()
        new3df = df[['MO','CLRSKY_SFC_PAR_TOT','T2M']].copy()
        df_calculado = calcular_psicrometricas(newdf)
        
        mostrar_tabla(df_calculado)

def mostrar_tabla(data_frame):
    tabla.delete(*tabla.get_children())  # Limpiar la tabla
    for index, row in data_frame.iterrows():
        tabla.insert('', 'end', values=row.tolist()) 

def generar_grafica():
    global linea1_visible, linea2_visible, linea3_visible, linea4_visible
    global lineas1, lineas2, lineas3, lineas4

    #visibilidad de graficas 
    linea1_visible = tk.BooleanVar()
    linea2_visible = tk.BooleanVar()
    linea3_visible = tk.BooleanVar()
    linea4_visible = tk.BooleanVar()
    linea1_visible.set(True)  # Línea 1 visible por defecto
    linea2_visible.set(True) # Línea 2 visible por defecto
    linea3_visible.set(True)  # Línea 3 visible por defecto
    linea4_visible.set(True) # Línea 4 visible por defecto


    gs.graficas(new2df)
    gs.histograma(new3df)

    hr_c = np.arange(0.0000000000001, 101, 10)
    temp_r = np.arange(0.0000000000001, 51, 2)
    figura, lineas1, lineas2, lineas3, lineas4 =gs.graficar_carta_psicrometrica(temp_r, hr_c, df_calculado,altura,linea1_visible,linea2_visible, linea3_visible, linea4_visible)
    canvas = FigureCanvasTkAgg(figura, master=marco_graficas)
  
    
    # Crear un nuevo frame contenedor para los botones, el lienzo y la barra de herramientas
    frame_botones = tk.Frame(marco_graficas)
    frame_botones.grid(row=0, column=1, sticky="nsew")
    #crear botones para los activacion de linas 
    chk_linea1 = tk.Checkbutton(frame_botones, text='Lineas W', variable=linea1_visible, command=lambda: actualizar_visibilidad(canvas))
    chk_linea1.grid(row=0, column=0, sticky='nsew')
    chk_linea2 = tk.Checkbutton(frame_botones, text='Líneas TBS', variable=linea2_visible, command=lambda: actualizar_visibilidad(canvas))
    chk_linea2.grid(row=1, column=0, sticky='nsew')
    chk_linea3 = tk.Checkbutton(frame_botones, text='Líneas TBH', variable=linea3_visible, command=lambda: actualizar_visibilidad(canvas))
    chk_linea3.grid(row=2, column=0, sticky='nsew')
    chk_linea4 = tk.Checkbutton(frame_botones, text='Líneas HR', variable=linea4_visible, command=lambda: actualizar_visibilidad(canvas))
    chk_linea4.grid(row=3, column=0, sticky='nsew')
   

    # Crear un nuevo frame contenedor para el lienzo y la barra de herramientas
    frame_contenedor = tk.Frame(marco_graficas)
    frame_contenedor.grid(row=1, column=0, sticky="nsew")

    # Agregar el lienzo al frame contenedor
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    canvas.draw()

    # Agregar la barra de herramientas al frame contenedor
    toolbar_grafica = NavigationToolbar2Tk(canvas, frame_contenedor)
    toolbar_grafica.update()
    toolbar_grafica.grid(row=1, column=0, sticky="ew")
    
def actualizar_visibilidad(canvas):
    # Obtener el valor de visibilidad de las variables de control
    visibilidad_linea1 = linea1_visible.get()
    visibilidad_linea2 = linea2_visible.get()
    visibilidad_linea3 = linea3_visible.get()
    visibilidad_linea4 = linea4_visible.get()
    # Actualizar la visibilidad de las líneas en la gráfica
    lineas1.set_visible(visibilidad_linea1)
    lineas2.set_visible(visibilidad_linea2)

    for linea in lineas3:
        linea.set_visible(visibilidad_linea3)
    
    for linea in lineas4:
        linea.set_visible(visibilidad_linea4)
    
    # Redibujar la gráfica
    canvas.draw()
  

def guardar_resultados():
    global df_calculado
    if df_calculado is None:
        messagebox.showerror("Error", "No hay resultados para guardar.")
        return
    
    # Abre un cuadro de diálogo para elegir la ubicación y nombre del archivo
    archivo_guardar = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
    
    if archivo_guardar:
        try:
            df_calculado.to_csv(archivo_guardar, index=False)
            mensaje_label.config(text=f"Guardado en {archivo_guardar}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
  

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora Psicrométrica")
ventana.configure(bg='gray')

# Crear una tira de color azul en la parte superior
header_frame = tk.Frame(ventana, bg="blue", height=40)
header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

# Label para introducir la altura
label_titulo = tk.Label(header_frame, text="CARTA PSICROMETRICA", fg="white", bg="blue")
label_titulo.grid(row=0, column=0, padx=10, pady=5)

# Crear un Notebook (pestañas)
pestañas = ttk.Notebook(ventana)
pestañas.grid(row=1, column=0, columnspan=4, sticky="nsew")

# Crear un marco para las pestañas "Gráficas"
marco_graficas = ttk.Frame(pestañas)
marco_graficas.grid(row=0, column=0, sticky="nsew")

# Crear un marco para las pestañas "Cálculos"
marco_calculos = ttk.Frame(pestañas)
marco_calculos.grid(row=0, column=1, sticky="nsew")


# Agregar los marcos como pestañas al Notebook
pestañas.add(marco_calculos, text="Cálculos")
pestañas.add(marco_graficas, text="Gráfica")

boton_grafica = tk.Button(marco_graficas, text="graficar", command=generar_grafica)
boton_grafica.grid(row=0, column=0, padx=10, pady=5)

frame_button = ttk.Frame(marco_calculos)
frame_button.grid(row=0, column=0, sticky="nsew")

label_altura = tk.Label(frame_button, text="Altura:", fg="white", bg="blue")
label_altura.grid(row=0, column=0, padx=10, pady=5)
# Campo de entrada para la altura
altura_entry = tk.Entry(frame_button)
altura_entry.grid(row=0, column=1, padx=5, pady=5)

# Botón para guardar la altura
boton_guardar_altura = tk.Button(frame_button, text="Guardar Altura", command=guardar_altura)
boton_guardar_altura.grid(row=0, column=2, padx=10, pady=5)
# Botón para cargar archivo de datos (en la pestaña "Cálculos")
boton_cargar_calculos = tk.Button(frame_button, text="Cargar Archivo y calcular", command=cargar_archivo)
boton_cargar_calculos.grid(row=0, column=3, padx=10, pady=10)

# Botón para guardar resultados (en la pestaña "Cálculos")
boton_guardar_calculos = tk.Button(frame_button, text="Guardar Resultados", command=guardar_resultados)
boton_guardar_calculos.grid(row=0, column=4, padx=10, pady=10)

# Etiqueta para mostrar mensajes (en la pestaña "Cálculos")
mensaje_label = tk.Label(frame_button, text="", fg="green")
mensaje_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Agregar una tabla en la pestaña "Gráficas" (usando el widget Treeview de ttk)
columns = ['Tbs (°C)', 'Hr (%)', 'W (kg va / kg as)', 'Ws (kg va / kg as)', 'Pvs (Pa)', 'Pv (Pa)', 'u (%)',
           'Veh (m3/kg )', 'Tpr (°C)', 'h(KJ/kg)', 'tbh (°C)']
tabla = ttk.Treeview(marco_calculos, columns=columns, show='headings')
for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)
tabla.grid(row=3, column=0, sticky="nsew")

# Agregar una barra de desplazamiento vertical a la tabla (en la pestaña "Gráficas")
scrollbar = ttk.Scrollbar(marco_calculos, orient="vertical", command=tabla.yview)
scrollbar.grid(row=3, column=1, sticky="ns")
tabla.configure(yscrollcommand=scrollbar.set)

# Configurar el grid para que se expanda correctamente en ambas pestañas
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)

ventana.mainloop()
