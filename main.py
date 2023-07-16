import os

from src.creat_db import DBCreat
from src.db_manager import DBManager
from src.headhunter_api import HeadHunter
from src.secret import db_name

if __name__ == "__main__":
    db_creat = DBCreat()
    if db_creat.conn is not None:
        print(f"БД {db_name} успешно создана")
    else:
        print(f"БД {db_name} не создана")
    db_manager = DBManager()
    if db_manager.conn is not None:
        print("Соединение с базой данных установлено успешно")
    else:
        print("Ошибка при установлении соединения с базой данных")
    db_manager.create_tables()

    hh = HeadHunter('your_api_key')
    hh.get_json_files()
    db_manager.fill_tables_from_files(["file.json"])

    if db_manager.conn is not None:
        print("Файлы json в папке data_json_employers успешно заполнены")
    else:
        print("Ошибка при заполнении файлов json в папке data_json_employers")

    i = 1

    for file in os.listdir("src/data_json_employers"):
        db_manager.fill_tables_from_files([file])
        print(file, "ОК", i)
        i += 1

    print()
    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary(), "Средняя зарплата")
    for row in db_manager.get_vacancies_with_higher_salary():
        print(row)

    print()
    print(db_manager.get_vacancies_with_keyword("python"))

    db_manager.close_conn()


