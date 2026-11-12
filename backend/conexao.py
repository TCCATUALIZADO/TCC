import os
import mysql.connector

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "trabalho")

try:
    banco = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = banco.cursor()
    print(f"[OK] Conectado com sucesso ao MySQL em '{DB_HOST}' (Banco: '{DB_NAME}')!")
    cursor.close()
    banco.close()
except Exception as erro:
    print(f"[ERRO] Falha ao conectar ao MySQL: {erro}")
