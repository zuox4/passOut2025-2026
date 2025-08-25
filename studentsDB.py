import mysql.connector
from mysql.connector import Error


def get_class_from_db(class_name):
    connection = mysql.connector.connect(
        host='192.168.20.61',  # адрес сервера
        database='students',  # имя базы данных
        user='pass_system',  # имя пользователя
        password='ktSXPOr2ekCGS4cr'  # пароль
    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from students WHERE className='{class_name}' AND archive=0")
        record = cursor.fetchall()
        data = [{'name': i[3]+' '+i[2], 'className': i[5]} for i in record]
        for i in data:
            print(i)
        cursor.close()
        return data
    return None
