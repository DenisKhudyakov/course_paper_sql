from src.get_api_data import HeadHunterAPI
from src.config import config
from src.utils import ConnectBD
from src.manager import DBManager


def main() -> None:
    """Функция взаимодействия с пользователем"""
    params = config()
    db_name = "test_bd"
    specialization = input('Введите название специальности ')
    data = HeadHunterAPI(0, specialization, '1384')
    data = data.new_structure()
    new_data = ConnectBD(params=params, data_base=data, db_name='test_bd')
    new_data.create_database()
    new_data.upload_dataframe()
    mng = DBManager(params=params, db_name=db_name)
    mng.get_companies_and_vacancies_count()
    employer = input('Введите название работодателя ')
    mng.get_all_vacancies(employer)
    mng.get_avg_salary()
    key_word = input('Введите ключевое слово для запроса ')
    mng.get_vacancies_with_keyword(key_word)


if __name__ == "__main__":
    main()
