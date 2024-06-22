import pyodbc
import sqlite3
from abc import ABC, abstractmethod
import asyncio


class DBHelper(ABC):
    connection: any
    cursor: any

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    async def shut_down_connection(self):
        try:
            await asyncio.to_thread(self.cursor.close)
            await asyncio.to_thread(self.connection.close)
        except Exception as e:
            raise e

    async def execute_query(self, query, params=None):
        try:
            await asyncio.to_thread(self.cursor.execute, query, params)

        except Exception as e:
            await asyncio.to_thread(self.connection.rollback)
            raise e

    async def commit(self):
        await asyncio.to_thread(self.connection.commit)

    async def fetch_all(self):
        return await asyncio.to_thread(self.cursor.fetchall)

    async def fetch_one(self):
        return await asyncio.to_thread(self.cursor.fetchone)


class PostgreHelper(DBHelper):

    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)


class MysqlHelper(DBHelper):

    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    def connect(self):
        pass


class SqlLiteHelper(DBHelper):

    def __init__(self, db_path):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        super().__init__(connection, cursor)

    def connect(self):
        pass

    def close_connection(self):
        pass


class SQLServerHelper(DBHelper):
    def __init__(self, db_name, username, password, server):
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={db_name};UID={username};PWD={password}"
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        super().__init__(connection, cursor)

    def connect(self):
        pass

    def close_connection(self):
        pass

    pass
