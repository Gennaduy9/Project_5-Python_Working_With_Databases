import os

import json
import psycopg2

from src.creat_db import DBCreat
from src.secret import host, user, password, db_name


class DBManager(DBCreat):
    """Класс DBManager, который будет подключаться к БД Postgres"""

    def __init__(self):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        self.conn.autocommit = True

    def create_tables(self):
        """Создание таблиц"""
        query_1 = """
        CREATE TABLE IF NOT EXISTS Employers (
        employer_id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL)"""

        query_2 = """
        CREATE TABLE IF NOT EXISTS Vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        employer_id INTEGER REFERENCES Employers (employer_id),
        title VARCHAR NOT NULL,
        description VARCHAR,
        salary INTEGER,
        url VARCHAR)"""

        for query in [query_1, query_2]:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()

    def fill_tables_from_files(self, file_path):
        """Заполнение таблиц с помощью файлов с вакансиями."""

        if os.path.exists(f"src/data_json_employers/{file_path}.json"):
            with open(file_path, 'r', encoding="utf-8") as file:

                data = json.load(file)

                for vacancy in data["items"]:

                    if vacancy["salary"] is not None and vacancy["salary"]["from"] is not None:
                        salary = vacancy["salary"]["from"]
                    else:
                        salary = 1

                    if len(vacancy["apply_alternate_url"]) != 0:
                        url = vacancy["apply_alternate_url"]
                    else:
                        url = ""

                    if len(vacancy["employer"]["name"]) != 0:
                        name_company = vacancy["employer"]["name"]
                    else:
                        name_company = ""

                    if len(vacancy["name"]) != 0:
                        name_vacancy = vacancy["name"]
                    else:
                        name_vacancy = ""

                    if vacancy["snippet"]["requirement"] is not None:
                        vacancy_desc_1 = vacancy["snippet"]["requirement"]
                    else:
                        vacancy_desc_1 = ""

                    if vacancy["snippet"]["responsibility"] is not None:
                        vacancy_desc_2 = vacancy["snippet"]["responsibility"]
                    else:
                        vacancy_desc_2 = ""

                    description = f"{vacancy_desc_1} {vacancy_desc_2}"

                    with self.conn.cursor() as cursor:
                        cursor.execute("""
                        INSERT INTO Employers (name)
                        SELECT %s
                        WHERE NOT EXISTS (
                        SELECT name
                        FROM Employers
                        WHERE name = %s)
                        """, (name_company, name_company))

                        self.conn.commit()

                        cursor.execute("SELECT employer_id FROM Employers ORDER BY employer_id DESC LIMIT 1")
                        employer_id = cursor.fetchone()[0]

                        cursor.execute("""INSERT INTO vacancies (employer_id, title, description, salary, url)
                        VALUES (%s, %s, %s, %s, %s)""", [employer_id, name_vacancy, description, salary, url])

                        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT employers.name, COUNT(vacancies.vacancy_id) AS vacancy_count
        FROM employers
        LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
        GROUP BY employers.name
        ORDER BY employers.name
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию."""
        query = """
        SELECT employers.name, vacancies.title, vacancies.salary, vacancies.url
        FROM employers
        INNER JOIN vacancies ON employers.employer_id = vacancies.employer_id
        ORDER BY employers.name, vacancies.title
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary) FROM Vacancies"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            avg_salary = cursor.fetchone()[0]

        if avg_salary is not None:
            return avg_salary
        else:
            return 0

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        print("Average Salary:", avg_salary)  # Проверка значения средней зарплаты
        query = f"SELECT * FROM vacancies WHERE salary > {avg_salary}"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        query = f"SELECT * FROM vacancies WHERE description ILIKE '%{keyword}%'"

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results

    def close_conn(self):
        self.conn.close()