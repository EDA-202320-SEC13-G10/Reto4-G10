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
            "arcos" : None,
            "vertices" : None,
            "connections" : None,
            "comparendos": None,
            "mapDatos": None,
            "lista_presentacion_estaccion": None,
            "lista_presentacion_comparendos": None,
        }
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=456091)
        analyzer["mapDatos"] = om.newMap()
        analyzer["lista_presentacion_estaccion"] = lt.newList()
        analyzer["lista_presentacion_comparendos"] = lt.newList()
       
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

    return analyzer


# Funciones para agregar informacion al modelo
def add_verices(analyzer, ticket):
    """
    Funcion que crea los vertices y agrega las estaciones
    al hash para hacer mas facil su recorrido
    """
    id_Estacion = ticket[0]

    lat = ticket[2]
    long = ticket[1]
    entry = om.get(analyzer["mapDatos"],id_Estacion)
    if entry is None:
        estacion_entry = new_Estacion(float(lat),float(long))
        om.put(analyzer["mapDatos"],id_Estacion,estacion_entry)
    
    if not gr.containsVertex(analyzer['connections'],id_Estacion):
        gr.insertVertex(analyzer['connections'],id_Estacion)
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
                n_comparendos = valor_i["Numeros_comparendos"] + valor_f["Numeros_comparendos"]
                edge = gr.addEdge(analyzer["connections"],final,initial,n_comparendos)
    return analyzer

def addEstacion(analyzer, estacion):
    entry = om.get(analyzer["mapDatos"],estacion["properties"]["OBJECTID"])
    if entry is None:
        lat = estacion["geometry"]["coordinates"][1]
        long = estacion["geometry"]["coordinates"][0]
        estacion_entry = new_Estacion(float(lat),float(long))
        om.put(analyzer["mapDatos"],estacion["properties"]["OBJECTID"],estacion_entry)
    else:
        entry["value"]["propiedades"] = estacion["properties"]
    return analyzer

def addComparendos(analyzer,comparendo):
    keys = om.keySet(analyzer["mapDatos"])
    comparendo = comparendo["properties"]
    distancia = None
    id_menor = None
    
    for key in lt.iterator(keys):
        valor = om.get(analyzer["mapDatos"],key)
        h_valor = valor["ubi"]
        h_comparendo = ( comparendo["properties"]["LATITUD"] , comparendo["properties"]["LONGITUD"] )
        haversine_nuevo  =haversine(h_valor,h_comparendo)
        if distancia == None:
            distancia = haversine_nuevo
            id_menor = key
        else:
            if distancia > haversine_nuevo:
                distancia = haversine_nuevo
                id_menor = key
    valor = om.get(analyzer["mapDatos"],id_menor)
    valor["value"]["Numeros_comparendos"] += 1
    lt.addLast(valor["value"]["comparendos"],comparendo["properties"])


def new_Estacion(lat,long):
    entry = {
        "ubi" : (lat,long),
        "propiedades" : None,
        "comparendos" : lt.newList(),
        "Numeros_comparendos" : 0
    }
    return entry

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

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


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

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
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
