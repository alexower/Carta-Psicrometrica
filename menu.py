import formulas as fo
import os 
def main():
    os.system("cls")
    tbs = float(input('Introduzca la temperatura de bulbo seco en centrigrados (°C) ==> '))
    humeda_relativa = float(input('Introduzca el porcentaje de humedad relativa (%) ==>  ' ))
    h_r = humeda_relativa / 100
    altura = 0
    Ra = 287.055
    
    tbs_kelvin = fo.Grados_Kelvin(tbs)
    p_atm = fo.presion_atm(altura)
    pvs = fo.PresionVaporSaturada(tbs_kelvin)
    pv = fo.PresionVapor(h_r,pvs)
    w , ws = fo.razonDehumedad(pv,pvs,p_atm)
    u = fo.GradoSaturacion(w,ws)
    Ve = fo.volumen_Espesifico(Ra,tbs_kelvin,w,p_atm)
    Veh = fo.volumen_Espesifico_aireHumedo(Ra,tbs_kelvin,w,p_atm)
    tpr = fo.PuntoDeRocio(tbs,pv)
    h = fo.eltalpia(tbs,w)
    tbh = fo.bulbo_humedo(tbs,humeda_relativa)

    print('\n ------------------Propiedades Psicrometricas-----------------------\n')
    print(f'1) La razon de humedad (W) es: {w} kg va / kg as \n')
    print(f'2) La razon de humedad saturada (Ws) es: {ws} kg va / kg as \n')
    print(f'3) La presion parcial de vapor de agua (pv) es: {pv} Pa\n')
    print(f'4) La presion parcial de vapor saturada (pvs) es: {pvs} Pa \n')
    print(f'5) El grado de saturacion (u) es: {u} % \n')
    print(f'6) El volumen especifico de aire humedo (Veh) es: {Veh} m3/kg \n')
    print(f'7) La temperatura del punto de rocio (Tpr) es: {tpr} °C\n')
    print(f'8) La temperatura del bulbo humedo (Tbh) es: {tbh} °C \n')
    print(f'9) La eltalpia (h) es: {h} KJ/kg')
          
if __name__ == '__main__':
    main()
    

   


