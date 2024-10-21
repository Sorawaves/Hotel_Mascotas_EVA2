import sqlite3

class habitacion:
    def __init__(self, numero_habitacion, id_reserva, tipo, estado, tamano):

        self.__numero_habitacion=numero_habitacion
        self.__id_reserva=id_reserva
        self.__tipo=tipo
        self.__estado=estado
        self.__tamano=tamano



    # Método para crear una nueva habitación
    def crear_habitacion(self, conn):
        cursor = conn.cursor()
        query = '''INSERT INTO habitacion (num_habitacion, id_reserva, tipo, estado, tamano)
                   VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(query, (self.__numero_habitacion, self.__id_reserva, self.__tipo, self.__estado, self.__tamano))
        conn.commit()

    # Método para leer una habitación por su número
    def leer_habitacion(self, conn, numero_habitacion):
        cursor = conn.cursor()
        query = '''SELECT * FROM habitacion WHERE num_habitacion = ?'''
        cursor.execute(query, (numero_habitacion,))
        habitacion = cursor.fetchone()
        return habitacion

    # Método para actualizar los detalles de una habitación
    def actualizar_habitacion(self, conn):
        cursor = conn.cursor()
        query = '''UPDATE habitacion 
                   SET id_reserva = ?, tipo = ?, estado = ?, tamano = ?
                   WHERE num_habitacion = ?'''
        cursor.execute(query, (self.__id_reserva, self.__tipo, self.__estado, self.__tamano, self.__numero_habitacion))
        conn.commit()

    # Método para borrar una habitación
    def borrar_habitacion(self, conn, numero_habitacion):
        cursor = conn.cursor()
        query = '''DELETE FROM habitacion WHERE num_habitacion = ?'''
        cursor.execute(query, (numero_habitacion,))
        conn.commit()
