from bs4 import BeautifulSoup
import requests
from utils import get_detail_vacancy, get_replace
from save_to import TxtWriter, CSVWriter, DbWriter, JsonWriter


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit 537.36'
                         '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
           }
HOST = "https://www.work.ua"
PATH = "/ru/jobs/"
FULL_URL = HOST + PATH

result = []
page = 0

writers_list = [
    TxtWriter(),
    JsonWriter(),
    CSVWriter(),
    DbWriter(),
]

while True:
    page += 1

    # if page == 10:
    #     break
    # print(f'Page: {page}')

    PARAMS = {
        'ss': 1,
        'page': page,
        }

    response = requests.get(FULL_URL, headers=HEADERS, params=PARAMS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs_table = soup.find('div', id='pjax-job-list')

    if jobs_table is None:
        break

    jobs_cards = jobs_table.find_all('div', class_='card card-hover card-visited wordwrap job-link js-hot-block')

    for job in jobs_cards:
        vacancy_link = job.find('a')['href']
        vacancy_id = ''.join(id_ for id_ in vacancy_link if id_.isdigit())
        vacancy = get_replace(job.find('a').text)
        detail_vacancy = get_detail_vacancy(HOST, vacancy_link, HEADERS)

        vacancy_info = {
            'vacancy_link': vacancy_link,
            'vacancy_id': vacancy_id,
            'vacancy': vacancy,
            'salary': detail_vacancy['salary'],
            'company_link': detail_vacancy['company_link'],
            'company_name': detail_vacancy['company_name'],
            'company_id': detail_vacancy['company_id'],
            'job_description': detail_vacancy['job_description'],
            'responsibilities': detail_vacancy['responsibilities'],
        }
        result.append(vacancy_info)

for writer in writers_list:
    writer.write(result)
    # writer.write(vacancy_info)
