from abc import ABC, abstractmethod
import psycopg2
from src.config import config


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
        self.conn = psycopg2.connect(dbname=self.db_name, **self.params)

    def get_companies_and_vacancies_count(self) -> None:
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT("Название специальности"), Работодатель FROM vacancy_data GROUP BY Работодатель
            """
            )
            rows = cur.fetchall()
            print("Кол-во | Работодатель")
            for row in rows:
                print(f"{row[0]}      | {row[1]}")
            self.conn.commit()

    def get_all_vacancies(self, employer: str) -> None:
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM vacancy_data WHERE Работодатель='{employer}'"
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            self.conn.commit()

    def get_avg_salary(self):
        """Функция получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """SELECT AVG("Зарплата от"), AVG("Зарплата до") FROM vacancy_data"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(f'Средняя зарплата от: {row[0]}, средняя зарплата до: {row[1]}')
            self.conn.commit()

    def get_vacancies_with_higher_salary(self) -> None:
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM vacancy_data WHERE "Зарплата от" > (SELECT AVG("Зарплата от") FROM vacancy_data);"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            self.conn.commit()

    def get_vacancies_with_keyword(self, word: str) -> None:
        """
        Функция получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.
        :param word: str
        :return: None
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM vacancy_data WHERE "Название специальности" ILIKE '%{word}%';""".format(word=word)
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            self.conn.commit()



if __name__ == "__main__":
    params = config()
    db_name = "test_bd"
    mng = DBManager(params=params, db_name=db_name)
    mng.get_companies_and_vacancies_count()
    mng.get_all_vacancies("КОНАР")
    mng.get_avg_salary()
    mng.get_vacancies_with_keyword('менеджер')