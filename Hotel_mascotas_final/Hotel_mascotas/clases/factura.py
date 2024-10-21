import sqlite3
from datetime import datetime

class Factura:
    def __init__(self, id_factura, id_reserva, fecha, metodo_pago, rut_cliente):
        self.__id_factura = id_factura
        self.__id_reserva = id_reserva        
        self.__fecha = fecha
        self.__metodo_pago = metodo_pago
        self.__rut_cliente = rut_cliente

    @classmethod
    def crear_factura(cls, conn, id_reserva, metodo_pago, rut_cliente):
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        query = '''INSERT INTO factura (id_reserva, fecha, metodo_pago, rut_cliente) 
                   VALUES (?, ?, ?, ?)'''
        cursor.execute(query, (id_reserva, fecha_actual, metodo_pago, rut_cliente))
        conn.commit()
        #devuelve el id de la factura recien creada
        id_factura = cursor.lastrowid
        return id_factura


    @classmethod
    def leer_factura(cls, conn, id_factura):
        cursor = conn.cursor()
        query = '''SELECT * FROM factura WHERE id_factura = ?'''
        cursor.execute(query, (id_factura,))
        factura = cursor.fetchone()
        return factura

    @classmethod
    def actualizar_factura(cls, conn, id_factura, id_reserva, fecha, metodo_pago, rut_cliente):
        cursor = conn.cursor()
        query = '''
            UPDATE factura 
            SET id_reserva = ?, fecha = ?, metodo_pago = ?, rut_cliente = ?
            WHERE id_factura = ?
        '''
        cursor.execute(query, (id_reserva, fecha, metodo_pago, rut_cliente, id_factura))
        conn.commit()

    @classmethod
    def borrar_factura(cls, conn, id_factura):
        cursor = conn.cursor()
        query = '''DELETE FROM factura WHERE id_factura = ?'''
        cursor.execute(query, (id_factura,))
        conn.commit()