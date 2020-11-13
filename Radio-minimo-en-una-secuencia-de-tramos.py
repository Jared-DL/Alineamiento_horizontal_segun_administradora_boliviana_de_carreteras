def inicio():
    print("Hallaremos los radios minimos para carreteras")
    ingresar_datos()
    operar()


def ingresar_datos():
    global total_de_tramos
    global tramo
    global longitud
    global velocidad_de_proyecto
    longitud=[]
    velocidad_de_proyecto=float(input('Velocidad de proyecto Vp[km/hr]='))
    total_de_tramos=int(input('¿Cúantos tramos se tiene? : '))
    tramo = 0
    print('ingresa los datos de logitudes')
    while tramo<total_de_tramos :
        longitud.append(float(input(f'longitud{tramo} [m]= ')))
        tramo +=1


def operar():
    global velocidad_85_percentil
    tipo=elegir_tipo()
    if tipo=='carretera':
        F_maxima=0.193-velocidad_de_proyecto/1134
        peralte_maximo=8/100
    elif tipo=='camino':
        F_maxima=0.265-velocidad_de_proyecto/602.4
        peralte_maximo=7/100
    radio_minimo=velocidad_de_proyecto**2/127*(1/(peralte_maximo+F_maxima))
    print(f'Radio mínimo: {radio_minimo}')
    # IDA
    print('---*---Para la ida---*---')
    tramo=0
    while tramo<(total_de_tramos-1):
        print(f'  --Del tramo {tramo} al {tramo+1}--')
        if longitud[tramo]>400 :
            print('    Caso II')
            if longitud[tramo]>600:
                if velocidad_de_proyecto<100:
                    velocidad_85_percentil=(velocidad_de_proyecto+20)
                elif velocidad_de_proyecto<120:
                    velocidad_85_percentil=(velocidad_de_proyecto+15)
                elif velocidad_de_proyecto>=120:
                    velocidad_85_percentil=(velocidad_de_proyecto+10)
            elif longitud[tramo]<=600:
                if velocidad_de_proyecto<120:
                    velocidad_85_percentil=(velocidad_de_proyecto+10)
                elif velocidad_de_proyecto>=120:
                    velocidad_85_percentil=(velocidad_de_proyecto+5)
        elif longitud[tramo]<=400 :
            print('    Caso I')
            velocidad_85_percentil=(velocidad_de_proyecto)
        print(f'    Velocidad 85 percentil V85[km/h]={velocidad_85_percentil}')
        tramo += 1
    # VUELTA
    print('---*---Para la ida---*---')
    tramo=total_de_tramos-1
    while tramo>0:
        print(f'  --Del tramo {tramo} al {tramo-1}--')
        if longitud[tramo]>400 :
            print('    Caso II')
            if longitud[tramo]>600:
                if velocidad_de_proyecto<100:
                    velocidad_85_percentil=(velocidad_de_proyecto+20)
                elif velocidad_de_proyecto<120:
                    velocidad_85_percentil=(velocidad_de_proyecto+15)
                elif velocidad_de_proyecto>=120:
                    velocidad_85_percentil=(velocidad_de_proyecto+10)
            elif longitud[tramo]<=600:
                if velocidad_de_proyecto<120:
                    velocidad_85_percentil=(velocidad_de_proyecto+10)
                elif velocidad_de_proyecto>=120:
                    velocidad_85_percentil=(velocidad_de_proyecto+5)
        elif longitud[tramo]<=400 :
            print('    Caso I')
            velocidad_85_percentil=(velocidad_de_proyecto)
        print(f'    Velocidad 85 percentil V85[km/h]={velocidad_85_percentil}')
        tramo -= 1



def elegir_tipo() :
    eleccion=input("""Tenemos una...
1. Carretera
2. Camino(los colectores, son caminos)
Elige una opción: """)
    if int(eleccion)==1 :
        return 'carretera'
    elif int(eleccion)==2 :
        return 'camino'
    else :
        print('ELIGE UNA OPCCIÓN VÁLIDA!!!')
        elegir_tipo()

if __name__ == "__main__":
    inicio()