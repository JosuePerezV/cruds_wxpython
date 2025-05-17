# CRUDs con wxPython y MySQL

Este proyecto contiene 7 interfaces CRUD desarrolladas en Python con wxPython, conectadas a una base de datos MySQL.

## Tablas de catálogo

- Categoría
- Producto
- Cliente
- Empleado
- Proveedor
- Membresía
- Detalle de venta

## Requisitos

- Python 3.x
- wxPython
- mysql-connector-python
- MySQL instalado y funcionando

## Instalación de dependencias

```bash
pip install wxPython mysql-connector-python
```

## Base de datos

La base de datos se llama `sistema_ventas`. Ejecuta el archivo `crear_bd_sistema_ventas.sql` en MySQL Workbench o consola para crear todas las tablas necesarias.

## Cómo ejecutar

Ejecuta cualquier CRUD así:

```bash
python crud_cliente_wxpython.py
```

## Conexión

La conexión a la base de datos se realiza desde el archivo `conexion.py`. Asegúrate de tener configurado correctamente el host, usuario, contraseña y nombre de la base.

## Autor

Ivan Pérez – 4° semestre de Ingeniería en Sistemas Computacionales
