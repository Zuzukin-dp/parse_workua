import csv
import json
import sqlite3


class TxtWriter:
    def __init__(self):
        self.file = open('./data/results.txt', 'w')

    def write(self, items: list):
        for item in items:
            self.file.write(f"{item}\n")


class JsonWriter:
    def __init__(self):
        self.file = open('./data/results.json', 'w', encoding='utf-8')

    def write(self, item: list):
        json.dump(item, self.file, ensure_ascii=False, indent=4)
        self.file.write(f"\n")


class CSVWriter:
    def __init__(self):
        self._file = open('./data/results.csv', 'w')
        self.writer = csv.writer(self._file, delimiter=";")

    def write(self, items: list):
        self.writer.writerow(list(items[0].keys()))

        for item in items:
            self.writer.writerow(list(item.values()))


class DbWriter:

    def __init__(self):
        self.connect = sqlite3.connect('./data/workua.db')
        self.cursor = self.connect.cursor()

    def write(self, items: list):
        self.connect.execute(
            """
                CREATE TABLE IF NOT EXISTS workua_vacancy (
                id INTEGER PRIMARY KEY,
                vacancy_link text,
                vacancy_id int,
                vacancy varchar(50),
                salary varchar(50),
                company_link varchar(50),
                company_name varchar(200),
                company_id int,
                job_description varchar(2500),
                responsibilities varchar(1500));
            """
        )

        for item in items:
            previous_vacancy = self.connect.execute(
                f"""
                    SELECT vacancy_id FROM workua_vacancy WHERE vacancy_id = '{item['vacancy_id']}'
                """).fetchone()

            if previous_vacancy is None or int(item['vacancy_id']) != previous_vacancy[0]:
                self.connect.execute(
                    f"""
                        INSERT INTO workua_vacancy (
                        vacancy_link,
                        vacancy_id,
                        vacancy,
                        salary,
                        company_link,
                        company_name,
                        company_id,
                        job_description,
                        responsibilities)
                        VALUES (
                        '{item['vacancy_link']}',
                        '{item['vacancy_id']}',
                        '{item['vacancy']}',
                        '{item['salary']}',
                        '{item['company_link']}',
                        '{item['company_name']}',
                        '{item['company_id']}',
                        '{item['job_description']}',
                        '{item['responsibilities']}');
                    """
                )
        self.connect.commit()
