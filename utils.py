from bs4 import BeautifulSoup
import requests


def get_replace(item: str):
    # replace special characters and more;)
    rep_dict = {
        "\u202f": "",
        "\u2009": "",
        "грн": "",
        "'": "`",
    }
    for i, j in rep_dict.items():
        item = item.replace(i, j)
    return item


def remove_duplicate(my_list: list) -> str:
    # remove duplicates when parsing
    set_list = []
    for item in my_list:
        if item not in set_list:
            set_list.append(item)
    set_list = ''.join(i + '--' for i in set_list)
    return set_list


def get_company_name(card_table):
    try:
        company_name = card_table.find_all('a')[1].find('b').get_text(strip=True)
        # change the single quote to a backtick and special characters
        company_name = get_replace(company_name).strip()
    except AttributeError:
        company_name = "no data available"
    return company_name


def get_salary(card_table):
    try:
        salary = card_table.find('b', class_="text-black").get_text(strip=True)
        # remove special characters
        salary = get_replace(salary).strip()
    except AttributeError:
        salary = "no data available"
    return salary


def get_description(card_table):
    try:
        job_description = card_table.find('div', id='job-description').find_all(['p', 'b', 'li'])
        description = [resp.get_text(strip=True) for resp in job_description]
        # remove duplicates when parsing
        description = remove_duplicate(description)
        # change the single quote to a backtick and special characters
        description = get_replace(description).strip()
    except AttributeError:
        description = "no data available"
    return description


def get_responsibilities(card_table):
    try:
        responsibilities_list = card_table.find('ol').find_all('li')
        responsibilities = [resp.get_text(strip=True) for resp in responsibilities_list]
        # remove duplicates when parsing
        responsibilities = remove_duplicate(responsibilities)
        # change the single quote to a backtick and special characters
        responsibilities = get_replace(responsibilities)
    except AttributeError:
        responsibilities = "no data available"
    return responsibilities


def get_detail_vacancy(root_url: str, job_card_link: str, headers: dict) -> dict:
    # select additional information about the vacancy

    response = requests.get(root_url+job_card_link, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    job_card_table = soup.find('div', class_='card wordwrap')

    salary = get_salary(job_card_table)
    company_link = job_card_table.find('a')['href']
    company_id = ''.join(id_ for id_ in company_link if id_.isdigit())
    company_name = get_company_name(job_card_table)
    description = get_description(job_card_table)
    responsibilities = get_responsibilities(job_card_table)

    detail_vacancy = {
        'salary': salary,
        'company_link': company_link,
        'company_name': company_name,
        'company_id': company_id,
        'job_description': description,
        'responsibilities': responsibilities,
    }

    return detail_vacancy
