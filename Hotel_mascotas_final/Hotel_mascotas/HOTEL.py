from datetime import datetime
import sqlite3
import time 
from clases.persona import *
from clases.factura import Factura
from clases.mascota import *
from clases.reservacion import reservacion
from clases.detalle_factura import DetalleFactura
from clases.habitacion import habitacion
# Conectar a la base de datos
conn = sqlite3.connect('hotelm.db')

# Crear un cursor para ejecutar comandos
cursor = conn.cursor()

def validar_entero(mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número entero.")

def validar_cadena(mensaje):
        while True:
            cadena = input(mensaje).strip()
            if cadena:
                return cadena
            print("La entrada no puede estar vacía. Inténtalo de nuevo.")

def validar_fecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        try:
            # Intentar convertir la cadena a un objeto de fecha
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d")
            return fecha  # Devuelve la fecha válida como cadena
        except ValueError:
            print("Fecha inválida. Asegúrese de que esté en el formato YYYY-MM-DD y sea una fecha real (ej: 2023-12-31).")

def submenu():
    opciones = ["Agregar dato", "Ver datos", "Eliminar datos", "Actualizar datos"]
    x = 0
    print("\n   Opciones en la tabla"    )
    print("--------------------------")
    for opcion in opciones:
        x += 1
        print("| {0} | {1} |".format(x, opcion.center(18)))
def submenureserva():
    opciones = ["Hacer reservación", "Ver reservación", "Cancelar reservación", "Actualizar reservación"]
    x = 0
    print("\n   Opciones en la tabla"    )
    print("--------------------------")
    for opcion in opciones:
        x += 1
        print("| {0} | {1} |".format(x, opcion.center(18)))
        
def preguntar(conn):
    val = int(input("\n   Desea realizar otra acción? : \n 1. Si \n 2. No \n"))
    if val == 1:
        volver_menu()
    elif val == 2:
        conn.close()
        exit()
    else:
        print("Opcion no válida")
        preguntar(conn)
def volver_menu():
    print("Volviendo al menú...")
    time.sleep(1)
    menu_principal()
    
def menu_principal():
    #Utilicé el mismo ejemplo de la consulta para llamar las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';") #Hace una consulta a la bd para ver las tablas existentes (menos la sqlite_sequence, que solo se encarga de los id incrementales)
    tablas = cursor.fetchall()
   
   
    x=0 
    print("\nTablas en la base de datos")
    print("--------------------------")
    for tabla  in tablas:# el ciclo es solamente para que numeración
        x=x+1
        print("| {0} | {1} |". format (x,tabla[0].center(18)))
    print("\n¡Hola!\n Selecciona el número correspondiente a la tabla de la base de dato deseas interactuar, presione 0 para salir")

    try:
        numero_tabla = int(input("-"))
        if numero_tabla == 0:
            conn.close
            exit()
    except ValueError:
        print("Valor Incorrecto")
        volver_menu()

    if numero_tabla == 1: # manejo de clientes
        instancia_cliente = cliente(None, None, None, None, None, None)
        submenu()

        try :
            eleccion = int(input("\n Elige tu opcion: "))
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1: # crear cliente
            rut = validar_entero("¿Cual es el rut del cliente que deseas agregar?: ")
            nombre = validar_cadena("Ingrese el nuevo nombre del cliente: ")
            apellido = validar_cadena("Ingrese el nuevo apellido del cliente: ")
            fono = validar_entero("Ingrese el nuevo teléfono del cliente sin espacios ni signos: ")
            mail = validar_cadena("Ingrese el nuevo correo del cliente: ")
            direccion = validar_cadena("Ingrese la nueva dirección del cliente: ")

            nuevo_cliente = cliente(rut, nombre, apellido, fono, mail, direccion)
            if not nuevo_cliente.rut_existe(conn, rut):
                try: 
                    nuevo_cliente.crear_cliente(conn) 
                    print(f"Cliente creado exitosamente con ID: {nuevo_cliente._rut}")
                except Exception as e:  # Captura cualquier otro error que pueda ocurrir al crear
                    print(f"Ocurrió un error inesperado: {e}")
                    volver_menu()
            else:
                print(f"Error: Ya existe un cliente con el RUT {rut}.")
                volver_menu()

        if eleccion == 2: #ver datos del cliente con rut especifico
            rut_vista = validar_entero("Ingresa rut del cliente que deseas visualizar: ") 
            mostrar_cliente = instancia_cliente.leer_cliente(rut_vista, conn)

            if mostrar_cliente:
                print(f"\n Información de cliente {rut_vista}:")
                print(f"Nombre: {mostrar_cliente[1]}")
                print(f"Apellido: {mostrar_cliente[2]}")
                print(f"Telefono: {mostrar_cliente[3]}")
                print(f"Mail: {mostrar_cliente[4]}")
                print(f"Dirección: {mostrar_cliente[5]}")
            else:
                print(f"No se encontró ningun cliente con el RUT {rut_vista}")  

        if eleccion == 3: #eliminar cliente con rut especifico
            rut_eliminar = validar_entero("Ingresa el rut del cliente que deseas eliminar: ") #repetimos proceso pero ahora utilizando eliminar
            try:
                instancia_cliente.borrar_cliente(rut_eliminar, conn)
                print(f"Cliente con RUT {rut_eliminar} eliminado con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al eliminar el cliente: {e}")
                volver_menu()
            instancia_cliente.borrar_cliente(rut_eliminar, conn)
        

        if eleccion == 4: #actualizar datos de cliente con rut especifico
            rut = validar_entero("¿Cual es el rut del cliente que deseas actualizar?: ")
            nombre = validar_cadena("Ingrese el nuevo nombre del cliente: ")
            apellido = validar_cadena("Ingrese el nuevo apellido del cliente: ")
            fono = validar_entero("Ingrese el nuevo teléfono del cliente sin espacios ni signos: ")
            mail = validar_cadena("Ingrese el nuevo correo del cliente: ")
            direccion = validar_cadena("Ingrese la nueva dirección del cliente: ")

            cliente_actualizado = cliente(rut, nombre,apellido,fono,mail,direccion)
            
            try:
                cliente_actualizado.actualizar_cliente(conn)
                print(f"Cliente con ID {rut} actualizado con éxito.")
            except sqlite3.IntegrityError as e:
                print("Error: Ya existe un cliente con ese ID o RUT.")
                volver_menu()
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                volver_menu()
        preguntar(conn)

    elif numero_tabla == 2: #manejo de mascotas
        submenu()
        
        try :
            eleccion = int(input("\n Elige tu opcion: "))
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1:
            RUT_CLIENTE = validar_entero("ingrese el rut del dueño: ")
            nombre_mascota = validar_cadena("ingrese el nombre de la mascota: ")
            tipo= validar_cadena("ingrese qué tipo de animal es: ")
            edad = validar_entero("ingrese la edad de la mascota: ")
            historial_medico = validar_cadena("ingrese detalles médicos de interés: ")
            tamaño = validar_cadena("ingrese el tamaño que tiene la mascota: ")
            if tipo.lower() == "perro":
                nueva_mascota = Perro(RUT_CLIENTE,nombre_mascota,tipo,edad,historial_medico,tamaño)
            elif tipo.lower() == "gato":
                nueva_mascota = Gato(RUT_CLIENTE,nombre_mascota,tipo,edad,historial_medico,tamaño)
            else:
                nueva_mascota = mascota(RUT_CLIENTE,nombre_mascota,tipo,edad,historial_medico,tamaño)
            try:
                nueva_mascota.crear_mascota(conn)
                print(f"Mascota creada exitosamente con ID: {nueva_mascota._id_mascota} \n")
                if tipo.lower() == "perro" or tipo.lower() == "gato":
                    print(nueva_mascota.higiene())
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                
            
        if eleccion == 2:
           id_mascota = validar_entero("ingrese el id de la mascota que desea ver: ")
           mascota.leer_mascota(id_mascota,conn)
           
        if eleccion == 3: 
            id_mascota_eliminar = validar_entero("ingrese el id de la mascota que desea eliminar: ")
            try:
                mascota.borrar_mascota(id_mascota_eliminar, conn)
                print(f"Mascota con ID {id_mascota_eliminar} eliminada con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al eliminar la mascota: {e}")
                volver_menu()

        if eleccion == 4: 
            id_mascota = validar_entero("ingrese el id de la mascota a actualizar: ")
            RUT_CLIENTE = validar_entero("ingrese el rut del dueño: ")
            nombre_mascota = validar_cadena("ingrese el nombre de la mascota: ")
            tipo= validar_cadena("ingrese qué tipo de animal es: ")
            edad = validar_entero("ingrese la edad de la mascota: ")
            historial_medico = validar_cadena("ingrese detalles médicos de interés: ")
            tamano = validar_cadena("ingrese el tamaño que tiene la mascota: ")

            if tipo.lower() == "perro":
                mascota_actualizada = Perro(RUT_CLIENTE,nombre_mascota,tipo,edad,historial_medico,tamano)
            elif tipo.lower() == "gato":
                mascota_actualizada = Gato(RUT_CLIENTE,nombre_mascota,tipo,edad,historial_medico,tamano)
            else:
                mascota_actualizada = mascota(RUT_CLIENTE,nombre_mascota,tipo,edad,historial_medico,tamano)
            try:
                mascota.actualizar_mascota(conn, id_mascota, RUT_CLIENTE, nombre_mascota, tipo, edad, historial_medico, tamano)
                print(f"Mascota actualizada exitosamente con ID: {id_mascota}")
                if tipo.lower() == "perro" or tipo.lower() == "gato":
                    print(mascota_actualizada.higiene())
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
        preguntar(conn)

    elif numero_tabla == 3: #manejo factura
        submenu()
        
        try :
            eleccion = int(input("\n Elige tu opcion: "))
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1:
            id_reserva = validar_entero("ingrese el id de la reservación: ")
            metodo_pago = validar_cadena("Ingrese el metodo de pago a usar: ")
            rut_cliente = validar_entero ("Ingrese el rut del cliente al que pertenece: ")
            try:
                id_factura = Factura.crear_factura(conn, id_reserva, metodo_pago, rut_cliente)
                print(f"Factura creada exitosamente con ID: {id_factura}")
            except Exception as e:
                print(f"Ocurrió un error al crear la factura: {e}")
                volver_menu()

        if eleccion == 2: 
            factura_vista = validar_entero("Ingrese el número de la factura que desea ver: ")
            try:
                resultado = Factura.leer_factura(conn, factura_vista)
                if resultado:
                    print(f"Factura encontrada: {resultado}")
                else:
                    print("No se encontró ninguna factura con ese número.")
            except Exception as e:
                print(f"Ocurrió un error al intentar leer la factura: {e}")
                volver_menu()

        if eleccion == 3: 
            factura_eliminar = validar_entero("ingrese el numero de la factura que desea eliminar: ")
            try:
                Factura.borrar_factura(conn, factura_eliminar)
                print(f"Factura con ID {factura_eliminar} eliminada con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al intentar eliminar la factura: {e}")
                volver_menu()
        
        if eleccion == 4: 
            id_factura = validar_entero("Ingrese el ID de la factura que desea actualizar: ")  # Obtener el ID de la factura
            id_reserva = validar_entero("Ingrese el nuevo ID de la reservación: ")  # Obtener el nuevo ID de la reservación
            fecha = validar_fecha("Ingrese la nueva fecha (formato YYYY-MM-DD) o presione Enter para mantener la actual: ")  # Obtener la nueva fecha
            metodo_pago = validar_cadena("Ingrese el nuevo método de pago: ")  # Obtener el nuevo método de pago
            rut_cliente = validar_entero("Ingrese el nuevo RUT del cliente: ")  # Obtener el nuevo RUT del cliente

            # Llama al método actualizar_factura con los nuevos valores
            try:
                Factura.actualizar_factura(conn, id_factura, id_reserva, fecha if fecha else None, metodo_pago, rut_cliente)
                print("Factura actualizada con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al intentar actualizar la factura: {e}")
                volver_menu()
        preguntar(conn)

    elif numero_tabla == 4:  # Tabla de empleados
        instancia_empleado = empleados(None, None, None, None, None, None)
        submenu()
        try:
            eleccion = int(input("\n Elige tu opción: "))
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1:  # Agregar un nuevo empleado
            rut = validar_entero("Ingrese el nuevo RUT del empleado sin puntos ni guiones: ")
            nombre = validar_cadena("Ingrese el nuevo nombre del empleado: ")
            apellido = validar_cadena("Ingrese el nuevo apellido del empleado: ")
            cargo = validar_cadena("Ingrese el nuevo cargo del empleado: ")
            horario = validar_cadena("Ingrese el nuevo horario del empleado (e.g., '9:00-17:00'): ")
            sueldo = validar_entero("Ingrese el nuevo sueldo del empleado: ")
            
            nuevo_empleado = empleados(rut, nombre, apellido, cargo, horario, sueldo)
            if not nuevo_empleado.rut_existe(conn, rut):
                try:
                    nuevo_empleado.crear_empleado(conn)
                    print(f"Empleado creado exitosamente con ID: {nuevo_empleado._id_empleado}")
                except Exception as e:  # Captura cualquier otro error que pueda ocurrir al crear
                    print(f"Ocurrió un error inesperado: {e}")
                    volver_menu()
            else:
                print(f"Error: Ya existe un empleado con el RUT {rut}.")
                volver_menu()

        elif eleccion == 2:  # Ver un empleado existente
            id_empleado = validar_entero("Ingrese el ID del empleado que desea visualizar: ")
            empleado_visto = instancia_empleado.leer_empleado(id_empleado, conn)

            if empleado_visto:
                print(f"\nDetalles del empleado con ID {id_empleado}:")
                print(f"RUT: {empleado_visto[1]}")
                print(f"Nombre: {empleado_visto[2]}")
                print(f"Apellido: {empleado_visto[3]}")
                print(f"Cargo: {empleado_visto[4]}")
                print(f"Horario: {empleado_visto[5]}")
                print(f"Sueldo: {empleado_visto[6]}")
            else:
                print(f"No se encontró ningún empleado con ID {id_empleado}.")

        elif eleccion == 3:  # Eliminar un empleado
            id_empleado = validar_entero("Ingrese el ID del empleado que desea eliminar: ")
            try:
                instancia_empleado.borrar_empleado(id_empleado, conn)
                print(f"Empleado con ID {id_empleado} eliminado con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al eliminar el empleado: {e}")
                volver_menu()

        elif eleccion == 4:  # Actualizar un empleado existente
            id_empleado = validar_entero("Ingrese el ID del empleado que desea actualizar: ")
            rut = validar_entero("Ingrese el nuevo RUT del empleado sin puntos ni guiones: ")
            nombre = validar_cadena("Ingrese el nuevo nombre del empleado: ")
            apellido = validar_cadena("Ingrese el nuevo apellido del empleado: ")
            cargo = validar_cadena("Ingrese el nuevo cargo del empleado: ")
            horario = validar_cadena("Ingrese el nuevo horario del empleado (e.g., '9:00-17:00'): ")
            sueldo = validar_entero("Ingrese el nuevo sueldo del empleado: ")

            
            try:
                empleados.actualizar_empleado(conn, id_empleado, rut, nombre, apellido, cargo, horario, sueldo)
                print(f"Empleado con ID {id_empleado} actualizado con éxito.")
            except sqlite3.IntegrityError as e:
                print("Error: Ya existe un empleado con ese ID o RUT.")
                volver_menu()
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                volver_menu()
        preguntar(conn)  # Volver al menú principal

    elif numero_tabla == 5:  # Tabla de reservación
        instancia_reservacion = reservacion(None, None, None, None, None)
        submenureserva()
        try:
            eleccion = int(input("\n Elige tu opción: ")) # pide el input
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1:  # Hacer una nueva reservación
            rutcliente = validar_entero("Ingrese el nuevo RUT del cliente sin puntos ni guiones: ")
            id_empleado = validar_entero("Ingrese el nuevo ID del empleado a cargo: ")
            fecha_inicio = validar_fecha("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = validar_fecha("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
            estado_total = validar_cadena("Ingrese el estado de la reservación (e.g., 'Confirmada', 'Pendiente'): ")

            nueva_reservacion = reservacion(rutcliente, id_empleado, fecha_inicio, fecha_fin, estado_total)
            
            try:
                id_reserva = nueva_reservacion.crear_reservacion(conn)
                print(f"Reservación creada exitosamente con ID: {id_reserva}")
            except sqlite3.Error as e:
                print(f"Error al crear la reservación: {e}")
                print("Volviendo al menú...")
                volver_menu()

        elif eleccion == 2:  # Ver una reservación existente
            id_reserva = validar_entero("Ingrese el ID de la reservación que desea visualizar: ")
            reservacion_vista = instancia_reservacion.leer_reservacion(conn, id_reserva)

            if reservacion_vista:
                print(f"\nDetalles de la reservación con ID {id_reserva}:")
                print(f"RUT Cliente: {reservacion_vista[1]}")
                print(f"ID Empleado: {reservacion_vista[2]}")
                print(f"Fecha de inicio: {reservacion_vista[3]}")
                print(f"Fecha de fin: {reservacion_vista[4]}")
                print(f"Estado: {reservacion_vista[5]}")
            else:
                print(f"No se encontró ninguna reservación con ID {id_reserva}.")

        elif eleccion == 3:  # Cancelar una reservación
            id_reserva = validar_entero("Ingrese el ID de la reservación que desea cancelar: ")
            instancia_reservacion.borrar_reservacion(conn, id_reserva)
            print(f"Reservación con ID {id_reserva} cancelada con éxito.")

        elif eleccion == 4:  # Actualizar una reservación existente
            id_reserva = validar_entero("Ingrese el ID de la reservación que desea actualizar: ")
            rutcliente = validar_entero("Ingrese el nuevo RUT del cliente sin puntos ni guiones: ")
            id_empleado = validar_entero("Ingrese el nuevo ID del empleado a cargo: ")
            fecha_inicio = validar_fecha("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = validar_fecha("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
            estado_total = validar_cadena("Ingrese el nuevo estado de la reservación (e.g., 'Confirmada', 'Pendiente'): ")
            
            try:
                reservacion.actualizar_reservacion(conn, id_reserva, rutcliente, id_empleado, fecha_inicio, fecha_fin, estado_total)

                print(f"Reservación con ID {id_reserva} actualizada con éxito.")
            except sqlite3.IntegrityError as e:
                print("Error: Cliente o empleado no existe en la base de datos.")
                volver_menu()
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                volver_menu()
        preguntar(conn)  # Volver al menú principal
        
        
    elif numero_tabla == 6:  # Tabla de detalle_factura
        instancia_detalle = DetalleFactura(None, None, None)
        submenu()

        try:
            eleccion = int(input("\n Elige tu opción: "))
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1:  # Agregar un nuevo detalle de factura
            id_factura = validar_entero("Ingrese el ID de la factura: ")
            fecha_inicio = validar_fecha("Ingrese la fecha de inicio de la reserva (YYYY-MM-DD): ")
            fecha_fin = validar_fecha("Ingrese la fecha de fin de la reserva (YYYY-MM-DD): ")

            # Cálculo de la cantidad de días
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                cantidad_dias = (fecha_fin_dt - fecha_inicio_dt).days
                if cantidad_dias <= 0:
                    print("Error: La fecha de fin debe ser posterior a la fecha de inicio.")
                    volver_menu()
            except ValueError:
                print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
                volver_menu()

            precio_diario = float(input("Ingrese el precio por día: "))
            precio_total = precio_diario * cantidad_dias
            print(f"id_factura: {id_factura}, cantidad_dias: {cantidad_dias}, precio_total: {precio_total}")


            nuevo_detalle = DetalleFactura(id_factura, cantidad_dias, precio_total)
            

            try:
                id_generado = nuevo_detalle.crear_detalle_factura(conn)
                print(f"Detalle de factura creado exitosamente con ID: {id_generado}")
            except sqlite3.IntegrityError as e: # el integrity error significa en este caso que se puso una clave foranea que no existe en la bd (en este caso, id_factura)
                print("Error de integridad: ", e)
            except sqlite3.Error as e: # el sqlite3.error captura cualquier otro error sql
                print("Error en la base de datos: ", e)
            except Exception as e: #y Exception captura errores generales del codigo, etc...
                print(f"Ocurrió un error inesperado: {e}")

        elif eleccion == 2:  # Ver un detalle de factura existente
            id_detalle_factura = int(input("Ingrese el ID del detalle de factura que desea visualizar: "))
            detalle_visto = instancia_detalle.leer_detalle_factura(conn, id_detalle_factura)

            if detalle_visto:
                print(f"\nDetalles del detalle de factura con ID {id_detalle_factura}:")
                print(f"ID Factura: {detalle_visto[1]}")
                print(f"Cantidad de días: {detalle_visto[2]}")
                print(f"Precio total: {detalle_visto[3]}")
            else:
                print(f"No se encontró ningún detalle de factura con ID {id_detalle_factura}.")

        elif eleccion == 3:  # Eliminar un detalle de factura
            id_detalle_factura = validar_entero("Ingrese el ID del detalle de factura que desea eliminar: ")
            try:
                instancia_detalle.borrar_detalle_factura(conn, id_detalle_factura)
                print(f"Detalle de factura con ID {id_detalle_factura} eliminado con éxito.")
            except Exception as e:
                print(f"Ocurrió un error al eliminar el detalle de factura: {e}")
                volver_menu()

        elif eleccion == 4:  # Actualizar un detalle de factura existente
            id_detalle_factura = validar_entero("Ingrese el ID del detalle de factura que desea actualizar: ")
            id_factura = validar_entero("Ingrese el ID de la factura: ")
            fecha_inicio = validar_fecha("Ingrese la nueva fecha de inicio de la reserva (YYYY-MM-DD): ")
            fecha_fin = validar_fecha("Ingrese la nueva fecha de fin de la reserva (YYYY-MM-DD): ")

            # Cálculo de la cantidad de días
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                cantidad_dias = (fecha_fin_dt - fecha_inicio_dt).days
                if cantidad_dias <= 0:
                    print("Error: La fecha de fin debe ser posterior a la fecha de inicio.")
                    volver_menu()
            except ValueError:
                print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")
                volver_menu()

            precio_diario = float(input("Ingrese el precio por día: "))
            precio_total = precio_diario * cantidad_dias

            detalle_actualizado = DetalleFactura(id_factura, cantidad_dias, precio_total)

            try:
                detalle_actualizado.actualizar_detalle_factura(conn, id_detalle_factura)
                print(f"Detalle de factura con ID {id_detalle_factura} actualizado con éxito.")
            except sqlite3.IntegrityError as e:
                print("Error: No se pudo actualizar el detalle de factura.")
                volver_menu()
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                volver_menu()
        preguntar(conn)  # Volver al menú principal

    elif numero_tabla == 7: #tabla habitacion
        instancia_habitacion = habitacion(None, None, None, None, None)
        submenu()

        try:
            eleccion = int(input("\n Elige tu opción: "))
        except ValueError:
            print("Valor Incorrecto")
            volver_menu()

        if eleccion == 1:  # Crear una nueva habitación
            numero_habitacion = validar_entero("Ingrese el número de la habitación: ")
            id_reserva = validar_entero("Ingrese el ID de la reservación (0 si no está reservada): ")
            tipo = validar_cadena("Ingrese el tipo de habitación: ")
            estado = validar_cadena("Ingrese el estado de la habitación (e.g., 'Disponible', 'Ocupada'): ")
            tamano = validar_cadena("Ingrese el tamaño de la habitación: ")

            nueva_habitacion = habitacion(numero_habitacion, id_reserva, tipo, estado, tamano)
            
            try:
                nueva_habitacion.crear_habitacion(conn)
                print(f"Habitación creada exitosamente con número: {numero_habitacion}")
            except sqlite3.Error as e:
                print(f"Error al crear la habitación: {e}")
                print("Volviendo al menú...")
                volver_menu()

        elif eleccion == 2:  # Ver una habitación existente
            numero_habitacion = int(input("Ingrese el número de la habitación que desea visualizar: "))
            habitacion_vista = instancia_habitacion.leer_habitacion(conn, numero_habitacion)

            if habitacion_vista:
                print(f"\nDetalles de la habitación número {numero_habitacion}:")
                print(f"ID Reserva: {habitacion_vista[1]}")
                print(f"Tipo: {habitacion_vista[2]}")
                print(f"Estado: {habitacion_vista[3]}")
                print(f"Tamaño: {habitacion_vista[4]}")
            else:
                print(f"No se encontró ninguna habitación con número {numero_habitacion}.")

        elif eleccion == 3:  # Cancelar una habitación
            numero_habitacion = int(input("Ingrese el número de la habitación que desea cancelar: "))
            instancia_habitacion.borrar_habitacion(conn, numero_habitacion)
            print(f"Habitación con número {numero_habitacion} cancelada con éxito.")

        elif eleccion == 4:  # Actualizar una habitación existente
            numero_habitacion = validar_entero("Ingrese el número de la habitación que desea actualizar: ")
            id_reserva = validar_entero("Ingrese el nuevo ID de la reservación (0 si no está reservada): ")
            tipo = validar_cadena("Ingrese el nuevo tipo de habitación: ")
            estado = validar_cadena("Ingrese el nuevo estado de la habitación (e.g., 'Disponible', 'Ocupada'): ")
            tamano = validar_cadena("Ingrese el nuevo tamaño de la habitación: ")

            habitacion_actualizada = habitacion(numero_habitacion, id_reserva, tipo, estado, tamano)
            
            try:
                habitacion_actualizada.actualizar_habitacion(conn)
                print(f"Habitación con número {numero_habitacion} actualizada con éxito.")
            except sqlite3.Error as e:
                print(f"Error al actualizar la habitación: {e}")
                volver_menu()
        preguntar(conn)  # Volver al menú principal

    else:
        print("\nElección inexistente")
        volver_menu()
menu_principal()
# Cerrar la conexión
conn.close()
