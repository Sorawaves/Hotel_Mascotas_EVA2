import sqlite3

class DetalleFactura:
    def __init__(self, id_factura, cantidad, precio_total):
        self.__id_detalle_factura = None
        self.__id_factura = id_factura        
        self.__cantidad = cantidad
        self.__precio_total = precio_total

    # Método para crear un nuevo detalle de factura
    def crear_detalle_factura(self, conn):
        cursor = conn.cursor()
        query = '''INSERT INTO detalle_factura (id_factura, cantidad, precio_total)
                   VALUES (?, ?, ?)'''
        cursor.execute(query, (self.__id_factura,  self.__cantidad, self.__precio_total))
        conn.commit()
        id_detalle_factura = cursor.lastrowid
        return id_detalle_factura

    # Método para leer un detalle de factura
    def leer_detalle_factura(self, conn, __id_factura):
        cursor = conn.cursor()
        query = '''SELECT * FROM detalle_factura WHERE id_factura = ?'''
        cursor.execute(query, (__id_factura,))
        detalle_factura = cursor.fetchone()  
        return detalle_factura

    # Método para actualizar un detalle de factura
    def actualizar_detalle_factura(self, conn, id_detalle_factura):
        cursor = conn.cursor()
        query = '''UPDATE detalle_factura 
                   SET id_factura = ?, cantidad = ?, precio_total = ?
                   WHERE id_detalle_factura = ?'''
        cursor.execute(query, (self.__id_factura, self.__cantidad, self.__precio_total, id_detalle_factura))
        conn.commit()

    # Método para borrar un detalle de factura
    def borrar_detalle_factura(self, conn, __id_detalle_factura):
        cursor = conn.cursor()
        query = '''DELETE FROM detalle_factura WHERE id_detalle_factura = ?'''
        cursor.execute(query, (__id_detalle_factura,))
        conn.commit()
