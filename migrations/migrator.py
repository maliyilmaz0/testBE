from os.path import isfile
from psycopg2 import connect
import os

select_mode = input("Create One Table: (yes / no)")
current_path = os.getcwd()
db_name = "tarot_project"
queries_path = f"{current_path}/DB_QUERIES"
username = "root"
password = "root"
all_tables_query = """SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'"""


def terminate_all_connections(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid();")
    connection.commit()
    cursor.close()
    connection.close()


def create_one_table(queries_path, file_name, exist_tables):
    with open(f"{queries_path}/{file_name}") as f:
        try:
            if str(os.path.splitext(file_name)[0]).lower() not in exist_tables:
                print(f"==={file_name}===")
                query = f.read()
                result = cursor_obj.execute(query)
                con.commit()
                print(f"SUCCESS | {file_name} | {result}")
        except Exception as e:
            error_message = f"File Name: [{file_name}] | error: {e}"
            print(error_message.rstrip("\n"))
            con.rollback()


def create_tables(queries_path, exist_tables):
    for file_name in os.listdir(queries_path):
        full_path = os.path.join(queries_path, file_name)
        name, extension = os.path.splitext(file_name)
        if os.path.isfile(full_path) and extension == '.sql':
            with open(full_path) as f:
                try:
                    if str(name).lower() not in exist_tables:
                        print(f"==={file_name}===")
                        query = f.read()
                        result = cursor_obj.execute(query)
                        con.commit()
                        print(f"SUCCESS | {file_name} | {result}")
                except Exception as e:
                    print(f"File Name: [{file_name}] | error: {e}")
                    con.rollback()
                    continue


def get_all_tables():
    cursor_obj.execute(all_tables_query)
    table_names = []
    for table_name in cursor_obj.fetchall():
        print(f"Table Name: {table_name}")
        table_names.append(table_name[0])
    print("----------------------------------------------------")
    return table_names


try:
    con = connect(
        database=db_name,
        user=username,
        password=password,
        host="localhost",
        port='5432'
    )

    cursor_obj = con.cursor()
    if select_mode == 'yes' or select_mode == 'YES':
        file_name = input('File name: ')
        create_one_table(queries_path, file_name, get_all_tables())
    else:
        create_tables(queries_path, get_all_tables())
    terminate_all_connections(con)
    cursor_obj.close()
    con.close()

    # result = cursor_obj.execute(query)
    # print(result)
except Exception as e:
    print("err", e)
