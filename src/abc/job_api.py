from abc import ABC, abstractmethod


class WorkAPI(ABC):
    def __init__(self, text: str, count: int):
        """
        Инициализация объекта WorkAPI.
        :param text: Текст.
        :param count: Количество.
        """
        self.text = text
        self.count = count

    @abstractmethod
    def get_vacancies(self):
        """
        Получение вакансий.
        """
        pass

    @abstractmethod
    def vacancies_for_user(self):
        """
         Получение вакансий для пользователя.
        """
        pass

