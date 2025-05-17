-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS sistema_ventas;
USE sistema_ventas;

-- Tabla: categoria
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla: producto
CREATE TABLE IF NOT EXISTS producto (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10,2),
    stock INT,
    caducidad DATE,
    categoria VARCHAR(100),
    inventario VARCHAR(100)
);

-- Tabla: cliente
CREATE TABLE IF NOT EXISTS cliente (
    idcliente INT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    telefono VARCHAR(15),
    email VARCHAR(100)
);

-- Tabla: empleado
CREATE TABLE IF NOT EXISTS empleado (
    idempleado INT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    direccion TEXT,
    telefono VARCHAR(15)
);

-- Tabla: proveedor
CREATE TABLE IF NOT EXISTS proveedor (
    idproveedor INT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(15),
    direccion TEXT
);

-- Tabla: membresia
CREATE TABLE IF NOT EXISTS membresia (
    id_tarjeta VARCHAR(20) PRIMARY KEY,
    puntos INT,
    fecha_emision DATE,
    fecha_expiracion DATE
);

-- Tabla: detalle_venta
CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle INT PRIMARY KEY,
    id_venta INT,
    cantidad INT,
    producto_codigo VARCHAR(20)
);
