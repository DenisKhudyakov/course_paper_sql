import psycopg2


class Connect:
    """Класс для подключения к БД и отправки данных"""

    def __init__(self, params: dict, db_name: str):
        """Конструктор класса ConnectAndUploadBD"""
        self.params = params
        self.db_name = db_name
        try:
            self.conn = psycopg2.connect(dbname=self.db_name, **self.params)
        except psycopg2.OperationalError:
            self.conn = psycopg2.connect(**self.params)
            self.conn.autocommit = True
            cursor = self.conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cursor.execute(f"CREATE DATABASE {self.db_name}")

    def __enter__(self):
        """Подключение к БД"""
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """закрытие БД"""
        try:
            self.conn.commit()
            self.conn.close()
        except TypeError("У объекта нет атрибута close()") as e:
            print(e)
            return True
