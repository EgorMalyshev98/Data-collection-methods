import requests
from bs4 import BeautifulSoup
import transliterate
from pymongo import MongoClient
from pymongo import errors
import re


def hh_scraper(job_title: str):

    def salary_parse(salary: str):

        salary = salary.replace(' ', '')
        min_sal, max_sal = None, None

        if salary.find(' – ') != -1:
            min_sal, max_sal = re.findall(r'\d+', salary)
            min_sal, max_sal = int(min_sal), int(max_sal)
        elif salary.find('от') != -1:
            min_sal = re.findall(r'\d+', salary)
            min_sal = int(min_sal[0])
        elif salary.find('до') != -1:
            max_sal = re.findall(r'\d+', salary)
            max_sal = int(max_sal[0])

        valute = re.findall(r'\D+', salary)[-1].lstrip()

        return min_sal, max_sal, valute

    def coll_name_translit(title: str):

        title = transliterate.translit(title, reversed=True)
        title = ''.join(re.findall(r'\w+', title.replace(' ', '_').lower()))
        return title

    url = 'https://hh.ru/search/vacancy'
    params = {'text': job_title, 'from': 'suggest_post', 'salary': '', 'clusters': 'true', 'ored_clusters': 'true',
              'enable_snippets': 'true',
              'items_on_page': '20',
              'only_with_salary': 'true'}
    session = requests.Session()

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/61.0.3163.100 Safari/537.36'}

    response = session.get(url, headers=headers, params=params)
    print('status code:', response.status_code)

    if response.status_code == 200:

        dom = BeautifulSoup(response.text, 'html.parser')
        try:
            last_page = dom.find('a', {'class': 'bloko-button', 'data-qa': 'pager-next'}).previous_sibling \
                .find_next().find_next().find_next().text
        except AttributeError:
            return print('Попробуйте ввести другой запрос')

        client = MongoClient('127.0.0.1', 27017)
        db = client['user10']
        collection_name = coll_name_translit(job_title)

        try:
            db.create_collection(collection_name)
        except errors.CollectionInvalid:
            pass

        collection = db.get_collection(collection_name)
        added_rows = 0

        for page in range(int(last_page)):
            print('page number:', page)
            params['page'] = page
            response = session.get(url, headers=headers, params=params)
            dom = BeautifulSoup(response.text, 'html.parser')

            salaries = dom.find_all('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancies = dom.find_all('a', {'data-qa': 'vacancy-serp__vacancy-title'})

            for vac, sal in zip(vacancies, salaries):

                # data = {'vacancy': None, 'salary_min': None, 'salary_max': None, 'valute': None, 'href': None}

                data = {'vacancy': vac.text, 'salary_min': (salary_parse(sal.text))[0],
                        'salary_max': (salary_parse(sal.text))[1], 'valute': (salary_parse(sal.text))[2],
                        'href': vac.get('href')}

                check_exist = collection.find_one({'href': data['href']})

                if not check_exist:
                    collection.insert_one(data)
                    added_rows += 1

        print(f'кол-во добавленных вакансий на должность {job_title}: {added_rows}')
        client.close()

    else:
        print(f'ошибка запроса: {response.status_code}')


if __name__ == '__main__':
    hh_scraper(input('Введите должность: '))

