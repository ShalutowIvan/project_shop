import psycopg2
from tests.settings import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST, MODE

#файл для созднания тестовой базы

try:
    conn = psycopg2.connect(dbname="postgres", user=DB_USER_TEST, password=DB_PASS_TEST, host=DB_HOST_TEST, port=DB_PORT_TEST)
    cursor = conn.cursor()
 
    conn.autocommit = True
    # команда для создания базы данных
    sql = f"CREATE DATABASE {DB_NAME_TEST}"
 
    # выполняем код sql
    cursor.execute(sql)
    print("База данных успешно создана")
    cursor.close()
    conn.close()
    
except Exception as ex:
    print("Ошибка создания тестовой базы !!!!!!!!!!!")
    print("ОШИБКА ТУТ:", ex)

    