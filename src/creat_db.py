import psycopg2

from src.config import config
from src.secret import db_name


class DBCreat:
    """Класс создаёт новую базу данных"""

    db_name = 'headhunter'

    params = config()
    conn = None

    def __init__(self):
        self.conn = psycopg2.connect(
            host=self.params['host'],
            user=self.params['user'],
            password=self.params['password'],

        )

        self.conn.autocommit = True

        cur = self.conn.cursor()
        # Проверяем активные подключения к базе данных
        cur.execute(
            f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
            f"FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{db_name}' "
            f"AND pid <> pg_backend_pid();"
        )

        # Удаляем базу данных
        cur.execute(f"DROP DATABASE IF EXISTS {db_name};")

        # Создаем новую базу данных
        cur.execute(f"CREATE DATABASE {db_name};")

        cur.close()