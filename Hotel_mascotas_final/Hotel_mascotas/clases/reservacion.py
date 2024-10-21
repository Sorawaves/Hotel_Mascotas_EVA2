import sqlite3

class reservacion:
    def __init__(self,rutcliente, id_empleado, fecha_inicio, fecha_fin, estado_total):
        self.__id_reserva = None
        self.__rutcliente=rutcliente
        self.__id_empleado=id_empleado
        self.__fecha_inicio=fecha_inicio
        self.__fecha_fin=fecha_fin
        self.__estado_total=estado_total 

     # Método para crear una nueva reservación
    def crear_reservacion(self, conn):
        cursor = conn.cursor()
        query = '''INSERT INTO reservacion (rut_cliente, id_empleado, fecha_inicio, fecha_fin, estado_total)
                   VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(query, (self.__rutcliente, self.__id_empleado, self.__fecha_inicio, self.__fecha_fin, self.__estado_total))
        conn.commit()
        self.id_reserva = cursor.lastrowid
        return self.id_reserva

    # Método para leer una reservación por su ID
    def leer_reservacion(self, conn, id_reserva):
        cursor = conn.cursor()
        query = '''SELECT * FROM reservacion WHERE id_reserva = ?'''
        cursor.execute(query, (id_reserva,))
        reservacion = cursor.fetchone()
        return reservacion

    # Método para actualizar una reservación existente
    def actualizar_reservacions(self, conn):
        cursor = conn.cursor()
        query = '''UPDATE reservacion 
                   SET rut_cliente = ?, id_empleado = ?, fecha_inicio = ?, fecha_fin = ?, estado_total = ?
                   WHERE id_reserva = ?'''
        cursor.execute(query, (self.__rutcliente, self.__id_empleado, self.__fecha_inicio, self.__fecha_fin, self.__estado_total, self.id_reserva))
        conn.commit()
    @classmethod
    def actualizar_reservacion(cls, conn, id_reserva, rut_cliente, id_empleado, fecha_inicio, fecha_fin, estado_total):
        cursor = conn.cursor()
        query = '''UPDATE reservacion 
                   SET rut_cliente = ?, id_empleado = ?, fecha_inicio = ?, fecha_fin = ?, estado_total = ?
                   WHERE id_reserva = ?'''
        cursor.execute(query, (rut_cliente, id_empleado, fecha_inicio, fecha_fin, estado_total, id_reserva))
        conn.commit()

    # Método para borrar una reservación
    def borrar_reservacion(self, conn, id_reserva):
        cursor = conn.cursor()
        query = '''DELETE FROM reservacion WHERE id_reserva = ?'''
        cursor.execute(query, (id_reserva,))
        conn.commit()