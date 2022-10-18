

""" 
BORRADOR
Información de los aviones: Tiempo de llegada, velocidad a la que pueden cambiar si van muy rapido, velocidad ideal, velocidad más económica, costos por llegar
tarde, costos por llegar temprano, separación mínima entre cualquier combinación de aviones.


Llega una avión en un tiempo determinado, este avión entrega sus tiempos de aterrizaje en el aire por lo que su agendamiento ocurre acá, no con toda la información anterior.

La misión es entregarle un tiempo de llegada lo más cercano a su tiempo favorito. Una solución inicial podría ser la de "llega un avión, en un principio
no sabemos cuál y le asignamos un tiempo de aterrizaje lo más cercano a su tiempo favorito, para ello es necesario hacer cálculo de sus tiempos minimos a respetar.

""" 

"Instancia de 3 aviones"

valores = []
datos_archivo = open("./40aviones.txt","r") # Acá se instancia el set de datos

while(True):

    line = datos_archivo.readline()
    if not line:
        break
    valores.append(line.strip())
datos_archivo.close()

parametros = valores[0].split(" ")

for x in range(len(parametros)):
    parametros[x] = int(parametros[x])

temporal = []
for a in range(1,len(valores)):
    temporal.append(valores[a].split(" "))

aviones = []
temp_aviones = []
temp_costos = []
temp_tarde_temprano = []
for b in range(len(temporal)):
    c = []
    t = []
    a = []
    if(b%2 > 0):
        for i in temporal[b]:
            c.append(int(i))
    else:
        for i in range(len(temporal[b])):
            if (i >=4):
                t.append(float(temporal[b][i]))
            else:
                a.append(int(temporal[b][i]))
    if(len(c) > 0):
        temp_costos.append(c)
    if(len(t) > 0):
        temp_tarde_temprano.append(t)
    if(len(a) > 0):
        temp_aviones.append(a)


"""aviones =  [[24,129,155,559],[120,195,258,744],[14,89,100,510],[21,96,106,521],[16,110,123,555],[45,120,135,576]]#106
temprano_tarde = [[10,10],[10,10],[30,30],[30,30],[30,30],[30,30]]
costos_aviones = [[99999,3,15,15,15,15],[3,99999,15,15,15,15],[15,15,999999,8,8,8],[15,15,8,99999,8,8],[15,15,8,8,99999,8],[15,15,8,8,8,99999]]"""

aviones = temp_aviones
temprano_tarde = temp_tarde_temprano
costos_aviones = temp_costos



def Hill3(combinacion3): #Retorna una solución mínima que respeta las claúsulas. Combinación de tamaño 3
    
    a = aviones[combinacion3[0]][1]

    if(aviones[combinacion3[1]][1] > a + costos_aviones[combinacion3[1]][combinacion3[0]]):
        b = aviones[combinacion3[1]][1]
    else:
        b = a + costos_aviones[combinacion3[1]][combinacion3[0]]

    if(aviones[combinacion3[2]][1]  > b + costos_aviones[combinacion3[2]][combinacion3[1]]):
        c = aviones[combinacion3[2]][1]
    else:
        c =  b + costos_aviones[combinacion3[2]][combinacion3[1]]

    solucion = [a,b,c]
    return solucion

def Vecindario3(solucion,combinaciones): #Crea un vecindario factible, fijar límites.

    pasos = [1,0,-1]
    vecindario = []
    for i in pasos:
        for j in pasos:
            for k in pasos:
                temp = Operacion3(solucion,i,j,k)
                if(Check_all(temp,combinaciones) == True and Chequeo_intervalo(temp,combinaciones) == True):
                    vecindario.append(temp)
    if(len(vecindario) == 0): #Retorna la primera solución factible que encuentre
        return [Hill3(combinaciones)]
    return vecindario

def Operacion3(solucion,i,j,k): #Complemento del vecindario
    respuesta = [solucion[0] + i, solucion[1] + j, solucion[2] + k]
    return respuesta

def Hill_climbing_final3(Mejor_candidato,combinacion,Mejor): #Mejor vecindario(valor inicial), aviones con los que está trabajando, Mejor valor de la función objetivo
    while(True):
        vecin = Vecindario3(Mejor_candidato,combinacion)
        evaluacion_vecindario = Evaluar_todo(vecin, combinacion)
        condicion = min(evaluacion_vecindario)
        Mejor_candidato = vecin[Min(evaluacion_vecindario)]
        
        if(condicion >= Mejor):
            break
        else:
            Mejor = condicion

    return Mejor_candidato, Mejor #Retorna mejores tiempos, mejor valor de la función objetivo


""" 2 iteraciones """

def Vecindario2(solucion,combinaciones):
    pasos = [1,0,-1]
    vecindario = []
    for i in pasos:
        for j in pasos:
            temp = Operacion2(solucion,i,j)
            if(Check_all(temp,combinaciones) == True and Chequeo_intervalo(temp,combinaciones) == True):
                    vecindario.append(temp)
    if(len(vecindario) == 0): #Retorna la primera solución factible que encuentre
        
        return [Hill2(combinaciones)]
    return vecindario

def Hill2(combinaciones): #Retorna una solución mínima que respeta las claúsulas. Combinación de tamaño 2
    a = aviones[combinaciones[0]][1]
    if(aviones[combinaciones[1]][1]  > a + costos_aviones[combinaciones[1]][combinaciones[0]]):
        b = aviones[combinaciones[1]][1]
    else:
        b = a + costos_aviones[combinaciones[1]][combinaciones[0]]
    return [a,b]

def Operacion2(solucion,i,j): #Complemento del vecindario
    respuesta = [solucion[0] + i, solucion[1] + j]
    return respuesta

def Hill_climbing_final2(Mejor_candidato,combinacion,Mejor):

    while(True):
        vecin = Vecindario2(Mejor_candidato,combinacion)
        evaluacion_vecindario = Evaluar_todo(vecin, combinacion)
        condicion = min(evaluacion_vecindario)
        Mejor_candidato = vecin[Min(evaluacion_vecindario)]
        
        if(condicion >= Mejor):
            break
        else:
            Mejor = condicion

    return Mejor_candidato, Mejor #Retorna mejores tiempos, mejor valor de la función objetivo



""" 1 iteración """

def Llega_1(avion):
    if(aviones[avion][1] > aviones[avion][2]):
        tiempo = aviones[avion][1]
    else:
        tiempo = aviones[avion][2]
    return tiempo


""" Todo terreno """

def Ordenar():
    orden = aviones.copy()
    orden.sort(key=lambda x: x[0])
    
    indices = []
    cambiados = [0]*len(aviones)
    nuevo_orden = [x for x in range(len(aviones))]
    for i in range(len(aviones)):
        for j in range(len(aviones)):
            if(aviones[i] == orden[j] and cambiados[i] == 0 and cambiados[j] == 0):

                indices.append([i,j])
                cambiados[i] = 1
                cambiados[j] = 1
    for x in indices:
        nuevo_orden[x[0]] = x[1]
        nuevo_orden[x[1]] = x[0]
    for x in range(len(indices)): #Cambio en los costes de los aviones, pero solo en la posición de los arreglos
        Swap_orden(costos_aviones,indices[x][0], indices[x][1])
        temp = temprano_tarde[indices[x][0]].copy()
        temprano_tarde[indices[x][0]] = temprano_tarde[indices[x][1]].copy()
        temprano_tarde[indices[x][1]] = temp
    
    for x in range(len(costos_aviones)):
        temp = costos_aviones[x].copy() #Copia del arreglo de aviones
        for i in range(len(temp)):
            
            costos_aviones[x][i] = temp[nuevo_orden[i]]

    aviones.sort(key=lambda x:x[0])
    return

def Swap_orden(arreglo, i,j):
    temp = arreglo[j]
    arreglo[j] = arreglo[i]
    arreglo[i] = temp
    return

def Ya_agendados(combinaciones, combinacion): #Todas las combinaciones, y una en especifico que se borrar la
    if(len(combinacion) == 1):
        for x in range(len(combinaciones)):
            if combinacion == combinaciones[x]:
                combinaciones[x] = []
        return combinaciones, x
    
    for x in range(len(combinaciones)):
        if(combinaciones[x] == combinacion):
            borrar = x
            continue
        else:
            if(len(combinaciones[x]) == 0):
                    continue
            else:
                if(len(combinaciones[x]) > 1):
                    for i in combinacion:
                        if(len(combinaciones[x]) == 0):
                            continue
                        if(combinaciones[x].count(i) > 0):
                            combinaciones[x].remove(i)
                else:
                    if(combinacion.count(combinaciones[x][0]) > 0):
                            combinaciones[x] = []

    orden_llegada = combinaciones[borrar].copy()
    combinaciones[borrar] = []
    return combinaciones, orden_llegada

def Costo_llegada(i,tiempo):
    if (tiempo == aviones[i][2]):
        return 0
    elif (tiempo > aviones[i][2]):
        return temprano_tarde[i][1] * max(0,tiempo - aviones[i][2])
    else:
        return temprano_tarde[i][0] * max(0,aviones[i][2] - tiempo)

def Evaluar_todo(vecindario, combinaciones): #Evalúa un vecindario, es una Matriz
    resultado = []

    for x in range(len(vecindario)):
        resultado.append(Evaluar(combinaciones,vecindario[x]))
    return resultado

def Evaluar(combinaciones,tiempos):
    #Función Objetivo
    total = 0
    for i in range(len(combinaciones)):
        total += Costo_llegada(combinaciones[i],tiempos[i])

    return total



def Min(solucion):
    minimo = min(solucion)
    indice = solucion.index(minimo)
    return indice

def Costo_llegada(i,tiempo):
    if (tiempo == aviones[i][2]):
        return 0
    elif (tiempo > aviones[i][2]):
        return temprano_tarde[i][1] * max(0,tiempo - aviones[i][2])
    else:
        return temprano_tarde[i][0] * max(0,aviones[i][2] - tiempo)


def Chequeo_intervalo(solucion,combinaciones):
    indice = 1
    compara = combinaciones[indice]
    if(len(solucion) == 2):
        if(solucion[0] + costos_aviones[combinaciones[0]][compara] > solucion[1]):
            return False
        else:
            return True
    for x in range(len(solucion) - 1):
        if(solucion[x] + costos_aviones[combinaciones[x]][compara] > solucion[x+1]):
            return False
        compara = combinaciones[indice+1]
    return True

def Check_all(solucion,combinaciones): #Chequea si todas las combinaciones están dentro de una ventana
    for x in range(len(combinaciones)):
        if(Indiv(solucion[x],combinaciones[x]) != True):
            return False
    return True

def Indiv(valor,i): #Chequea si un valor está dentro de una ventana
    if(valor >= aviones[i][1] and valor <= aviones[i][3]):
        return True
    return False

def Limite_inferior(limite,indice_ultimo): #Fija el tiempo mínimo para llegar según los aviones que ya han llegado.
    for x in range(len(aviones)):
        if(indice_ultimo == x):
            continue
        if limite + costos_aviones[x][indice_ultimo] > aviones[x][1]:
            aviones[x][1] = limite + costos_aviones[x][indice_ultimo]
    return
        


"""Fin todo terreno"""
print("Antes de ordenar : " ,aviones)

Ordenar()

print("Después de ordenar : ", aviones)
print(costos_aviones)

combinaciones = [] #Posibles cambios en la solución
for i in range(len(aviones)):
    combinaciones.append([i])


for i in range(len(aviones)):
    for j in range(i,len(aviones)):
        if (i == j):
            continue
        if(aviones[i][0] + parametros[1] >= aviones[j][0]):
            combinaciones[i].append(j)

print("antes de :",combinaciones)
temp = []
for x in combinaciones:
    if(len(x) > 3):
        while(len(x) > 0):
            if(len(x) > 3):
                temp.append([x[0],x[1],x[2]])
                x.remove(x[0])
                x.remove(x[0])
                x.remove(x[0])
            elif (len(x) > 2):
                temp.append(x[0],x[1])
                x.remove(x[0])
                x.remove(x[0])
            else:
                temp.append([x[0]])
                x.remove(x[0])

for a in range(len(combinaciones)):
    if len(combinaciones[a]) == 0:
        index = a
        break



for x in range(len(temp)):
    for j in temp[x]:
        for i in combinaciones:
            if(i.count(j) > 0):
                i.remove(j) 



for a in temp:
    combinaciones.insert(index,a)
    index +=1


while(combinaciones.count([]) > 0):
    combinaciones.remove([])


ultimo_llega = 0
resultado = []
orden_llegada  = []

if(len(combinaciones[0]) == 3):

    inicial = Hill3(combinaciones[0]) #Toma los valores de los aviones que llegan en ese orden.
    vecin = Vecindario3(inicial,combinaciones[0])   #Genera un vecindario para 3 valores. 
    evaluacion_vecindario = Evaluar_todo(vecin,combinaciones[0]) #Genera la evaluación del vecindario.
if(len(combinaciones[0]) == 2):
    inicial = Hill2(combinaciones[0])
    vecin = Vecindario2(inicial,combinaciones[0])
    evaluacion_vecindario = Evaluar_todo(vecin,combinaciones[0])
"""if(len(combinaciones[0] == 1)):
    resultado.append(aviones[x[0]][2])
    orden_llegada.append(0)
    Limite_inferior(resultado[len(orden_llegada) - 1], orden_llegada[len(orden_llegada) - 1])
    combinaciones, llegan = Ya_agendados(combinaciones,0)"""

Mejor = min(evaluacion_vecindario)
Mejor_candidato = vecin[Min(evaluacion_vecindario)]
condicion = Mejor



#Hill climbing

"""while(True):
    vecin = Vecindario3(Mejor_candidato,combinaciones[0])
    evaluacion_vecindario = Evaluar_todo(vecin, combinaciones[0])
    condicion = min(evaluacion_vecindario)
    Mejor_candidato = vecin[Min(evaluacion_vecindario)]
    
    if(condicion >= Mejor):
        break
    else:
        Mejor = condicion"""
print("Vecindario inicial" , vecin)
for x in combinaciones:
    if(len(x) > 0):
        if(len(x) == 1): # Asigna su tiempo objetivo y, en caso de no poder, simplemente asigna el valor superior más cercanoa  la función objetivo
            if(ultimo_llega + costos_aviones[x[0]][orden_llegada[len(orden_llegada) - 1]] < aviones[x[0]][2]):
                resultado.append(aviones[x[0]][2])
            else:
                resultado.append(Llega_1(x[0]))
            orden_llegada.append(x[0])
            Limite_inferior(resultado[len(orden_llegada) - 1], orden_llegada[len(orden_llegada) - 1])
            combinaciones, llegan = Ya_agendados(combinaciones,x)
        elif(len(x) == 2):
            Mejor_candidato, Mejor = Hill_climbing_final2(Mejor_candidato,x,Mejor)
            
            for a in Mejor_candidato:
                resultado.append(a)
            combinaciones, llegan = Ya_agendados(combinaciones,x)
            ultimo_llega = Mejor_candidato[len(Mejor_candidato)-1]
            for b in llegan:
                orden_llegada.append(b)
            Limite_inferior(resultado[len(orden_llegada) - 1], orden_llegada[len(orden_llegada) - 1])
        elif(len(x) == 3):
            if(len(Mejor_candidato) == 2):
                inicial = Hill3(x) #Toma los valores de los aviones que llegan en ese orden.
                vecin = Vecindario3(inicial,x)   #Genera un vecindario para 3 valores. 
                evaluacion_vecindario = Evaluar_todo(vecin,x) #Genera la evaluación del vecindario.
                Mejor_candidato = vecin[Min(evaluacion_vecindario)]
            Mejor_candidato, Mejor = Hill_climbing_final3(Mejor_candidato,x,Mejor)
            for a in Mejor_candidato:
                resultado.append(a)
            combinaciones, llegan = Ya_agendados(combinaciones,x)
            ultimo_llega = Mejor_candidato[len(Mejor_candidato) - 1]
            for b in llegan:
                orden_llegada.append(b)
            Limite_inferior(resultado[len(orden_llegada) - 1], orden_llegada[len(orden_llegada) - 1])

        else:
            while(len(x) > 1):
                if(len(x) > 3):
                    combi = [x[0],x[1],x[2]]
                    Mejor_candidato, Mejor = Hill_climbing_final3(Mejor_candidato,combi,Mejor)
                    for a in Mejor_candidato:
                        resultado.append(a)
                    combinaciones, llegan = Ya_agendados(combinaciones,combi)
                    ultimo_llega = Mejor_candidato[len(Mejor_candidato) - 1]
                    for b in llegan:
                        orden_llegada.append(b)
                    Limite_inferior(resultado[len(orden_llegada) - 1], orden_llegada[len(orden_llegada) - 1])



print(orden_llegada)
print(resultado)
print(Evaluar(orden_llegada,resultado))

f = open('./resultados.txt','a')
f.write('\n' + f"{parametros[0]}" + " " + f"{Evaluar(orden_llegada,resultado)}")
f.close()