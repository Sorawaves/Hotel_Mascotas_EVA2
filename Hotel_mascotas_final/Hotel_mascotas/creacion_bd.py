import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('hotelm.db')
cursor = conn.cursor()

# Ejecutar múltiples sentencias SQL usando executescript()
cursor.executescript('''

    
    CREATE TABLE clientes 
(
    rut_cliente INT NOT NULL, 
    nombre_cliente VARCHAR(15), 
    apellido_cliente VARCHAR(20),
    fono_cliente INT, 
    mail_cliente VARCHAR(30),
    direccion VARCHAR(30),
    PRIMARY KEY (rut_cliente)
);

CREATE TABLE mascotas 
(
    id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
    rut_cliente INT NOT NULL, 
    nombre_mascota VARCHAR(20), 
    tipo VARCHAR(15), 
    edad INT,
    historial_medico VARCHAR(40), 
    tamano VARCHAR(10), 
    
    FOREIGN KEY (rut_cliente) REFERENCES clientes(rut_cliente)
);

CREATE TABLE factura 
(
    id_factura INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_reserva INT NOT NULL, 
    fecha DATE, 
    metodo_pago VARCHAR(12), 
    rut_cliente INT NOT NULL,
    FOREIGN KEY (rut_cliente) REFERENCES clientes(rut_cliente),
    FOREIGN KEY (id_reserva) REFERENCES reservacion(id_reserva)
);

CREATE TABLE empleados 
(
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT, 
    rut_empleado INT NOT NULL, 
    nombre_empleado VARCHAR(15), 
    apellido_empleado VARCHAR(20), 
    cargo VARCHAR(20), 
    horario VARCHAR(12), 
    sueldo INT
);

CREATE TABLE reservacion 
(
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT, 
    rut_cliente INT NOT NULL, 
    id_empleado INT NOT NULL,
    fecha_inicio DATE, 
    fecha_fin DATE, 
    estado_total VARCHAR(15),
    FOREIGN KEY (rut_cliente) REFERENCES clientes(rut_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);

CREATE TABLE detalle_factura 
(
    id_detalle_factura INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_factura INT NOT NULL,
    cantidad INT NOT NULL,    
    precio_total INT NOT NULL,
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
    
);

CREATE TABLE habitacion 
(
    num_habitacion INT NOT NULL, 
    id_reserva INT NOT NULL, 
    tipo VARCHAR(15),
    estado VARCHAR(13), 
    tamano VARCHAR(10), 
    FOREIGN KEY (id_reserva) REFERENCES reservacion(id_reserva),
    PRIMARY KEY (num_habitacion)
);

''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()
