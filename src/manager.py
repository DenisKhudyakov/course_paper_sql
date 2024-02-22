from abc import ABC, abstractmethod

import psycopg2

from src.config import config
from src.connect_bd import Connect
from typing import Any


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

    @staticmethod
    def get_companies_and_vacancies_count(cur: Any) -> None:
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        cur.execute(
            """
            SELECT COUNT("specialty"), employer FROM vacancy_data GROUP BY employer
        """
        )
        rows = cur.fetchall()
        print("Кол-во | Работодатель")
        for row in rows:
            print(f"{row[0]}      | {row[1]}")

    @staticmethod
    def get_all_vacancies(employer: str, cur) -> None:
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        cur.execute(f"SELECT * FROM vacancy_data WHERE employer='{employer}'")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    @staticmethod
    def get_avg_salary(cur: Any):
        """Функция получает среднюю зарплату по вакансиям."""
        cur.execute(
            """SELECT AVG("salary_from"), AVG("salary_to") FROM vacancy_data"""
        )
        rows = cur.fetchall()
        for row in rows:
            print(
                f"Средняя зарплата от: {row[0]}, средняя зарплата до: {row[1]}"
            )

    @staticmethod
    def get_vacancies_with_higher_salary(cur: Any) -> None:
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cur.execute(
            """SELECT * FROM vacancy_data WHERE "salary_from" > (SELECT AVG("salary_from") FROM vacancy_data);"""
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)

    @staticmethod
    def get_vacancies_with_keyword(cur: Any, word: str) -> None:
        """
        Функция получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.
        :param word: str
        :return: None
        """
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
    mng = DBManager()
    with Connect(params=params, db_name=db_name) as con:
        with con.cursor() as cur:
            mng.get_companies_and_vacancies_count(cur)
            mng.get_all_vacancies("КОНАР", cur)
            mng.get_avg_salary(cur)
            mng.get_vacancies_with_keyword(cur, "менеджер")
