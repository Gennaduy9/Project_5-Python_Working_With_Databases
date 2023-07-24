import psycopg2

from config import config


class DBManager:
    db_name = 'db_job_parser'
    params = config()
    avg_vacancies = 0

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании!
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT company_title, COUNT(*)
                        FROM vacancies
                        GROUP BY company_title 
                        """)
            for row in cur:
                print(row)
        conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company_title, title, payment, url
                FROM vacancies
                """)
            for row in cur:
                print(row)
        conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT AVG(payment)
                        FROM vacancies
                        """)
            for row in cur:
                self.avg_vacancies = int(row[0])
        conn.close()
        return self.avg_vacancies

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE payment > {self.get_avg_salary()}")
            for row in cur:
                print(row)
        conn.close()

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в требованиях которых содержатся переданные в метод слова!"""
        search_word = input('Введите слово для поиска в требованиях:   ')

        conn = psycopg2.connect(dbname=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM vacancies WHERE requirements LIKE '%{search_word}%'")
            for row in cur:
                print(row)
        conn.close()