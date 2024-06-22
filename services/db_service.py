from psycopg2 import sql
from utilities.helpers.db_connector_helper import DBHelper


class DBService:
    def __init__(self, db_helper: DBHelper, table_name: str):
        self.db_helper = db_helper
        self.__table_name = table_name

    async def get_data_by_id(self, id):
        try:
            query = sql.SQL("SELECT * FROM {} WHERE id = %s".format(sql.Identifier(self.__table_name).string))
            await self.db_helper.execute_query(query, (id,))
            result = await self.db_helper.fetch_one()
            result_data = dict(result.items())
            return result_data
        except Exception as e:
            raise e

    async def delete_data(self, id: str):
        try:
            query = sql.SQL("DELETE FROM {} WHERE id = %s".format(sql.Identifier(self.__table_name).string))
            await self.db_helper.execute_query(query, (id,))
            await self.db_helper.commit()
        except Exception as e:
            raise e

    async def get_data_by_query(self, conditions: {}, params, conjunction="AND", aritmetic_operator="="):
        try:
            final_params = ()
            if len(conditions) == 1:
                key, value = list(conditions.items())[0]
                condition_str = "{} {} %s".format(sql.Identifier(key).string, aritmetic_operator)
            else:
                condition_str = " {} ".format(conjunction).join(
                    ["{} = %s".format(sql.Identifier(key).string) for key in conditions.keys()])
            final_query = sql.SQL("""SELECT {} FROM {} WHERE {}""".format(
                '*',
                sql.Identifier(self.__table_name).string,
                condition_str
            ))

            if params is not None:
                final_params = list(conditions.values()) + params
            else:
                final_params = list(conditions.values())
            await self.db_helper.execute_query(final_query, final_params)
            result = await self.db_helper.fetch_all()
            result_list = [dict(row.items()) for row in result]
            return result_list
        except Exception as e:
            raise e

    async def get_all(self):
        try:
            query = sql.SQL("SELECT {} FROM {}".format(
                "*",
                sql.Identifier(self.__table_name).string
            ))
            await self.db_helper.execute_query(query, None)
            result = await self.db_helper.fetch_all()
            result_list = [dict(row.items()) for row in result]
            return result_list
        except Exception as e:
            raise e

    async def get_pagination(self, page_number: int, page_size: int):
        try:
            offset = (page_number - 1) * page_size
            query = sql.SQL("SELECT * FROM {} LIMIT %s OFFSET %s").format(
                sql.Identifier(self.__table_name)
            )
            count_query = sql.SQL("SELECT COUNT(*) FROM {}").format(
                sql.Identifier(self.__table_name)
            )

            # Verileri çek
            await self.db_helper.execute_query(query, (page_size, offset))
            result = await self.db_helper.fetch_all()
            result_list = [dict(row.items()) for row in result]
            # Toplam kayıt sayısını al
            await self.db_helper.execute_query(count_query)
            total_rows = self.db_helper.fetch_one()[0]

            return {"data": result_list, "total_count": total_rows}
        except Exception as e:
            raise e

    async def insert_data(self, data):
        try:
            columns = sql.SQL(", ").join(sql.Identifier(col) for col in data.keys())
            values_placeholder = sql.SQL(", ").join(sql.Placeholder() for _ in data.values())
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(self.__table_name),
                columns,
                values_placeholder
            )

            params = list(data.values())
            await self.db_helper.execute_query(query, params)
            await self.db_helper.commit()
            return data
        except Exception as e:
            raise e

    async def update_data(self, id, data):
        try:
            set_clause = ', '.join(f"{column} = %s" for column in data.keys())
            query = f"UPDATE {sql.Identifier(self.__table_name).string} SET {set_clause} WHERE id = %s"
            params = [*data.values(), id]
            await self.db_helper.execute_query(query, params)
            await self.db_helper.commit()
            return data
        except Exception as e:
            raise e

    async def close(self):
        await self.db_helper.shut_down_connection()
