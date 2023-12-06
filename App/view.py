"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import  orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import folium as fol
import webbrowser

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
filename_arco = "Data/tickets/bogota_arcos.txt"
filename_vertices = "Data/tickets/bogota_vertices.txt"
filename_comparendos = "tickets//comparendos_2019_bogota_vertices.csv"
filename_Estaciones = "tickets//estacionpolicia_bogota_vertices.csv"

def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return controller.new_controller()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    
    controller.load_data(control,filename_vertices,filename_arco,filename_Estaciones,filename_comparendos)



def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    
    # TODO: Imprimir el resultado del requerimiento 1
    print("Req No. 1 Input".center(130,"="))

    lat_i =  float(input("Latitud inicial: "))
    long_i =  float(input("Longitud inicial: "))
    lat_f =  float(input("Latitud final: "))
    long_f =  float(input("Longitud final: "))

    datos,d, size, vertice_i, vertice_f = controller.req_1(control,lat_i,long_i,lat_f,long_f)
    print(("Total distancia: " +str(d)+ " entre el vertice "+ vertice_i +" y el vertice "+ vertice_f))
    print(("El total de los vertices en el camino " +str(size)))
    print(("El total de seccuencia de los vertices: vvvv "))
    print(datos)
    


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("Req No. 2 Input".center(130,"="))

    lat_i =  float(input("Latitud inicial: "))
    long_i =  float(input("Longitud inicial: "))
    lat_f =  float(input("Latitud final: "))
    long_f =  float(input("Longitud final: "))

    datos,d, size, vertice_i, vertice_f = controller.req_2(control,lat_i,long_i,lat_f,long_f)
    print(("Total distancia: " +str(d)+ " entre el vertice "+ vertice_i +" y el vertice "+ vertice_f))
    print(("El total de los vertices en el camino " +str(size)))
    print(("El total de seccuencia de los vertices: vvvv "))
    print(datos)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    print("Req No. 3 Input".center(130,"="))

    localidad =  (input("localidad inicial: "))
    m =  int(input("Numero de camaras a instalar: "))


    tamanio,v,distancia_total,precio = controller.req_3(control,localidad, m)

    print(("El total de los vertices en el camino " +str(tamanio) + "en la localidad de " + str(localidad)))
    print(("El total de seccuencia de los vertices: vvvv "))
    print(v)
    print(("Kilometros recorridos" + str(distancia_total)))
    print(("El costo total de la instalacion es:" + str(precio)))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print("Req No. 4 Input".center(130,"="))

    m =  int(input("Numero de camaras a instalar: "))

    tamanio,v,distancia_total,precio = controller.model.req_4(control, m)

    print(("El total de los vertices en el camino " +str(tamanio)+ " con mayor gravedad de comparendos"))
    print(("El total de seccuencia de los vertices: vvvv "))
    print(v)
    print(("Kilometros recorridos" + str(distancia_total)))
    print(("El costo total de la instalacion es:" + str(precio)))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print("Req No. 5 Input".center(130,"="))

    m =  int(input("Numero de camaras a instalar: "))
    vehiculo = input("Clase de vehiculo: ")
    
    tamanio,v,distancia_total,precio = controller.model.req_5(control, m, vehiculo)

    print(("El total de los vertices en el camino " +str(tamanio)+ " con mayor gravedad de comparendos"))
    print(("El total de seccuencia de los vertices: vvvv "))
    print(v)
    print(("Kilometros recorridos" + str(distancia_total)))
    print(("El costo total de la instalacion es:" + str(precio)))


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    print("Req No. 7 Input".center(130,"="))

    lat_i =  float(input("Latitud inicial: "))
    long_i =  float(input("Longitud inicial: "))
    lat_f =  float(input("Latitud final: "))
    long_f =  float(input("Longitud final: "))

    tamanio ,datos,muestra,n_comaprendos, distancia = controller.req_7(control,lat_i,long_i,lat_f,long_f)
    print(("El total de los vertices en el camino " +str(tamanio)))
    print(("El total de seccuencia de los vertices: vvvv "))
    print(datos)
    print(("El total de seccuencia de los arcos: vvvv "))
    print(muestra)
    print(("El total de comparendos es " +str(n_comaprendos)))
    print(("Kilometros recorridos" + str(distancia)))


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    mapa = fol.Map(location=[4.656931, -74.050868], zoom_start=13)

# Añadir una capa de Google Maps
    fol.TileLayer('https://maps.googleapis.com/maps/api/staticmap?center={0},{1}&zoom={2}&scale={3}&size={4}x{4}&maptype={5}&format={6}&visual_refresh={7}&key={8}',
                 attr='Google',
                 subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                 min_zoom=0,
                 max_zoom=23,
                 bounds=True,
                 origin='upper'
                 ).add_to(mapa)


# Se crea el controlador asociado a la vista
    control = new_controller()
    valores = control["mapDatos"]
    for i in lt.iterator(mp.keySet(valores)):
        valor = mp.get(valores,i)
        tupla = valor["value"]["ubi"]
        fol.Marker(
                location=tupla,
                icon=fol.Icon(icon="cloud",color="green"),
            ).add_to(mapa)
    
    mapa.save("footprint.html")
    webbrowser.open("footprint.html")


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
