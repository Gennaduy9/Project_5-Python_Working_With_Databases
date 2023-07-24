import json

import requests

from src.abc.job_api import WorkAPI


class SuperJobAPI(WorkAPI):
    """
    Класс для работы с API SuperJob.
    """
    def get_vacancies(self):
        """
        Получает вакансии с сайта SuperJob по ключевому слову и указанному количеству.
        :return: Возвращает список словарей с информацией о вакансиях.
        """
        url_str = f'https://api.superjob.ru/2.0/vacancies/?keyword={self.text}&t=4&count={self.count}/'
        req = requests.get(url_str, headers={"X-Api-App-Id": 'v3.r.137586941.f8b5c1d6c7ceb995c050acb9474a789e4ab49761.8cab32a4e53a3040d3f44b75eb5336b86fe9a2a3'})
        data = json.loads(req.content.decode())
        req.close()
        return data

    def vacancies_for_user(self):
        """
        Преобразует полученные данные в список словарей с определенными полями: название вакансии, ссылка на вакансию,
        зарплата, требования и название работодателя.
        :return:  Возвращает список словарей с информацией о вакансиях.
        """
        vacancies_SJ = []
        data = self.get_vacancies()
        for i in data['objects']:
            vacancies_SJ.append(dict(name=i['profession'], url=i['link'], payment=i['payment_from'],
                                       requirements=i['candidat'], employer=i['firm_name']))
        return vacancies_SJ