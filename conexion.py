import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="AL1ZzSqL8712$",
        database="sistema_ventas"
    )
