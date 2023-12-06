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
 """

import config as cf
import model
import time
import csv
import tracemalloc
import json 
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    analyzer = model.new_data_structs()
    return analyzer


# Funciones para la carga de datos
def mostrardatos(control):
    return model.mostrar_datos(control)
def load_data (control, filename_v,filename_a,filename_e,filename_cm):

    load_Vertices(control, filename_v)   
    load_estacion (control, filename_e)
    load_comparendos(control,filename_cm)
    load_Arcos(control, filename_a)
    return control

def load_Vertices(control, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    centinela = True

    with open(filename) as f:
        while centinela:
            vertice = f.readline()
            if not vertice:
                centinela = False
            else:
                vertice = vertice.split(",")
                model.add_verices(control,vertice)
    f.close()

# Funciones de ordenamiento
def load_Arcos(control, filename):
    centinela = True
    
    with open(filename) as f:
        arcos = f.readline()
        arcos = f.readline()
        while centinela:
            arcos = f.readline()
            if not arcos:
                centinela = False
            else:
                arcos = arcos.split()
                model.addConnection(control,arcos)
    f.close()

def load_estacion (control, filename):
    estaciones = cf.data_dir + filename
    input_file = csv.DictReader(open(estaciones,encoding="utf8"),
                                delimiter=",")
    for estacion in input_file:
        model.addEstacion(control,estacion)

def load_comparendos(control,filename):
    comparendos = cf.data_dir + filename
    input_file = csv.DictReader(open(comparendos,encoding="utf8"),
                                delimiter=",")
    for comparendo in input_file:
        model.addComparendos(control,comparendo)


def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, lat_i, long_i, lat_f, long_f):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    return model.req_1(control, lat_i, long_i, lat_f, long_f)


def req_2(control, lat_i, long_i, lat_f, long_f):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    return model.req_2(control, lat_i, long_i, lat_f, long_f)


def req_3(control, localidad, M):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(control, localidad, M)


def req_4(control, M):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    return model.req_4(control, M)


def req_5(control, M, vehiculo):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(control, M, vehiculo)

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control, lat_i, long_i, lat_f, long_f):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(control,lat_i,long_i,lat_f,long_f)


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass
    # Presente unicamente en el view.py


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
