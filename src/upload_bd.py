from src.config import config
from typing import Any
from src.get_api_data import HeadHunterAPI
from src.connect_bd import Connect


class UploadBD:
    """Класс отправки"""

    @staticmethod
    def upload(any_data: list, cur: Any) -> None:
        """Отправка данных"""
        for one_vacancy in any_data:
            cur.execute(
                f"""
                INSERT INTO vacancy_data (specialty, salary_from, salary_to, employer) 
                VALUES(%s, %s, %s, %s)
                """,
                (
                    one_vacancy["Название специальности"],
                    one_vacancy["Зарплата от"],
                    one_vacancy["Зарплата до"],
                    one_vacancy["Работодатель"],
                ),
            )

    @staticmethod
    def create_table(cur: Any) -> None:
        """Создание таблицы вакансий"""
        cur.execute(
            f"""
            CREATE TABLE vacancy_data (
            specialty VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            employer VARCHAR(255) NOT NULL
            )
            """
        )


if __name__ == "__main__":
    params = config()
    db_name = "test_bd2"
    up = UploadBD()
    data = HeadHunterAPI(0, "снабжение", "1384")
    data = data.new_structure()
    with Connect(params=params, db_name=db_name) as con:
        with con.cursor() as cur:
            up.create_table(cur=cur)
            up.upload(any_data=data, cur=cur)
