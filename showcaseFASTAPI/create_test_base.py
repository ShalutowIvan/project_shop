import psycopg2
from src.settings_t.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

#файл для созднания тестовой базы

try:
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
 
    conn.autocommit = True
    # команда для создания базы данных metanit
    sql = f"CREATE DATABASE {DB_NAME}"
 
    # выполняем код sql
    cursor.execute(sql)
    print("База данных успешно создана")
    cursor.close()
    conn.close()
    
except Exception as ex:
    print("Ошибка создания тестовой базы !!!!!!!!!!!")
    print("111", ex)

    