import pandas as pd
import psycopg2
from typing import Any
from src.get_api_data import HeadHunterAPI
from src.config import config
from sqlalchemy import create_engine

class ConnectBD:
    """Данный класс преобразует входные данные в DataFrame и отправляет их на БД PostgresSQL"""

    def __init__(self, params: dict):
        self.params = params

    def create_database(self, db_name: str) -> None:
        """Создает новую базу данных."""
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")

        conn.close()

    def create_data_frame(self, data_base: list[dict[str: Any]]):
        """Создаем дата фрейм с данными, которые получаем от модуля get_api_data"""
        return pd.DataFrame(data_base)


    def upload_dataframe(self):
        # Ниже только пример
        engine = create_engine('postgresql://postgres:279211@localhost:5432/north')
        df1 = pd.read_csv(config.EMPLOYEES)
        df1.to_sql('employees_data', engine)



if __name__ == '__main__':
    data = HeadHunterAPI(0, 'снабжение', '1384')
    data = data.new_structure()
    params = config()
    new_data = ConnectBD(params)
    print(new_data.create_data_frame(data))