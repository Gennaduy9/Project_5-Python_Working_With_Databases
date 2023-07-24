import json

import requests

from src.abc.job_api import WorkAPI


class HeadHunterAPI(WorkAPI):
    """
    Класс для работы с API HeadHunter.
    """

    def get_vacancies(self):
        """
        Получает вакансии с сайта по ключевому слову и указанному количеству.
        :return: Список словарей с информацией о вакансиях.
        """
        name_value = "name:" + self.text
        params = {
            'text': name_value, # Текст фильтра.
            'area': 1, # Поиск осуществляется по вакансиям города Москва.
            'page': 0, # Индекс страницы поиска на HH.
            'per_page': self.count # Кол-во вакансий.
        }
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = json.loads(req.content.decode())
        req.close()
        return data

    def vacancies_for_user(self):
        """
        Преобразует полученные данные в список словарей с определенными полями.
        :return: Список словарей с информацией о вакансиях.
        """
        vacancies_HH = []
        data = self.get_vacancies()
        for i in data['items']:
            if i['salary']:
                if i['salary']['from']:
                    vacancies_HH.append(dict(name=i['name'], url=i['alternate_url'], payment=i['salary']['from'],
                                       requirements=i['snippet']['requirement'], employer=i['employer']['name']))
                else:
                    vacancies_HH.append(dict(name=i['name'], url=i['alternate_url'], payment=0,
                                             requirements=i['snippet']['requirement'], employer=i['employer']['name']))
            else:
                vacancies_HH.append(dict(name=i['name'], url=i['alternate_url'], payment=0,
                                       requirements=i['snippet']['requirement'], employer=i['employer']['name']))
        return vacancies_HH