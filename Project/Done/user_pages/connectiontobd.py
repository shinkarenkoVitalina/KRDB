import hashlib
from psycopg2 import Error
import psycopg2
from psycopg2 import OperationalError
import datetime

def ExecuteQuery(query):
    try:
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="testdone")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")

def ExecuteReadQuery(query):
    try:
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="testdone")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")


# def create_connection(db_name, db_user, db_password, db_host, db_port):
#     connection = None
#     try:
#         connection = psycopg2.connect(
#             database=db_name,
#             user=db_user,
#             password=db_password,
#             host=db_host,
#             port=db_port,
#         )
#         print("Connection to PostgreSQL DB successful")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#     return connection
#
#
# def execute_query(connection, query):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Query executed successfully")
#
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#
# def execute_read_query(connection, query):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()


# ---

# passw = "pass1"
# hpass = hashlib.md5(passw.encode())
# print(hpass)
# pass1 = hpass.hexdigest()
# print(pass1)
# query1 = f"INSERT INTO Пользователь VALUES ('User1', 'mail1@gmail.com', '{pass1}')"
# passw = "pass2"
# hpass = hashlib.md5(passw.encode())
# pass2 = hpass.hexdigest()
# query2 = f"INSERT INTO Пользователь VALUES ('User2', 'mail2@gmail.com', '{pass2}')"
# passw = "pass3"
# hpass = hashlib.md5(passw.encode())
# pass3 = hpass.hexdigest()
# query3 = f"INSERT INTO Пользователь VALUES ('User3', 'mail3@gmail.com', '{pass3}')"
# passw = "pass4"
# hpass = hashlib.md5(passw.encode())
# pass4 = hpass.hexdigest()
# query4 = f"INSERT INTO Пользователь VALUES ('User4', 'mail4@gmail.com', '{pass4}')"
# execute_query(connection,query1)
# execute_query(connection,query2)
# execute_query(connection,query3)
# execute_query(connection,query4)


# query = "SELECT * FROM Пользователь"
# temp = execute_read_query(connection, query)
# print(temp)


# date1 = datetime.datetime.now()
# query1 = f"INSERT INTO Рабочее_пространство VALUES ('name1','desc1','{date1}','mail1@gmail.com')"
# query2 = f"INSERT INTO Рабочее_пространство VALUES ('name2','desc2','{date1}','mail1@gmail.com')"
# query3 = f"INSERT INTO Рабочее_пространство VALUES ('name3','desc3','{date1}','mail1@gmail.com')"
# execute_query(connection,query1)
# execute_query(connection,query2)
# execute_query(connection,query3)

# query = "SELECT * FROM Рабочее_пространство"
# res = execute_read_query(connection, query)
# print(res)
#
# query = "SELECT * FROM Доска"
# res = execute_read_query(connection, query)
# print(res)

