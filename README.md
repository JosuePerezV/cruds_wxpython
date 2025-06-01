# Sistema POS HEB

Este proyecto es un sistema de punto de venta completo desarrollado en **Python** con **wxPython** y **MySQL**.

## 🚀 Requisitos

- Python 3.11 o superior
- MySQL Server
- Módulos de Python (ver `requirements.txt`)

## 📦 Instalación

1. Clona o descarga este repositorio.
2. Ejecuta el script SQL en MySQL Workbench o consola:
   ```
   crear_bd_sistema_ventas.sql
   ```
3. Instala los módulos requeridos:
   ```
   pip install -r requirements.txt
   ```
4. Ejecuta el sistema:
   ```
   python main.py
   ```

## ✅ Funcionalidades

- Login de usuarios
- Menú lateral moderno
- CRUD de Clientes, Empleados, Categorías, Proveedores, Productos, Membresías y Usuarios
- Escaneo de productos por código de barras con cámara
- Generación de tickets PDF
- Control de stock y carrito
- Registro de ventas y detalle

## 📁 Estructura
```
main.py
main_lateral.py
venta_pos.py
conexion.py
crud_*.py
codigos_barras/
crear_bd_sistema_ventas.sql
requirements.txt
.gitignore
```

## 👤 Acceso de prueba
- Usuario: admin
- Contraseña: admin123

