import requests
from bs4 import BeautifulSoup
import pandas as pd
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

    url = 'https://hh.ru/search/vacancy'
    params = {'text': job_title, 'from': 'suggest_post', 'salary': '', 'clusters': 'true', 'ored_clusters': 'true',
              'enable_snippets': 'true',
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

        data = {'vacancy': [], 'salary_min': [], 'salary_max': [], 'valute': [], 'href': []}

        for page in range(int(last_page)):
            print('page number:', page)
            params['page'] = page
            response = session.get(url, headers=headers, params=params)
            dom = BeautifulSoup(response.text, 'html.parser')

            salaries = dom.find_all('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancies = dom.find_all('a', {'data-qa': 'vacancy-serp__vacancy-title'})

            for vac, sal in zip(vacancies, salaries):
                vacancy = vac.text
                salar = sal.text
                href = vac.get('href')

                salr = salary_parse(salar)
                data['vacancy'].append(vacancy)
                data['href'].append(href)
                data['salary_min'].append(salr[0])
                data['salary_max'].append(salr[1])
                data['valute'].append(salr[2])

        df = pd.DataFrame(data)
        df.to_csv('result.csv')


if __name__ == '__main__':
    hh_scraper(input('Введите должность: '))
