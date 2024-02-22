from src.config import config
from src.get_api_data import HeadHunterAPI
from src.manager import DBManager
from src.upload_bd import UploadBD
from src.connect_bd import Connect


def main() -> None:
    """Функция взаимодействия с пользователем"""
    params = config()
    db_name = "test_bd2"
    specialization = input("Введите название специальности ")
    data = HeadHunterAPI(0, specialization, "1384")
    data = data.new_structure()
    upload = UploadBD()
    mng = DBManager()
    with Connect(params=params, db_name=db_name) as con:
        with con.cursor() as cur:
            upload.create_table(cur=cur)
            upload.upload(any_data=data, cur=cur)
            mng.get_companies_and_vacancies_count(cur)
            employer = input("Введите название работодателя ")
            mng.get_all_vacancies(cur=cur, employer=employer)
            mng.get_avg_salary(cur)
            key_word = input("Введите ключевое слово для запроса ")
            mng.get_vacancies_with_keyword(cur, key_word)


if __name__ == "__main__":
    main()
