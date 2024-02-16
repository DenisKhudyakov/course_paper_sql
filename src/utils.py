import pandas as pd
import psycopg2
from typing import Any
from src.get_api_data import HeadHunterAPI
from src.config import config
from sqlalchemy import create_engine


class ConnectBD:
    """Данный класс преобразует входные данные в DataFrame и отправляет их на БД PostgresSQL"""

    def __init__(self, params: dict, db_name: str, data_base: list[dict[str: Any]]):
        self.params = params
        self.db_name = db_name
        self.data_base = data_base

    def create_database(self) -> None:
        """Создает новую базу данных."""
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        cursor.execute(f"CREATE DATABASE {self.db_name}")
        conn.close()

    @staticmethod
    def create_data_frame(data_base: list[dict[str: Any]]) -> pd.DataFrame:
        """Создаем дата фрейм с данными, которые получаем от модуля get_api_data"""
        return pd.DataFrame(data_base)

    def upload_dataframe(self) -> None:
        """Функция, которая отправляет дата фрейм в PostgreSQL"""
        engine = create_engine(
            f'postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.db_name}'
        )
        conn = engine.connect()
        df = self.create_data_frame(self.data_base)
        df.to_sql('vacancy_data', con=conn, if_exists='replace', index=False)
        conn.close()


if __name__ == '__main__':
    data = HeadHunterAPI(0, 'снабжение', '1384')
    data = data.new_structure()
    params = config()
    new_data = ConnectBD(params=params, data_base=data, db_name='test_bd')
    new_data.create_database()
    new_data.upload_dataframe()
