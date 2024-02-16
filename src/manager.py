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

    def get_companies_and_vacancies_count(self) -> None:
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT("Название специальности"), Работодатель FROM vacancy_data GROUP BY Работодатель
            """
            )
            rows = cur.fetchall()
            print("Кол-во | Работодатель")
            for row in rows:
                print(f"{row[0]}      | {row[1]}")
            conn.commit()
            conn.close()

    def get_all_vacancies(self, employer: str) -> None:
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM vacancy_data WHERE Работодатель='{employer}'"
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            conn.commit()
            conn.close()

    def get_avg_salary(self):
        """Функция получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """
        Функция получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.
        """
        pass


if __name__ == "__main__":
    params = config()
    db_name = "test_bd"
    mng = DBManager(params=params, db_name=db_name)
    mng.get_companies_and_vacancies_count()
    mng.get_all_vacancies("КОНАР")