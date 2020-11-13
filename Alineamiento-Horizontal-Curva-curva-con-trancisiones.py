import math


def ejecutar() :
    ingresar_datos()
    hallar_elementos_geométricos_de_la_curva()

def ingresar_datos() :
    global tipo
    global F_maxima
    global radio_minimo
    global radio_adoptado
    global azimut_entrada
    global azimut_salida
    global velocidad_de_diseño
    global PI_coordenadas
    global bombeo
    PI_coordenadas={'Este':0,'Norte':0}
    global progresiva_PI
    global peralte_adoptado
    global n_cantidad_de_carriles
    global a_ancho_de_carril
    global pendiente_relativa_de_borde
    tipo=elegir_tipo()
    velocidad_de_diseño=float(input('Velocidad de diseñ= [km/h]= '))
    if tipo=='carretera':
        F_maxima=0.193-velocidad_de_diseño/1134
        peralte_maximo=8/100
    elif tipo=='camino':
        F_maxima=0.265-velocidad_de_diseño/602.4
        peralte_maximo=7/100
    radio_minimo=velocidad_de_diseño**2/127*(1/(peralte_maximo+F_maxima))
    print(f'Radio mínimo: {radio_minimo}')
    radio_adoptado=float(input('Radio adoptado de la curva[m]= '))
    azimut_entrada=float(input('Azimut de entrada [radianes](si solo tienes de dato el delta entre ambas rectas, pon aquí ese delta)= '))
    azimut_salida=float(input('Azimut de salida [radianes](si solo tienes de dato el delta entre ambas rectas, pon aquí cero)= '))
    PI_coordenadas['Este']=float(input('PI coordenadas Norte UTM: '))
    PI_coordenadas['Norte']=float(input('PI coordenadas Este UTM: '))
    progresiva_PI=float(input('progresiva del PI [m] = '))
    bombeo=float(input('bombeo [tanto por 1] = '))
    print(f'Peralte máximo[tanto por 1]= {peralte_maximo}')    
    # PERALTE
    if tipo=='carretera':
        if radio_adoptado<=700:
            peralte_adoptado=8/100
        elif radio_adoptado<=5000:
            peralte_adoptado=(8-7.3*(1-700/radio_adoptado)**(1.3))/100
        elif radio_adoptado<=7500:
            peralte_adoptado=2/100
        else  :
            peralte_adoptado=bombeo
    elif tipo=='camino':
        if radio_adoptado<=350:
            peralte_adoptado=7/100
        elif radio_adoptado<=2500:
            peralte_adoptado=(7-6.08*(1-350/radio_adoptado)**(1.3))/100
        elif radio_adoptado<=3500:
            peralte_adoptado=2/100
        else :
            peralte_adoptado=bombeo
    print(f'Peralte adoptado[tanto por 1]= {peralte_adoptado}')

    # pendiente relativa de borde
    pendiente_relativa_de_borde=elegir_tipo_pendiente_relativa_de_borde()
    print(f'pendiente relativa de borde = {pendiente_relativa_de_borde}')
    pendiente_relativa_de_borde= cambiar_dato(pendiente_relativa_de_borde)
    print(f'pendiente relativa de borde = {pendiente_relativa_de_borde}')
    
    #CANTIDAD DE CARRILES
    n_cantidad_de_carriles=elegir_n_cantidad_de_carriles()

    # ANCHO DE CARRILES
    a_ancho_de_carril=float(input('Ancho de Carril a[m]='))


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

def elegir_n_cantidad_de_carriles():
    eleccion=input('Cantidad de carriles n (n de ida y n de vuelta): ')
    if int(eleccion)<=0 :
        print('n debe mayor que cero')
        elegir_n_cantidad_de_carriles()
    elif ((int(eleccion)==1) or (int(eleccion)==2) or (int(eleccion)==3) or (int(eleccion)==4) or (int(eleccion)==5) or (int(eleccion)==6)):
        return int(eleccion)
    else:
        print('Debes ingresar un n válido menor a 7 :v')
        elegir_n_cantidad_de_carriles()


def hallar_elementos_geométricos_de_la_curva() :
    global angulo_de_deflexion_caso_especial
    global angulo_de_deflexion_positivo
    global angulo_de_deflexion
    global lt
    angulo_de_deflexion=azimut_salida-azimut_entrada
    if  abs(angulo_de_deflexion)>math.pi :
        angulo_de_deflexion_caso_especial=True
        if angulo_de_deflexion>0 :
            angulo_de_deflexion = angulo_de_deflexion +2*math.pi
        elif angulo_de_deflexion<0 :
            angulo_de_deflexion = angulo_de_deflexion-2*math.pi
    else :
        angulo_de_deflexion_caso_especial=False
    if angulo_de_deflexion>0:
        angulo_de_deflexion_positivo=True
    elif angulo_de_deflexion<0:
        angulo_de_deflexion_positivo=False

    # Longitud de transición == lt
    lt={}
    lt['guiado optico']=radio_adoptado/9
    lt['guiado optico adicional']=(12*radio_adoptado)**(0.5)   
    lt['maxima pendiente relativa de borde'] = n_cantidad_de_carriles*a_ancho_de_carril*peralte_adoptado*100/abs(pendiente_relativa_de_borde)
    velocidad_especifica_para_calculo_de_lt=[]
    if velocidad_de_diseño<=80 :
        velocidad_especifica_para_calculo_de_lt.append((-0.211*radio_adoptado+( ((0.211*radio_adoptado)**2-4*radio_adoptado*(-127)*(peralte_adoptado+0.265)) )**(0.5))/2)
        velocidad_especifica_para_calculo_de_lt.append((-0.211*radio_adoptado-( ((0.211*radio_adoptado)**2-4*radio_adoptado*(-127)*(peralte_adoptado+0.265)) )**(0.5))/2)
    elif velocidad_de_diseño>80:
        velocidad_especifica_para_calculo_de_lt.append((-0.112*radio_adoptado+( ((0.112*radio_adoptado)**2-4*radio_adoptado*(-127)*(peralte_adoptado+0.193)) )**(0.5))/2)
        velocidad_especifica_para_calculo_de_lt.append((-0.112*radio_adoptado-( ((0.112*radio_adoptado)**2-4*radio_adoptado*(-127)*(peralte_adoptado+0.193)) )**(0.5))/2)

    if velocidad_especifica_para_calculo_de_lt[0]>velocidad_especifica_para_calculo_de_lt[1]:
        velocidad_especifica_para_calculo_de_lt_adoptado=velocidad_especifica_para_calculo_de_lt[0]
    else:
        velocidad_especifica_para_calculo_de_lt_adoptado=velocidad_especifica_para_calculo_de_lt[1]

    if radio_adoptado<=(1.2*radio_minimo) :
        if velocidad_de_diseño <=60 :
            j_normal = 1.5
        elif velocidad_de_diseño <= 70 :
            j_normal=1.4
        elif velocidad_de_diseño<=80 :
            j_normal=1
        elif velocidad_de_diseño<=90 :
            j_normal=0.9
        elif velocidad_de_diseño<=100 :
            j_normal=0.8
        else:
            j_normal=0.4
    else:
        if velocidad_especifica_para_calculo_de_lt_adoptado<80:
            j_normal=0.5
        else:
            j_normal=0.4
    print(f'J={j_normal}')

    lt['comodidad dinamica']=velocidad_especifica_para_calculo_de_lt_adoptado/(46.656*j_normal)*(velocidad_especifica_para_calculo_de_lt_adoptado**2/radio_adoptado-1.27*peralte_adoptado)

    if (lt['guiado optico']>lt['guiado optico adicional']) and (lt['guiado optico']>lt['maxima pendiente relativa de borde']) and ((lt['guiado optico']>lt['comodidad dinamica'])):
        lt['final']=lt['guiado optico']
    elif (lt['guiado optico adicional']>lt['guiado optico']) and (lt['guiado optico adicional']>lt['maxima pendiente relativa de borde']) and ((lt['guiado optico adicional']>lt['comodidad dinamica'])):
        lt['final']=lt['guiado optico adicional']
    elif(lt['maxima pendiente relativa de borde']>lt['guiado optico']) and (lt['maxima pendiente relativa de borde']>lt['guiado optico adicional']) and (lt['maxima pendiente relativa de borde']>lt['comodidad dinamica']) :
        lt['final']=lt['maxima pendiente relativa de borde']        
    elif (lt['comodidad dinamica']>lt['guiado optico']) and (lt['comodidad dinamica']>lt['guiado optico adicional']) and ((lt['comodidad dinamica']>lt['maxima pendiente relativa de borde'])):
        lt['final']=lt['comodidad dinamica']

    print(f"""Longitud de transición por GUIADO ÓPTICO[M]: {lt['guiado optico']}[m]""")
    print(f"""Longitud de transición por GUIADO ÓPTICO ADICIONAL[M]: {lt['guiado optico adicional']}[m]""")
    print(f"""Longitud de transición por MAXIMA PENDIENTE RELATIVA DE BORDE[M]: {lt['maxima pendiente relativa de borde']}[m]""")
    print(f"""Velocidad específica 1: {velocidad_especifica_para_calculo_de_lt[0]} [km/h]""")
    print(f"""Velocidad específica 2: {velocidad_especifica_para_calculo_de_lt[1]} [km/h]""")
    print(f"""Longitud de transición por COMODIDAD DINÁMICA: {lt['comodidad dinamica']}[m]""")
    print(f"""LONGITUD DE transición final {lt['final']}[m]""")

    lt_adoptado=float(input('Esriba la longitud de transición adoptada[m] : '))

    # angulo de la clotoide == angulo_clotoide
    angulo_clotoide=1/2*lt_adoptado/radio_adoptado
    print(f'Ángulo de la clotoide {angulo_clotoide}[Rad]')

    # calculo de Xc y Yc
    Xc=lt_adoptado*(1-angulo_clotoide**2/10+angulo_clotoide**4/216-angulo_clotoide**6/9360+angulo_clotoide**8/685440)
    Yc=lt_adoptado*(angulo_clotoide/3-angulo_clotoide**3/42+angulo_clotoide**5/75600+angulo_clotoide**9/6894720)
    print(f'Xc={Xc}[m]')
    print(f'Yc={Yc}[m]')

    # disloque o retranqueo de coordenadas p y k
    k=Xc-radio_adoptado*math.sin(angulo_clotoide)
    p=Yc-radio_adoptado*(1-math.cos(angulo_clotoide))
    print(f'k={k}[m]')
    print(f'p={p}[m]')

    tangente_espiral=k+(radio_adoptado+p)*math.tan(abs(angulo_de_deflexion)/2)
    print(f'Tangente espiral Te={tangente_espiral}[m]')

    externa_espiral=(p+radio_adoptado)/(math.cos(abs(angulo_de_deflexion)/2))-radio_adoptado
    print(f'Externa espiral Ee={externa_espiral}[m]')

    tangente_corta=Yc/math.sin(angulo_clotoide)
    tangente_larga=Xc-Yc*(1/math.tan(angulo_clotoide))
    print(f'Tangente corta Tc={tangente_corta}[m]')
    print(f'Tangente larga TL={tangente_larga}[m]')

    # Longitud y ángulo de la curva osculatriz
    angulo_curva_osculatriz=abs(angulo_de_deflexion)-2*angulo_clotoide
    longitud_curva_osculatriz=radio_adoptado*angulo_curva_osculatriz
    print(f'Ángulo curva osculatriz {angulo_curva_osculatriz}[rad]')
    print(f'Longitud curva osculatriz {longitud_curva_osculatriz}[m]')

    longitud_total=2*lt_adoptado+longitud_curva_osculatriz
    print(f'Longitud total = {longitud_total}[m]')

    progresiva_TE=progresiva_PI-tangente_espiral
    progresiva_EC=progresiva_TE+lt_adoptado
    progresiva_CE=progresiva_EC+longitud_curva_osculatriz
    progresiva_ET=progresiva_CE+lt_adoptado

    print(f'Progresiva TE = {progresiva_TE}')
    print(f'Progresiva EC = {progresiva_EC}')
    print(f'Progresiva CE = {progresiva_CE}')
    print(f'Progresiva ET = {progresiva_ET}')


def elegir_tipo_pendiente_relativa_de_borde() :
    eleccion=input("""Tipo de pendiente de borde
1. Normal
2. Máxima, numero de carriles=1
3. Máxima, numero de carriles>1   
Elige una opción: """)
    if int(eleccion)==1 :
        if velocidad_de_diseño<=50 :
            return 0.7
        elif velocidad_de_diseño<=70 :
            return 0.6
        elif velocidad_de_diseño<=90 :
            return 0.5
        elif velocidad_de_diseño>90 :
            return 0.35
            if velocidad_de_diseño>120 :
                print("CUIDADO LA NORMA DE LA ABC NO ESPECIFICA UN VALOR PARA LA PENDIENTE DE BORDE SI VELOCIDAD DE DISEÑO ES MAYOR A 120 [KM/H]")
    elif int(eleccion)==2 :
        if velocidad_de_diseño<=50 :
            return 1.5
        elif velocidad_de_diseño<=70 :
            return 1.3
        elif velocidad_de_diseño<=90 :
            return 0.9
        elif velocidad_de_diseño>90 :
            return 0.8
            if velocidad_de_diseño>120 :
                print("CUIDADO LA NORMA DE LA ABC NO ESPECIFICA UN VALOR PARA LA PENDIENTE DE BORDE SI VELOCIDAD DE DISEÑO ES MAYOR A 120 [KM/H]")
    elif int(eleccion)==3 :
        if velocidad_de_diseño<=50 :
            return 1.5
        elif velocidad_de_diseño<=70 :
            return 1.3
        elif velocidad_de_diseño<=90 :
            return 0.9
        elif velocidad_de_diseño>90 :
            return 0.8
            if velocidad_de_diseño>120 :
                print("CUIDADO LA NORMA DE LA ABC NO ESPECIFICA UN VALOR PARA LA PENDIENTE DE BORDE SI VELOCIDAD DE DISEÑO ES MAYOR A 120 [KM/H]")
    else :
        print('ELIGE UNA OPCCIÓN VÁLIDA!!!')
        elegir_tipo_pendiente_relativa_de_borde()


def cambiar_dato(dato):
    eleccion=int(input(""" ¿Deseas cambiar este valor: {dato}?
1. si
2. no
elige:    """))
    if eleccion ==1 :
        dato=float(input("Nuevo valor"))
    elif eleccion==2 :
        dato=dato
    else:
        print('ELIGE UNA OPCCIÓN VÁLIDA!!!')
        cambiar_dato(dato)
    return dato

if __name__ == "__main__":
    ejecutar()