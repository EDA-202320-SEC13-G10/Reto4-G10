"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.Utils import error as error
from haversine import haversine, Unit
import math

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    try:
        analyzer = {
           
            "vertices" : None,
            "connections" : None,
            "connections_o_hash" : None,
            "mapDatos": None,
            "mapEstaciones": None,
            "mapLocalidades": None, 

            "lista_presentacion_estaccion": None,
            "lista_presentacion_comparendos": None,

            "s_req1": None,
            "s_req2": None,
            "s_req3": None,
            "s_req4": None,
            "s_req5": None,
            "req_6": None,
            "req_7": None
        }
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=456091)
        analyzer['connections_o_hash'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=456091)
        analyzer['connections_o_comp'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=456091)
        
        analyzer["mapDatos"] = om.newMap()
        analyzer["mapEstaciones"] = om.newMap()
        analyzer["mapLocalidades"] = om.newMap()

        analyzer["vertices"] = lt.newList("ARRAY_LIST")
        analyzer["lista_presentacion_estaccion"] = lt.newList("ARRAY_LIST")
        analyzer["lista_presentacion_comparendos"] = lt.newList("ARRAY_LIST")
       
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

    return analyzer


# Funciones para agregar informacion al modelo


    #TODO: Crear la función para agregar elementos a una lista
    
def propiedades(analyzer): 
    num_vertices = gr.numVertices(analyzer["connections"])
    num_arcos = gr.numEdges(analyzer["connections"])
    return num_vertices,num_arcos

def add_verices(analyzer, ticket):
    """
    Funcion que crea los vertices y agrega las estaciones
    al hash para hacer mas facil su recorrido
    """
    d = {
        "N_vertice" :  ticket[0],
        "lat" :  ticket[2],
        "long" :  ticket[1],
    }
    lt.addLast(analyzer["vertices"],d)
    numero_malla = str(ticket[0])

    lat = ticket[2]
    long = ticket[1]
    entry = om.get(analyzer["mapDatos"],numero_malla)
    if entry is None:
        estacion_entry = new_Malla_vial(float(lat),float(long))
        om.put(analyzer["mapDatos"],numero_malla,estacion_entry)
    
    if not gr.containsVertex(analyzer['connections'],numero_malla):
        gr.insertVertex(analyzer['connections'],numero_malla)
        gr.insertVertex(analyzer['connections_o_hash'],numero_malla)
        
    return analyzer


def addConnection(analyzer,ltsConennctions):

    """añade los arcos entre las etaciones y calcula la distancia Haversine atravez de un map con las id de las estaciones y su lat y long"""
    tamanio = len(ltsConennctions)
    for i in range(0,tamanio):  
        if i+1 < tamanio:
            initial = ltsConennctions[i]
            final = ltsConennctions[i+1] 
            edge = gr.getEdge(analyzer["connections"],initial,final)
             
            if edge is None:
                valor_i = (om.get(analyzer["mapDatos"],initial))["value"]
                valor_f = (om.get(analyzer["mapDatos"],final))["value"]
                h_initial =valor_i["ubi"] 
                h_final = valor_f["ubi"]
                hsn = haversine(h_initial,h_final)
                edge = gr.addEdge(analyzer["connections"],initial,final,hsn)
                gr.addEdge(analyzer["connections_o_hash"],initial,final,hsn)
                gr.addEdge(analyzer["connections_o_hash"],final,initial,hsn)
                n_comparendos = lt.size(valor_i["comparendos"]) + lt.size(valor_f["comparendos"]) 
                edge = gr.addEdge(analyzer["connections"],final,initial,n_comparendos)
                
                gr.addEdge(analyzer["connections_o_comp"],final,initial,n_comparendos)
                gr.addEdge(analyzer["connections_o_comp"],initial,final,n_comparendos)

    return analyzer

def addEstacion(analyzer, estacion):
    mp_estaciones = analyzer["mapEstaciones"]
    d = {
        "ID" : estacion["OBJECTID"],
        "N-Estacion" : estacion["EPONOMBRE"],
        "LATITUD" : estacion["EPOLATITUD"],
        "LONGITUD" : estacion["EPOLONGITU"],
        "DESCRIPCION" : estacion["EPODESCRIP"],
        "DIRECCION" : estacion["EPODIR_SITIO"],
        "TIPO_SERVICIO" : estacion["EPOSERVICIO"],
        "HORARIO" : estacion["EPOHORARIO"],
        "TELEFONO" : estacion["EPOTELEFON"],
        "CORREO" : estacion["EPOCELECTR"]
    }
    lt.addLast(analyzer["lista_presentacion_estaccion"],d)
    entry = om.get(mp_estaciones,estacion["OBJECTID"])
    entry_hash = om.get(analyzer["mapDatos"],estacion["VERTICES"])
    if entry is None:
        estacion_entry = new_Estacion()
        estacion_entry["propiedades"] = estacion
        om.put(analyzer["mapEstaciones"],estacion["OBJECTID"],estacion_entry)
    if entry_hash is not None:
        om.get(mp_estaciones,estacion["OBJECTID"])["value"]["Estaciones_cercanas"] = estacion
    return analyzer


def addComparendos(analyzer,comparendo):
    d = {
        "ID" : comparendo["OBJECTID"],
        "LATITUD" : comparendo["LATITUD"],
        "LONGITUD" : comparendo["LONGITUD"],
        "FECHA_HORA" : comparendo["FECHA_HORA"],
        "MEDIO_DETECCION" : comparendo["MEDIO_DETECCION"],
        "CLASE_VEHICULO" : comparendo["CLASE_VEHICULO"],
        "TIPO_SERVICIO" : comparendo["TIPO_SERVICIO"],
        "INFRACCION" : comparendo["INFRACCION"],
        "DESCRIPCION" : comparendo["DES_INFRACCION"],
        "LOCALIDAD" : comparendo["LOCALIDAD"],
        "VERTICES" : comparendo["VERTICES"]
    }
    lt.addLast(analyzer["lista_presentacion_comparendos"],d)

    valor = om.get(analyzer["mapDatos"],comparendo["VERTICES"])
    if valor is not None:
        lt.addLast(valor["value"]["comparendos"],comparendo)
    


def new_Malla_vial(lat,long):
    entry = {
        "ubi" : (lat,long),
        "propiedades" : None,
        "comparendos" : lt.newList(),
        "Estaciones_cercanas" : {}

    }
    return entry

def new_Estacion():
    entry = {
        "propiedades" : None
        }
    return entry

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def data_sizel(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    return lt.size(data_structs) 

def sublista(data_structs, pos_i, num):
    s =  lt.subList(data_structs, pos_i, num)
    return s

def first_last5(data_structs):
    primeros = sublista(data_structs,1,5)
    ultimos = sublista(data_structs,data_sizel(data_structs)-4,5)
    for i in lt.iterator(ultimos):
        lt.addLast(primeros,i)
    return primeros

def mostrar_datos(analyzer):

    sizecomparendo = lt.size(analyzer["lista_presentacion_comparendos"])
    l_presentarC = first_last5(analyzer["lista_presentacion_comparendos"])
    sizeestaciones = lt.size(analyzer["lista_presentacion_estaccion"])
    l_presentarE = first_last5(analyzer["lista_presentacion_estaccion"])
    nm = gr.numVertices(analyzer["connections"])
    l_presentarV = first_last5(analyzer["vertices"])
    return sizecomparendo,l_presentarC,sizeestaciones,l_presentarE,nm,l_presentarV

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass

def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

def vertices_mas_cercanos(map,lat,long,lat1,long1):

    """ Se usa para recorre cada verticee de la malla vial para poder determinar
     el vertice inicial y el vertice final """
    key_Menor = None
    distancia = None
    key_Menor1 = None
    distancia1 = None
    lista_key = om.keySet(map)
    h_valor = (lat,long)
    h_valor1 = (lat1,long1)
    for i in lt.iterator(lista_key):
        
        valor = (om.get(map,i))["value"]["ubi"]
        distancia_h = haversine(valor,h_valor)
        if key_Menor == None and distancia == None:
            distancia = distancia_h
            key_Menor = i
        elif distancia > distancia_h:
            distancia = distancia_h
            key_Menor = i
        distancia_h1 = haversine(valor,h_valor1)
        if key_Menor1 == None and distancia1 == None:
            distancia1 = distancia_h1
            key_Menor1 = i
        elif distancia1 > distancia_h1:
            distancia1 = distancia_h1
            key_Menor1 = i
    return key_Menor, key_Menor1

def distancia_secuencia(analyzer,pila):
    numero_anteior = None
    datos = lt.newList("ARRAY_LIST")

    distancia  = 0
    centinela = st.isEmpty(pila)
    while centinela == False:
        numero = st.pop(pila)
        if numero_anteior ==None:
            numero_anteior = numero
        else:
            
              lt.addLast(datos,numero)
        centinela = st.isEmpty(pila)

    numero = None
    numero_anterior_lista = None
    for i in lt.iterator(datos):
        numero = i
        if numero_anterior_lista ==None:
            numero_anterior_lista =  numero
        else:
            arco = gr.getEdge(analyzer,numero_anterior_lista,numero)
            if type(arco["weight"]) == int:
                arco = gr.getEdge(analyzer,numero,numero_anterior_lista)
            
            distancia += arco["weight"]
        numero_anterior_lista =  numero
        
    return datos,distancia

def req_1(analyzer,lat_i,long_i,lat_f,long_f):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    vertice_i, vertice_f= vertices_mas_cercanos(analyzer["mapDatos"],lat_i,long_i,lat_f,long_f)
    analyzer["s_req1"] =  bfs.BreathFirstSearch(analyzer["connections"],vertice_i)
    if bfs.hasPathTo(analyzer['s_req1'],vertice_f) == True:
        pila =  bfs.pathTo(analyzer["s_req1"],vertice_f)
    datos,d = distancia_secuencia(analyzer["connections"],pila)
    size = lt.size(datos)

    return datos,d, size, vertice_i, vertice_f

def req_2(analyzer,lat_i,long_i,lat_f,long_f):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    vertice_i, vertice_f= vertices_mas_cercanos(analyzer["mapDatos"],lat_i,long_i,lat_f,long_f)
    analyzer["s_req2"] =  bfs.BreathFirstSearch(analyzer["connections"],vertice_i)
    if bfs.hasPathTo(analyzer['s_req2'],vertice_f) == True:
        pila =  bfs.pathTo(analyzer["s_req2"],vertice_f)
    datos,d = distancia_secuencia(analyzer["connections"],pila)
    size = lt.size(datos)
    return datos,d, size, vertice_i, vertice_f
    
def req_3(analyzer, localidad, M):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    lista = lt.newList("ARRAY_LIST")
    lista1 = lt.newList("ARRAY_LIST")
    d = {
    }
    for i in lt.iterator(analyzer["lista_presentacion_comparendos"]):
        if i["LOCALIDAD"].lower() == localidad.lower():
            if i["VERTICES"] not in d:
                d[i["VERTICES"]] = 1
            else:
                d[i["VERTICES"]] +=1
    
    for i in d.keys():
        l = {"vertice" : i,
             "n_comparendos" : d[i]
             }
        lt.addLast(lista,l)
    

    y = merg.sort(lista,sort_criteria)
    sublista = lt.subList(y,1,M)
    
    for i in lt.iterator(sublista):
        lt.addLast(lista1,i["vertice"])
    sublista1 = lt.subList(lista1,1,M)    
    distancia_total = 0
    numero = None
    numero_base = lt.getElement(sublista1,0)
    datos = lt.newList("ARRAY_LIST")
    analyzer["s_req3"] =  prim.PrimMST(analyzer["connections_o_hash"],numero_base)
    for i in lt.iterator(sublista1):
            numero = i   
            espacio = prim.scan(analyzer["connections_o_comp"],analyzer['s_req3'],numero)
            if espacio != math.inf:
                    pila =  prim.edgesMST(analyzer["s_req3"],numero)
                    distancia_total += espacio
                   

                    centinela = st.isEmpty(pila)
                    while centinela == False:
                        numero1 = st.pop(pila)
                        if lt.isPresent(datos,numero1) == 0:
                            lt.addLast(datos,numero1)
                        centinela = st.isEmpty(pila)
                    


    return  M, gr.vertices(analyzer["s_req3"]), distancia_total, distancia_total*1000000

def req_4(analyzer, M):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    identifyu = lt.newList("ARRAY_LIST")
    lista = lt.newList("ARRAY_LIST")
    lista1 = lt.newList("ARRAY_LIST")
    d = {
    }
    for i in lt.iterator(analyzer["lista_presentacion_comparendos"]):
        if i["VERTICES"] not in d:
            d[i["VERTICES"]] = [i["TIPO_SERVICIO"], i["INFRACCION"]]
        else:
            # Hallar el comparendo mas grave
            if organizar_mayor_comp(d[i["VERTICES"]], [i["TIPO_SERVICIO"], i["INFRACCION"]]) == False:
                d[i["VERTICES"]] = [i["TIPO_SERVICIO"], i["INFRACCION"]]
            
    for i in d.keys():
        l = {"vertice" : i,
             "mayor_comp" : d[i]
             }
        lt.addLast(lista,l)
    
    y = merg.sort(lista,sort_criteria_2)
    sublista = lt.subList(y,1,M)
    
    for i in lt.iterator(sublista):
        lt.addLast(lista1,i["vertice"])
    sublista1 = lt.subList(lista1,1,M)    
    distancia_total = 0
    numero = None
    numero_base = lt.getElement(sublista1,0)
    datos = lt.newList("ARRAY_LIST")
    analyzer["s_req4"] =  prim.PrimMST(analyzer["connections_o_hash"],numero_base)
    for i in lt.iterator(sublista1):
            numero = i   
            espacio = prim.scan(analyzer["connections_o_comp"],analyzer['s_req4'],numero)
            if espacio != math.inf:
                    pila =  prim.edgesMST(analyzer["s_req4"],numero)
                    distancia_total += espacio
                   

                    centinela = st.isEmpty(pila)
                    while centinela == False:
                        numero1 = st.pop(pila)
                        if lt.isPresent(datos,numero1) == 0:
                            lt.addLast(datos,numero1)
                        centinela = st.isEmpty(pila)
                    


    return  analyzer["s_req4"], M, gr.vertices(analyzer["s_req4"]), distancia_total, distancia_total*1000000


def req_5(analyzer, M, vehiculo):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    identifyu = lt.newList("ARRAY_LIST")
    lista = lt.newList("ARRAY_LIST")
    lista1 = lt.newList("ARRAY_LIST")
    d = {
    }
    for i in lt.iterator(analyzer["lista_presentacion_comparendos"]):
        if i["CLASE_VEHICULO"].lower() == vehiculo.lower():
            if i["VERTICES"] not in d:
                d[i["VERTICES"]] = 1
            else:
                d[i["VERTICES"]] +=1
    
    for i in d.keys():
        l = {"vertice" : i,
             "n_comparendos" : d[i]
             }
        lt.addLast(lista,l)
    

    y = merg.sort(lista,sort_criteria)
    sublista = lt.subList(y,1,M)
    
    for i in lt.iterator(sublista):
        lt.addLast(lista1,i["vertice"])
    sublista1 = lt.subList(lista1,1,M)    
    distancia_total = 0
    numero = None
    numero_base = lt.getElement(sublista1,0)
    datos = lt.newList("ARRAY_LIST")
    analyzer["s_req5"] =  prim.PrimMST(analyzer["connections_o_hash"],numero_base)
    for i in lt.iterator(sublista1):
            numero = i   
            espacio = prim.scan(analyzer["connections_o_comp"],analyzer['s_req5'],numero)
            if espacio != math.inf:
                    pila =  prim.edgesMST(analyzer["s_req5"],numero)
                    distancia_total += espacio
                   

                    centinela = st.isEmpty(pila)
                    while centinela == False:
                        numero1 = st.pop(pila)
                        if lt.isPresent(datos,numero1) == 0:
                            lt.addLast(datos,numero1)
                        centinela = st.isEmpty(pila)
                    


    return  analyzer["s_req5"], M, gr.vertices(analyzer["s_req5"]), distancia_total, distancia_total*1000000

    


def req_6(analyzer,m):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    menor_lat = 100
    mayor_lat = 0 
    menor_long = 100
    mayor_long = 0 
    for i in lt.iterator(analyzer["lista_presentacion_comparendos"]):
        lat = float(i["LATITUD"])
        long = abs(float(i["LONGITUD"]))
        if  lat > mayor_lat:
            mayor_lat = lat
        if lat < menor_lat:
            menor_lat = lat
        if long > mayor_long:
            mayor_long =long
        if long < menor_long:
            menor_long = long
    y = analyzer["lista_presentacion_comparendos"]
    l =["Público","Oficial","Particular"]
    
    u = lt.newList()
    for m in lt.iterator(y):
        if m["TIPO_SERVICIO"] == l[0]:
            lt.addLast(u,m)
       


    return quk.sort(u,compare)


def req_7(analyzer,lat_i,long_i,lat_f,long_f):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    numero_ante = None

    distancia_hash = 0
    muestra = lt.newList("ARRAY_LIST")
    datos = lt.newList("ARRAY_LIST")
    n_comaprendos = 0
    vertice_i, vertice_f= vertices_mas_cercanos(analyzer["mapDatos"],lat_i,long_i,lat_f,long_f)
    analyzer["req_7"] = djk.Dijkstra(analyzer["connections_comp"],vertice_i)
    if djk.hasPathTo(analyzer["req_7"],vertice_f):
        req8 = djk.pathTo(analyzer["req_7"],vertice_f)
        centinela = st.isEmpty(req8)
        while centinela == False:
                numero1 = st.pop(req8)
                if numero_ante == None:
                    numero_ante = numero1
                    
                else:
                    arco = gr.getEdge(analyzer["connections_comp"],numero_ante,numero1)
                    arc1 = gr.getEdge(analyzer["connections"],numero_ante,numero1)
                    d = {
                        "vertice_i" : numero_ante,
                        "vertice_f" : numero1,
                        "arco" : arco
                    }
                  
                    distancia_hash += arc1
                    lt.addLast(muestra,d)
                lt.addLast(datos,numero1)
                numero_ante = numero1 
                centinela = st.isEmpty(req8)
                n_comaprendos += lt.size((mp.get(analyzer["mapDatos"],numero1))["value"]["comparendos"])

    return lt.size(datos),datos,muestra,n_comaprendos, distancia_hash


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass
    # Presente unicamente el view.py

# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista

    return data_1["INFRACCION"] < data_2["INFRACCION"]

    
   
        
        

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar

    return data_1["n_comparendos"] > data_2["n_comparendos"]

def organizar_mayor_comp(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    if data_1[0] == "Oficial" and (data_2[0] == "Público" or data_2[0] == "Particular"):
        return True
    elif data_1[0] == "Público" and data_2[0] == "Particular":
        return True
    elif data_1[0] == "Particular" and (data_2[0] == "Público" or data_2[0] == "Oficial"):
        return False
    elif data_1[0] == "Público" and data_2[0] == "Oficial":
        return False
    elif (data_1[0] == "Oficial" and data_2[0] == "Oficial") or (data_1[0] == "Particular" and data_2[0] == "Particular") or (data_1[0] == "Público" and data_2[0] == "Público"):
        if data_1[1] >= data_2[1]:
            return True
        elif data_1[1] < data_2[1]:
            return False
        
def sort_criteria_2(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    data_1 = data_1["mayor_comp"]
    data_2 = data_2["mayor_comp"]
    if data_1[0] == "Oficial" and (data_2[0] == "Público" or data_2[0] == "Particular"):
        return True
    elif data_1[0] == "Público" and data_2[0] == "Particular":
        return True
    elif data_1[0] == "Particular" and (data_2[0] == "Público" or data_2[0] == "Oficial"):
        return False
    elif data_1[0] == "Público" and data_2[0] == "Oficial":
        return False
    elif (data_1[0] == "Oficial" and data_2[0] == "Oficial") or (data_1[0] == "Particular" and data_2[0] == "Particular") or (data_1[0] == "Público" and data_2[0] == "Público"):
        if data_1[1] >= data_2[1]:
            return True
        elif data_1[1] < data_2[1]:
            return False

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
