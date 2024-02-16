from abc import ABC, abstractmethod
import psycopg2


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

    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self):
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE channels (
                    channel_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    views INTEGER,
                    subscribers INTEGER,
                    videos INTEGER,
                    channel_url TEXT
                )
            """
            )
            conn.commit()
            conn.close()
        pass

    def get_all_vacancies(self):
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        pass

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
