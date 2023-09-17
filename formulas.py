import math 
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

def Grados_Kelvin(grados):
    kelvin  = grados + 273.15
    return kelvin

def PresionVapor(humeda_R, Psv):
    Pv = humeda_R * Psv
    return Pv

def PresionVaporSaturada(tem):
    if  tem > 273.15 and tem < 373.15:
        psv1 =(t2["A1"]/tem) + t2["A2"] + t2["A3"]*tem + t2["A4"]*math.pow(tem,2) + t2["A5"]*math.pow(tem,3) + t2["A6"]*math.pow(tem,4) + t2["A7"]*math.log(tem)
        psv1 = math.exp(psv1) # resultado en pascales 
        return psv1
    elif tem < 273 and tem > 213:
        psv2 =(t1["A1"]/tem) + t1["A2"] + t1["A3"]*tem + t1["A4"]*math.pow(tem,2) + t1["A5"]*math.pow(tem,3) + t1["A6"]*math.pow(tem,4) + t1["A7"]*math.log(tem)
        psv2 = math.exp(psv2) # resultado en pascales 
        return psv2
    else:
        return None

def razonDehumedad(pv, pvs, p_atm):
    w = (0.622)* pv/(p_atm - pv)
    ws = (0.622)* pvs/(p_atm - pvs)
    return w, ws

def presion_atm(altura):
    p_atm = 101.325*(math.pow((1-2.25577e-5*altura),5.2559))
    p_atm = p_atm*1000 # resultado en pascales 
    return p_atm 

def GradoSaturacion(w, ws):
    u = w/ws
    return u * 100

def PuntoDeRocio(temp, pv):
    if  temp > 0 and temp < 70:
        tpr = -35.957 - 1.8726 * math.log(pv) + 1.1689*(math.log(pv)**2)
        return tpr
    elif temp >= -60 and temp < 0:
        tpr2 = -60.450 + 7.0322 * math.log(pv) + 0.3700*math.pow(math.log(pv),2)
        return tpr2
    else :
        return None
  
def eltalpia(tbs,w):
    h =  1.006*tbs + w*(2501 + 1.805*tbs) # centigrados
    return h

def volumen_Espesifico(Ra, Tbs_k, w, patm):
    Ve = ((Ra*Tbs_k)/patm)*(1+1.6078* w)
    return Ve

def volumen_Espesifico_aireHumedo(Ra, Tbs_K, w, patm):
    Veh = ((Ra*Tbs_K)/patm)*(1+1.6078* w)/(1+w)
    return Veh

def bulbo_humedo(temperatura,humeda_relativa):
    tbh = (
        temperatura * math.atan(0.151977 * (humeda_relativa + 8.313659) ** 0.5) +
        math.atan(temperatura + humeda_relativa) - math.atan(humeda_relativa - 1.676331) +
        0.00391838 * (humeda_relativa ** 1.5) * math.atan(0.023101 * humeda_relativa) - 4.686035
    )
    return tbh

