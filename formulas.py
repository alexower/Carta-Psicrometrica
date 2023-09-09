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
    "A3": -48.6403239e-3,
    "A4":  41.764768e-6,
    'A5': -14.52093e-9,
    'A6':  0.0,
    'A7':  6.5459673e0
}

def Grados_Kelvin(grados):
    kelvin  = grados + 273.15
    return kelvin

def PresionVaporSaturada(temperature):
    pass

