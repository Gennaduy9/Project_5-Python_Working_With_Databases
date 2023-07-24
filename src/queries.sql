--создание таблицы
CREATE TABLE vacancies(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                url VARCHAR(255),
                payment INTEGER,
                requirements TEXT,
                company_title VARCHAR(255)
                )

--заполнение таблицы
INSERT INTO vacancies (title, url, payment, requirements, company_title)
VALUES (%s, %s, %s, %s, %s)

--Получает список всех компаний и количество вакансий у каждой компании
SELECT company_title, COUNT(*)
FROM vacancies
GROUP BY company_title

--Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT company_title, title, payment, url
FROM vacancies

--Получает среднюю зарплату по вакансиям
SELECT AVG(payment)
FROM vacancies

--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT * FROM vacancies WHERE payment > {self.get_avg_salary()}

--Получает список всех вакансий, в требованиях которых содержатся переданные в метод слова
SELECT * FROM vacancies WHERE requirements LIKE '%{search_word}%'