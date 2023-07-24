
from src.functions.HH_API import HeadHunterAPI
from src.functions.JobJSONFile import SuperJobAPI
from src.functions.zarplata import ZarpLATAAPI


def get_api_vacancies(platform, word):
    count_vac = 100   # Количество вакансий с платформы

    if platform == 1:
        vacancies_all = HeadHunterAPI(word, count_vac).vacancies_for_user()
        print(f'Найдено {len(vacancies_all)} вакансий с платформы Head Hunter')
    elif platform == 2:
        vacancies_all = SuperJobAPI(word, count_vac).vacancies_for_user()
        print(f'Найдено {len(vacancies_all)} вакансий с платформы Super Job')
    elif platform == 3:
        vacancies_all = ZarpLATAAPI(word, count_vac).vacancies_for_user()
        print(f'Найдено {len(vacancies_all)} вакансий с платформ Zarplata')
    elif platform == 4:
        vacancies_all = HeadHunterAPI(word, count_vac).vacancies_for_user() + \
                        SuperJobAPI(word, count_vac).vacancies_for_user() + \
                        ZarpLATAAPI(word, count_vac).vacancies_for_user()
        print(f'Найдено {len(vacancies_all)} вакансий с платформ Super Job, Head Hunter, Zarplata')
    else:
        print('Такой платформы нет, попробуйте снова')
        exit()

    return vacancies_all


