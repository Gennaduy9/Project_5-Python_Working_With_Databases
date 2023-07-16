import os

import psycopg2
import requests
import json


class HeadHunter:
    """Класс для работы с платформой HeadHunter"""

    _api_link = "https://api.hh.ru/vacancies"

    @staticmethod
    def _get_session():
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        return session

    def __init__(self, api_key):
        self.session = HeadHunter._get_session()
        self._params = {'apikey': api_key}

    def get_vacancies_api(self, **kwargs):
        """
        Метод get_vacancies_api() выполняет GET-запрос к API для получения данных о вакансиях
        с использованием переданных параметров поиска.
        :param kwargs: Именованные аргументы для параметров поиска в формате "ключ-значение".
        :return: None (Если имеется ошибка, тогда возвращается пустой словарь {})
        """

        params = {}

        for key, value in kwargs.items():
            params[key] = value

        response = self.session.get(self._api_link, params=params)

        if response.status_code == 200:
            data = response.text
            data_dict = json.loads(data)
            return data_dict
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return {}

    def get_json_files(self):
        """Сохранение файлов 10 компаний."""
        for one_id in [1122462, 15478, 80, 78638, 1308904, 6, 5947075, 3529, 4181, 1429999]:
            if os.path.exists(f"src/data_json_employers/{one_id}.json"):
                with open(f"src/data_json_employers/{one_id}.json", 'w', encoding="utf-8") as file:
                    json.dump(self.get_vacancies_api(employer_id=one_id, per_page=100),
                              file, indent=2, ensure_ascii=False)