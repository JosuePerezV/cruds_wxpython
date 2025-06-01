
CREATE DATABASE sistema_ventas;
USE sistema_ventas;

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS producto (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10,2),
    stock INT,
    caducidad DATE,
    categoria VARCHAR(100),
    inventario VARCHAR(100),
    codigo_barras VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS cliente (
    idcliente INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    telefono VARCHAR(15),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS empleado (
    idempleado INT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    direccion TEXT,
    telefono VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS proveedor (
    idproveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(15),
    direccion TEXT
);

CREATE TABLE IF NOT EXISTS membresia (
    id_tarjeta VARCHAR(20) PRIMARY KEY,
    puntos INT,
    fecha_emision DATE,
    fecha_expiracion DATE
);

CREATE TABLE IF NOT EXISTS venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    idcliente INT NOT NULL,
    id_empleado INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    FOREIGN KEY (idcliente) REFERENCES cliente(idcliente),
    FOREIGN KEY (id_empleado) REFERENCES empleado(idempleado)
);

CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT,
    cantidad INT,
    producto_codigo VARCHAR(20),
    precio_unitario DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (producto_codigo) REFERENCES producto(codigo)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleado(idempleado)
);

