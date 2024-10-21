import sqlite3

class mascota:
    def __init__(self, rut_cliente, nombre_mascota, tipo, edad, historial_medico, tamano):

        self._id_mascota=None
        self._rut_cliente=rut_cliente
        self._nombre_mascota=nombre_mascota
        self._tipo=tipo
        self._edad=edad
        self._historial_medico=historial_medico
        self._tamano=tamano
    
    def higiene(self):
        raise NotImplementedError("Se debe implementar en cada clase")
    
    def crear_mascota(self, conn):
        cursor = conn.cursor()
        query = '''INSERT INTO mascotas (rut_cliente, nombre_mascota, tipo, edad, historial_medico, tamano)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, (self._rut_cliente, self._nombre_mascota, self._tipo, self._edad, self._historial_medico, self._tamano))
        conn.commit()
        self._id_mascota = cursor.lastrowid  # Obtener el ID generado
        print (self._id_mascota)
    
    @classmethod
    def leer_mascota(cls, id_mascota, conn):
        cursor = conn.cursor()
        query = '''SELECT * FROM mascotas WHERE id_mascota = ?'''
        cursor.execute(query, (id_mascota,))
        data = cursor.fetchone()

        if data is not None:
            print(f"\n rut_cliente: {data[0]} \n nombre de la mascota: {data[1]}\n tipo de animal: {data[2]}\n edad: {data[3]}\n historial médico: {data[4]}\n tamaño: {data[5]}\n id de la mascota: {data[6]} ")
            return None  # Crear una instancia de Mascota o su subclase
        else:
            print(f"No se encontró una mascota con el ID {id_mascota}")
            return None

    
    @classmethod
    def actualizar_mascota(cls, conn, id_mascota, rut_cliente, nombre_mascota, tipo, edad, historial_medico, tamano):
        cursor = conn.cursor()
        query = '''UPDATE mascotas SET rut_cliente = ?, nombre_mascota = ?, tipo = ?, edad = ?, historial_medico = ?, tamano = ?
                   WHERE id_mascota = ?'''
        cursor.execute(query, (rut_cliente, nombre_mascota, tipo, edad, historial_medico, tamano, id_mascota))
        conn.commit()
    
    
    @classmethod
    def borrar_mascota(cls, id_mascota, conn):
        cursor = conn.cursor()
        query = '''DELETE FROM mascotas WHERE id_mascota = ?'''
        cursor.execute(query, (id_mascota,))
        conn.commit()

   
class Perro(mascota):
    def higiene(self):
        return f"{self._nombre_mascota} Necesita baño y cepillado de pelaje"

class Gato(mascota):
    def higiene(self):
        return f"{self._nombre_mascota} Necesita limpieza de almohadillas, orejas y cepillado de pelaje."


