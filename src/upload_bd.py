from src.connect_bd import Connect
from src.config import config
from src.get_api_data import HeadHunterAPI


class UploadBD:
    """Класс отправки"""

    def __init__(self, params: dict, db_name: str) -> None:
        """конструктор класса UploadBD"""
        self.params = params
        self.db_name = db_name

    def upload(self, any_data: list) -> None:
        """Отправка данных"""
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                for one_vacancy in any_data:
                    cur.execute(
                        f"""
                        INSERT INTO vacancy_data (specialty, salary_from, salary_to, employer) 
                        VALUES(%s, %s, %s, %s)
                        """,
                        (one_vacancy['Название специальности'], one_vacancy['Зарплата от'], one_vacancy['Зарплата до'],
                         one_vacancy['Работодатель'])
                    )

    def create_table(self) -> None:
        """Создание таблицы вакансий"""
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                            CREATE TABLE vacancy_data (
                                specialty VARCHAR(255) NOT NULL,
                                salary_from INTEGER,
                                salary_to INTEGER,
                                employer VARCHAR(255) NOT NULL
                            )
                        """)


if __name__ == '__main__':
    params = config()
    db_name = "test_bd2"
    up = UploadBD(params=params, db_name=db_name)
    data = HeadHunterAPI(0, 'снабжение', '1384')
    data = data.new_structure()
    up.create_table()
    up.upload(any_data=data)
