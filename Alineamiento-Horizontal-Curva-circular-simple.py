import math

def ejecutar() :
    ingresar_datos()
    hallar_elementos_geométricos_de_la_curva()
    coordenadas_replanteo_de_la_curva()
    progresion_del_peralte()

def ingresar_datos() :
    global tipo
    global F_maxima
    global radio_adoptado
    global azimut_entrada
    global azimut_salida
    global velocidad_de_diseño
    global PI_coordenadas
    global bombeo
    PI_coordenadas={'Este':0,'Norte':0}
    global progresiva_PI
    global avance_en_progresivas_dentro_de_la_curva
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
    avance_en_progresivas_dentro_de_la_curva=float(input('Avance en progresivas dentro de la curva en [m]='))

def hallar_elementos_geométricos_de_la_curva() :
    global angulo_de_deflexion
    global tangente
    global cuerda_larga
    global externa
    global media
    global longitud_de_curva
    global grado_de_curvatura_por_metro
    global deflexion_por_metro
    global progresiva_PC
    global progresiva_PT
    global PC_principio_de_curva_coordenadas 
    PC_principio_de_curva_coordenadas={'Este':0,'Norte':0}
    global PT_final_de_curva_coordenadas 
    PT_final_de_curva_coordenadas={'Este':0,'Norte':0}
    global centro_de_la_curva_coordenadas 
    centro_de_la_curva_coordenadas={'Este':0,'Norte':0}
    global azimut_PC_a_centro_de_la_curva 
    azimut_PC_a_centro_de_la_curva={'Este':0,'Norte':0}
    global  azimut_centro_de_la_curva_a_PC

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
    # angulo de deflección siempre mide el angulo que existe entre la dirección de entrada y la dirección de salida

    tangente=radio_adoptado*math.tan(abs(angulo_de_deflexion)/2)
    cuerda_larga=2*radio_adoptado*math.sin(abs(angulo_de_deflexion)/2)
    externa=radio_adoptado*(1/(math.cos(abs(angulo_de_deflexion)/2))-1)
    media=radio_adoptado*(1-math.cos(abs(angulo_de_deflexion)/2))
    longitud_de_curva=radio_adoptado*abs(angulo_de_deflexion)
    grado_de_curvatura_por_metro=1*abs(angulo_de_deflexion)/longitud_de_curva
    deflexion_por_metro=grado_de_curvatura_por_metro/2
    progresiva_PC=progresiva_PI-tangente
    progresiva_PT=progresiva_PC+longitud_de_curva
    PC_principio_de_curva_coordenadas['Este']=hallar_este(PI_coordenadas['Este'],invertir_azimut(azimut_entrada),tangente)
    PC_principio_de_curva_coordenadas['Norte']=hallar_norte(PI_coordenadas['Norte'],invertir_azimut(azimut_entrada),tangente)
    PT_final_de_curva_coordenadas['Este']=hallar_este(PI_coordenadas['Este'],azimut_entrada,tangente)
    PT_final_de_curva_coordenadas['Norte']=hallar_norte(PI_coordenadas['Norte'],azimut_entrada,tangente)
    
    if angulo_de_deflexion_caso_especial:
        if angulo_de_deflexion_positivo:
            azimut_PC_a_centro_de_la_curva = azimut_entrada - math.pi*3/2
        else:
            azimut_PC_a_centro_de_la_curva = azimut_entrada + math.pi*3/2
    else :
        if angulo_de_deflexion_positivo:
            azimut_PC_a_centro_de_la_curva = azimut_entrada + math.pi/2
        else:
            azimut_PC_a_centro_de_la_curva = azimut_entrada - math.pi/2

    centro_de_la_curva_coordenadas['Este']=hallar_este(PC_principio_de_curva_coordenadas['Este'],azimut_PC_a_centro_de_la_curva,radio_adoptado)
    centro_de_la_curva_coordenadas['Norte']=hallar_norte(PC_principio_de_curva_coordenadas['Norte'],azimut_PC_a_centro_de_la_curva,radio_adoptado)
    azimut_centro_de_la_curva_a_PC=invertir_azimut(azimut_PC_a_centro_de_la_curva)
    
    print(f'angulo de deFlexión de rectas [radianes]={angulo_de_deflexion}')
    print(f'tangente[m]={tangente}')
    print(f'Cuerda larga[m]={cuerda_larga}')
    print(f'Externa [m]={externa}')
    print(f'Media [m]={media}')
    print(f'Longitud de curva[m]={longitud_de_curva}')
    print(f'grado de curvatura por metro [radianes]={grado_de_curvatura_por_metro}')
    print(f'deflexion por metro [radianes]={deflexion_por_metro}')
    print(f'Progresiva PC[m]={progresiva_PC}')
    print(f'Progresiva PT[m]={progresiva_PT}')
    print(f'Coordenaras Principio de curva PC UTM:' + str(PC_principio_de_curva_coordenadas['Este']) + ',' + str(PC_principio_de_curva_coordenadas['Norte']))
    print(f'Coordenadas Final de Curva PT UTM:' + str(PT_final_de_curva_coordenadas['Este']) + ',' + str(PT_final_de_curva_coordenadas['Norte']))
    print(f'Coordenadas centro de la Curva UTM:' + str(centro_de_la_curva_coordenadas['Este']) + ',' + str(centro_de_la_curva_coordenadas['Norte']))
    print(f'Azimut del cetro de la curva a PC: {azimut_centro_de_la_curva_a_PC}')


def coordenadas_replanteo_de_la_curva() :
    este=[0]
    norte=[0]
    contador=0
    progresiva_replanteo=int(math.ceil(progresiva_PC))

    ang_deflexion_replanteo=0
    este[contador]=PC_principio_de_curva_coordenadas['Este']
    norte[contador]=PC_principio_de_curva_coordenadas['Norte']
    print('-----*-----INICIO DE REPLANTEO DE LA CURVA CIRCULAR SIMPLE-----*-----')
    print(f'progresiva[m]: {progresiva_PC} ')
    print(f'Ángulo de deflexión: {ang_deflexion_replanteo}')
    print(f'Ángulo de doble deflexión: {2*ang_deflexion_replanteo}')
    print('Coordenadas E:' + str(este[contador]) + ',   N:' + str(norte[contador]))
    
    progresiva_replanteo=int(math.ceil(progresiva_PC))
    while (progresiva_replanteo%avance_en_progresivas_dentro_de_la_curva)!=0 :
        progresiva_replanteo += 1

    while progresiva_replanteo<progresiva_PT :
        contador+=1
        ang_deflexion_replanteo+=avance_en_progresivas_dentro_de_la_curva*deflexion_por_metro
        este.append(hallar_este_replanteo(2*ang_deflexion_replanteo))
        norte.append(hallar_norte_replanteo(2*ang_deflexion_replanteo))
        print('--- --- ---- --- ---')
        print(f'progresiva[m]: {progresiva_replanteo} ')
        print(f'Ángulo de deflexión {ang_deflexion_replanteo}')
        print(f'Ángulo de doble deflexión: {2*ang_deflexion_replanteo}')
        print('Coordenadas E:' + str(este[contador]) + ',   N:' + str(norte[contador]))
        progresiva_replanteo+=avance_en_progresivas_dentro_de_la_curva
    
    contador+=1
    progresiva_replanteo-=avance_en_progresivas_dentro_de_la_curva
    ang_deflexion_replanteo+=(progresiva_PT-progresiva_replanteo)*deflexion_por_metro
    este.append(hallar_este_replanteo(2*ang_deflexion_replanteo))
    norte.append(hallar_norte_replanteo(2*ang_deflexion_replanteo))
    print('--- --- ---- --- ---')
    print(f'progresiva[m]: {progresiva_PT} ')
    print(f'Ángulo de deflexión {ang_deflexion_replanteo}')
    print(f'Ángulo de doble deflexión: {2*ang_deflexion_replanteo}')
    print('Coordenadas E:' + str(este[contador]) + ',   N:' + str(norte[contador]))


def progresion_del_peralte() :
    # PERALTE
    if tipo=='carretera':
        if radio_adoptado<=700:
            peralte=8/100
        elif radio_adoptado<=5000:
            peralte=(8-7.3*(1-700/radio_adoptado)**(1.3))/100
        elif radio_adoptado<=7500:
            peralte=2/100
        else  :
            peralte=bombeo
    elif tipo=='camino':
        if radio_adoptado<=350:
            peralte=7/100
        elif radio_adoptado<=2500:
            peralte=(7-6.08*(1-350/radio_adoptado)**(1.3))/100
        elif radio_adoptado<=3500:
            peralte=2/100
        else :
            peralte=bombeo
    # PENDIENTE RELATIVA DE BORDE
    pendiente_relativa_de_borde=elegir_tipo_pendiente_relativa_de_borde()
    #CANTIDAD DE CARRILES
    n_cantidad_de_carriles=elegir_n_cantidad_de_carriles()
    print(f'Peralte [tanto por 1]= {peralte}')
    print(f'Pendiente relativa de borde= {pendiente_relativa_de_borde}')
    # CALCULO DE VALORES
    a=float(input("a[m]="))
    Lt=n_cantidad_de_carriles*a*peralte*100/pendiente_relativa_de_borde
    N=Lt*(bombeo/peralte)
    B=a*bombeo
    E=a*peralte
    print(f'Lt[m]={Lt}')
    print(f'N[m]={N}')
    print(f'B[m]={B}')
    print(f'E[m]={E}')
    progresiva_A=progresiva_PC-0.7*Lt-N
    progresiva_B=progresiva_PC-0.7*Lt
    progresiva_C=progresiva_PC-0.7*Lt+N
    progresiva_D=progresiva_PC+0.3*Lt
    progresiva_E=progresiva_PT-0.3*Lt
    progresiva_F=progresiva_PT+0.7*Lt-N
    progresiva_G=progresiva_PT+0.7*Lt
    progresiva_H=progresiva_PT+0.7*Lt+N
    print('----- ----- -----')
    print(f'Progresiva A[m]: {progresiva_A}')
    print(f'Progresiva B[m]: {progresiva_B}')
    print(f'Progresiva C[m]: {progresiva_C}')
    print(f'Progresiva D[m]: {progresiva_D}')
    print(f'Progresiva E[m]: {progresiva_E}')
    print(f'Progresiva F[m]: {progresiva_F}')
    print(f'Progresiva G[m]: {progresiva_G}')
    print(f'Progresiva H[m]: {progresiva_H}')


def invertir_azimut(azimut):
    azimut_invertido=azimut+math.pi
    if azimut_invertido>(2*math.pi):
        azimut_invertido -= 2*math.pi
    return azimut_invertido

def hallar_este(este,azimut,distancia_entre_puntos) :
    este=este+distancia_entre_puntos*math.sin(azimut)
    return este

def hallar_norte(norte,azimut,distancia_entre_puntos) :
    norte=norte+distancia_entre_puntos*math.cos(azimut)
    return norte

def hallar_este_replanteo(ang_dob_def):
    este=centro_de_la_curva_coordenadas['Este']+radio_adoptado*(math.sin(azimut_centro_de_la_curva_a_PC+ang_dob_def))
    return este

def hallar_norte_replanteo(ang_dob_def):
    norte=centro_de_la_curva_coordenadas['Norte']+radio_adoptado*(math.cos(azimut_centro_de_la_curva_a_PC+ang_dob_def))
    return norte

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


def radianes_a_grados_minutos_segundos(radianes):
    grados=math.floor(radianes*182/math.pi)

if __name__ == "__main__":
    ejecutar()