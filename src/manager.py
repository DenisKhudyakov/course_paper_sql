from abc import ABC, abstractmethod

import psycopg2

from src.config import config
from src.connect_bd import Connect


class AbstractManager(ABC):
    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass


class DBManager(AbstractManager):
    """Класс управления базой данных"""

    def __init__(self, params: dict, db_name: str):
        self.params = params
        self.db_name = db_name

    def get_companies_and_vacancies_count(self) -> None:
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT("specialty"), employer FROM vacancy_data GROUP BY employer
                """
                )
                rows = cur.fetchall()
                print("Кол-во | Работодатель")
                for row in rows:
                    print(f"{row[0]}      | {row[1]}")

    def get_all_vacancies(self, employer: str) -> None:
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancy_data WHERE employer='{employer}'")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_avg_salary(self):
        """Функция получает среднюю зарплату по вакансиям."""
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT AVG("salary_from"), AVG("salary_to") FROM vacancy_data"""
                )
                rows = cur.fetchall()
                for row in rows:
                    print(
                        f"Средняя зарплата от: {row[0]}, средняя зарплата до: {row[1]}"
                    )

    def get_vacancies_with_higher_salary(self) -> None:
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT * FROM vacancy_data WHERE "salary_from" > (SELECT AVG("salary_from") FROM vacancy_data);"""
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_vacancies_with_keyword(self, word: str) -> None:
        """
        Функция получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.
        :param word: str
        :return: None
        """
        with Connect(params=self.params, db_name=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT * FROM vacancy_data WHERE "specialty" ILIKE '%{word}%';""".format(
                        word=word
                    )
                )
                rows = cur.fetchall()
                for row in rows:
                    print(row)


if __name__ == "__main__":
    params = config()
    db_name = "test_bd2"
    mng = DBManager(params=params, db_name=db_name)
    mng.get_companies_and_vacancies_count()
    mng.get_all_vacancies("КОНАР")
    mng.get_avg_salary()
    mng.get_vacancies_with_keyword("менеджер")
