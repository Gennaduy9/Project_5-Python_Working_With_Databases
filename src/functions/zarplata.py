import json

import requests

from src.abc.job_api import WorkAPI


class ZarpLATAAPI(WorkAPI):
    """
    Класс для работы с API zarplata.ru.
    """

    def get_vacancies(self):
        """
        Этот метод отправляет запрос к API Zarplata.ru с указанными параметрами
        (ключевое слово, город, индекс страницы и количество вакансий).
        Он получает ответные данные в формате JSON и возвращает их.
        """

        name_value = "name:" + self.text
        params = {
            'text': name_value, # Текст фильтра.
            'area': 1, # Поиск осуществляется по вакансиям города Москва
            'page': 0, # Индекс страницы поиска на zarplata.ru
            'per_page': self.count # Кол-во вакансий.
        }
        req = requests.get('https://api.zarplata.ru/vacancies', params) # Посылаем запрос к API
        data = json.loads(req.content.decode())
        req.close()
        return data

    def vacancies_for_user(self):
        """
        Этот метод вызывает метод get_vacancies для получения данных о вакансиях.
        Затем он перебирает элементы в ответных данных и извлекает соответствующие поля,
        такие как название работы, URL, оплата, требования и название работодателя.
        Он создает список словарей, представляющих каждую вакансию, и возвращает его.
        """
        vacancies_ZP = []
        data = self.get_vacancies()
        for i in data['items']:
            if i['salary']:
                if i['salary']['from']:
                    vacancies_ZP.append(dict(name=i['name'], url=i['alternate_url'], payment=i['salary']['from'],
                                             requirements=i['snippet']['requirement'], employer=i['employer']['name']))
                else:
                    vacancies_ZP.append(dict(name=i['name'], url=i['alternate_url'], payment=0,
                                             requirements=i['snippet']['requirement'], employer=i['employer']['name']))
            else:
                vacancies_ZP.append(dict(name=i['name'], url=i['alternate_url'], payment=0,
                                         requirements=i['snippet']['requirement'], employer=i['employer']['name']))
        return vacancies_ZP