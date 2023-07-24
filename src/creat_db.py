import psycopg2

from src.config import config


def create_database() -> None:
    """Создает новую базу данных. Закрывает сеанс """
    db_name = 'db_job_parser'
    params = config()
    conn = None
    conn = psycopg2.connect(dbname='postgres', **params)

    conn.autocommit = True

    cur = conn.cursor()

    with conn.cursor() as cursor:
        cursor.execute("""
           SELECT pg_terminate_backend(pg_stat_activity.pid)
           FROM pg_stat_activity
           WHERE pg_stat_activity.datname = 'db_job_parser'
           AND pid <> pg_backend_pid();
           """)

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")

    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                url VARCHAR(255),
                payment INTEGER,
                requirements TEXT,
                company_title VARCHAR(255)
                )
                """)
    conn.commit()
    conn.close()


def save_data_to_database(data):
    db_name = 'db_job_parser'
    params = config()
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        for i in data:
            cur.execute("""
                INSERT INTO vacancies (title, url, payment, requirements, company_title)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                        (i['name'], i['url'], i['payment'], i['requirements'], i['employer'])
                        )
    conn.commit()
    conn.close()