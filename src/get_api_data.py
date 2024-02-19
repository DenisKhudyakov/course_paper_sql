from copy import copy

import requests


class HeadHunterAPI:
    """Класс работы с API hh.ru"""

    url: str = "https://api.hh.ru/vacancies"
    vacancy_list: list = []
    new_struct: dict = {
        "Название специальности": None,
        "Зарплата от": None,
        "Зарплата до": None,
        "Работодатель": None,
    }

    def __init__(self, page: int, name: str, region: str):
        """конструктор класса HeadHunterAPI, инициализируется URL-адресом"""
        self.page = page
        self.name = name
        self.region = region
        param = {
            "page": self.page,
            "per_page": 100,
            "text": f"NAME:{self.name}",
            "area": self.region,
        }
        self.response = requests.get(self.url, params=param)

    def get_data_vacancy(self):
        """Функция, которая получает данные по вакансиям в формате json"""
        return self.response.json()["items"]

    def new_structure(self):
        """Преобразование ответа от API под предпочитаемую структуру"""
        for i_job in self.get_data_vacancy():
            try:
                new_struct = copy(self.new_struct)
                new_struct["Название специальности"] = i_job["name"]
                new_struct["Зарплата от"] = i_job["salary"]["from"]
                new_struct["Зарплата до"] = i_job["salary"]["to"]
                new_struct["Работодатель"] = i_job["employer"]["name"]
                self.vacancy_list.append(new_struct)
            except TypeError:
                continue
        return self.vacancy_list


if __name__ == "__main__":
    data = HeadHunterAPI(0, "снабжение", "1384")
    for i in data.new_structure():
        print(i)
