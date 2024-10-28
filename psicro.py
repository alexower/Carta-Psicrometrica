import math 
import numpy as np

t1  =  {
    # Para -100<T<0
    "A1": -5.6745359e3,
    "A2":  6.3925247e0,
    "A3": -9.677843e-3,
    "A4":  0.6221570e-6,
    'A5':  2.0747925e-9,
    'A6': -0.94844024e-12,
    'A7':  4.1635019e0
}
t2  =  {
    # Para 0<T<100
    "A1": -5.8002206e3,
    "A2":  1.3914993e0,
    "A3": -48.640239e-3,
    "A4":  41.764768e-6,
    'A5': -14.452093e-9,
    'A6':  0.0,
    'A7':  6.5459673e0
}

def Grados_Kelvin(matriz_de_tem):
    return matriz_de_tem + 273.15

def PresionVapor(humeda_R, Psv):
    return humeda_R * Psv

def PresionVaporSaturada(tem):
    # Inicializar un array para almacenar los resultados
    psv = np.zeros_like(tem, dtype=float)
    
    # Calcular los resultados para temperaturas entre 0 y 70 grados Celsius
    valido1 = (tem > 273.15) & (tem < 373.15)
    psv[valido1] = (t2["A1"] / tem[valido1]) + t2["A2"] + t2["A3"] * tem[valido1] + t2["A4"] * np.power(tem[valido1], 2) + t2["A5"] * np.power(tem[valido1], 3) + t2["A6"] * np.power(tem[valido1], 4) + t2["A7"] * np.log(tem[valido1])
    psv[valido1] = np.exp(psv[valido1])  # resultado en pascales 
    
    # Calcular los resultados para temperaturas entre -60 y 0 grados Celsius
    valido2 = (tem >= 213) & (tem < 273.15)
    psv[valido2] = (t1["A1"] / tem[valido2]) + t1["A2"] + t1["A3"] * tem[valido2] + t1["A4"] * np.power(tem[valido2], 2) + t1["A5"] * np.power(tem[valido2], 3) + t1["A6"] * np.power(tem[valido2], 4) + t1["A7"] * np.log(tem[valido2])
    psv[valido2] = np.exp(psv[valido2])  # resultado en pascales
    
    # Asignar None a los valores fuera de los rangos especificados
    psv[~(valido1 | valido2)] = None
    return psv

def razonDehumedad(pv, pvs, p_atm):
    w = (0.622)* pv/(p_atm - pv)
    ws = (0.622)* pvs/(p_atm - pvs)
    return w, ws

def razonDehumedadSaturada(pvs, p_atm):
    ws = (0.622)* pvs/(p_atm - pvs)
    return ws

#formula para graficar Tbh
def TG(yasat,calorLa,tw):
    Tg = ((yasat*calorLa)/0.227) + tw
    return Tg

def humedad_especifica(temp, hr):
    temp = temp + 273.15
    psv = PresionVaporSaturada(temp)
    w = (0.622)* PresionVapor(hr,psv)/(presion_atm(0) - PresionVapor(hr,psv))
    return w  

def presion_atm(altura):
    p_atm = 101.325*(math.pow((1-2.25577e-5*altura),5.2559))
    p_atm = p_atm*1000 # resultado en pascales 
    return p_atm

def GradoSaturacion(w, ws):
    u = w/ws
    return u * 100

def PuntoDeRocio(temp, pv):
    # Inicializar un array para los resultados con None
    tpr = np.full_like(temp, None, dtype=float)
    
    # Calcular el punto de rocío para temperaturas entre 0 y 70 grados Celsius
    valid_temp1 = (temp > 0) & (temp < 70)
    tpr[valid_temp1] = -35.957 - 1.8726 * np.vectorize(math.log)(pv[valid_temp1]) + 1.1689 * (np.vectorize(math.log)(pv[valid_temp1]) ** 2)
    
    # Verificar que hay al menos un elemento válido para temperaturas entre -60 y 0 grados Celsius
    if np.any(temp >= -60) and np.any(temp < 0):
        # Calcular el punto de rocío para temperaturas entre -60 y 0 grados Celsius
        valid_temp2 = (temp >= -60) & (temp < 0)
        tpr[valid_temp2] = -60.450 + 7.0322 * np.vectorize(math.log)(pv[valid_temp2]) + 0.3700 * (np.vectorize(math.log)(pv[valid_temp2]) ** 2)
    
    return tpr


def eltalpia(tbs,w):
    h =  1.006*tbs + w*(2501 + 1.805*tbs) # centigrados
    return h

def TBS(Ve,Ra,w,patm):
    Tbs = ((patm * Ve) / (Ra * (1 + 1.6078 * w))) - 273.15
    return Tbs

def volumen_Espesifico(Ra, Tbs_k, w, patm):
    Ve = ((Ra*Tbs_k)/patm)*(1+1.6078* w)
    return Ve

def volumen_Espesifico_aireHumedo(Ra, Tbs_K, w, patm):
    Veh = ((Ra*Tbs_K)/patm)*(1+1.6078* w)/(1+w)
    return Veh

def bulbo_humedo(p_atm, tbs, w, iter=20):
  
    Tpr = tbs - 1
    x0 = Tpr
    tolerancia = 0.00001
    i = 0
    resultado = np.empty_like(x0,dtype=float)

    while i < iter:
        X = x0 + 273.15

        Pvsa = np.where(tbs > 0, PresionVaporSaturada(X), PresionVaporSaturada(X))

        h_x = np.where(tbs > 0, Pvsa * (-(-5.8002206e+3 / X ** 2) + (-48.640239e-3)
                                        + (2 * 41.764768e-6 * X) + (3 * -14.452093e-9 * X ** 2)
                                        + (6.5459673 / X)),
                      Pvsa * (-(-5.6745359e+3 / X ** 2) + (-9.677843e-3)
                              + (2 * 0.6221570e-6 * X) + (3 * 2.0747825e-9 * X ** 2)
                              + (4 * -0.94844024e-12 * X ** 3) + (4.1635019 / X)))

        wsa = 0.62198 * (Pvsa / (p_atm - Pvsa))

        g_x = 0.62198 * ((p_atm * h_x) / ((p_atm - Pvsa) ** 2))

        fx = (((2501 - 2.381 * x0) * wsa - 1.006 * (tbs - x0)) / (2501 + 1.805 * 20 - 4.186 * x0)) - w

        f_x = ((((2501 - 2.381 * x0) * g_x + wsa * (-2.381) + 1.006)
                / ((2501 + 1.805 * tbs) - 4.186 * x0))
               - ((((2501 - 2.381 * x0) * wsa + 1.006 + (-1.006 * tbs)) * (-4.186)) /
                  ((2501 + 1.805 * tbs) - 4.186 * x0) ** 2))

        X1 = x0 - (fx / f_x)

        error = (X1 - x0) / x0


        print(f" Numero de iteracion: ", i)
        print(f'aproximacion: ', X1)
      
        
        i = i + 1

        x0 = X1

        if np.all(np.abs(error) < tolerancia):
            break

    resultado[:] = X1
    return resultado
