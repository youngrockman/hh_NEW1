import sqlite3
def save_to_sqlite(vacancies_data, db_name="vacancies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            name TEXT,
            area TEXT,
            salary_from REAL,
            salary_to REAL,
            salary_currency TEXT,
            url TEXT
        )
    ''')

    # Вставка данных
    for vacancy in vacancies_data['items']:
        salary = vacancy.get('salary')
        cursor.execute('''
            INSERT INTO vacancies (name, area, salary_from, salary_to, salary_currency, url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            vacancy['name'],
            vacancy['area']['name'],
            salary.get('from') if salary else None,
            salary.get('to') if salary else None,
            salary.get('currency') if salary else None,
            vacancy['alternate_url']
        ))

    conn.commit()
    conn.close()