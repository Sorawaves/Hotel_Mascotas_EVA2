import sqlite3

class persona:
    def __init__(self, rut, nombre, apellido):
        self._rut=rut
        self._nombre=nombre
        self._apellido=apellido

class cliente(persona):
    def __init__(self, rut, nombre, apellido, fono, mail, direccion):
        super().__init__(rut, nombre, apellido)    
        self._fono=fono
        self._mail=mail
        self._direccion=direccion

    def crear_cliente(self, conn):
        cursor = conn.cursor()
        query = '''INSERT INTO clientes (rut_cliente, nombre_cliente, apellido_cliente, fono_cliente, mail_cliente, direccion)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, (self._rut, self._nombre, self._apellido, self._fono, self._mail, self._direccion))
        conn.commit()

    @classmethod #metodo que verifica si existe ya un empleado con ese rut
    def rut_existe(cls, conn, rut):
        cursor = conn.cursor()
        query = '''SELECT * FROM clientes WHERE rut_cliente = ?'''
        cursor.execute(query, (rut,))
        return cursor.fetchone() is not None  # Retorna True si el RUT existe
    
    def leer_cliente(self, rut, conn):
        cursor = conn.cursor()
        query = '''SELECT * FROM clientes WHERE rut_cliente = ?'''
        cursor.execute(query, (rut,))
        cliente = cursor.fetchone()
        return cliente

    def actualizar_cliente(self, conn):
        cursor = conn.cursor()
        query = '''UPDATE clientes SET nombre_cliente = ?, apellido_cliente = ?, fono_cliente = ?, mail_cliente = ?, direccion = ? 
                   WHERE rut_cliente = ?'''
        cursor.execute(query, (self._nombre, self._apellido, self._fono, self._mail, self._direccion, self._rut))
        conn.commit()

    def borrar_cliente(self, rut, conn):
        cursor = conn.cursor()
        query = '''DELETE FROM clientes WHERE rut_cliente = ?'''
        cursor.execute(query, (rut,))
        conn.commit()

class empleados(persona): #agregar en la base de datos rut y apellido
    def __init__(self, rut, nombre, apellido, cargo, horario, sueldo):
        super().__init__(rut, nombre, apellido)
        self._id_empleado=None
        self._cargo=cargo
        self._horario=horario
        self._sueldo=sueldo
    
    def crear_empleado(self, conn):
        cursor = conn.cursor()
        query = '''INSERT INTO empleados (rut_empleado, nombre_empleado, apellido_empleado, cargo, horario, sueldo)
                   VALUES (?, ?, ?, ?, ?, ?)''' # ARREGLAR LOS VALORES DE LA TABLA EMPLEADO CON ESTOS NOMBRES
        cursor.execute(query, (self._rut, self._nombre, self._apellido, self._cargo, self._horario, self._sueldo))
        conn.commit()
        self._id_empleado = cursor.lastrowid
        return self._id_empleado
    
    @classmethod #metodo que verifica si existe ya un empleado con ese rut
    def rut_existe(cls, conn, rut):
        cursor = conn.cursor()
        query = '''SELECT * FROM empleados WHERE rut_empleado = ?'''
        cursor.execute(query, (rut,))
        return cursor.fetchone() is not None  # Retorna True si el RUT existe

    def leer_empleado(self, id_empleado, conn):
        cursor = conn.cursor()
        query = '''SELECT * FROM empleados WHERE id_empleado = ?'''
        cursor.execute(query, (id_empleado,))
        empleado = cursor.fetchone()
        return empleado

    def actualizar_empleados(self, conn):
        cursor = conn.cursor()
        query = '''UPDATE empleados SET nombre_empleado = ?, apellido_empleado = ?, cargo = ?, horario = ?, sueldo = ? 
                   WHERE id_empleado = ?'''
        cursor.execute(query, (self._nombre, self._apellido, self._cargo, self._horario, self._sueldo, self._id_empleado))
        conn.commit()
    @classmethod
    def actualizar_empleado(cls, conn, id_empleado, rut, nombre, apellido, cargo, horario, sueldo):
        cursor = conn.cursor()
        query = '''UPDATE empleados SET rut_empleado = ?, nombre_empleado = ?, apellido_empleado = ?, cargo = ?, horario = ?, sueldo = ? 
                WHERE id_empleado = ?'''
        cursor.execute(query, (rut, nombre, apellido, cargo, horario, sueldo, id_empleado))
        conn.commit()


    def borrar_empleado(self, id_empleado, conn):
        cursor = conn.cursor()
        query = '''DELETE FROM empleados WHERE id_empleado = ?'''
        cursor.execute(query, (id_empleado,))
        conn.commit()
    
    