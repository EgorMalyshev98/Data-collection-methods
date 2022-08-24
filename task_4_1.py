import requests
from lxml import html
from pprint import pprint


def news_scraper():
    url = 'https://lenta.ru'
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/104.0.0.0 Safari/537.36'}
    response = session.get(url, headers=headers)
    print('status code:', response.status_code)

    dom = html.fromstring(response.text)

    hrefs = dom.xpath("//div[contains(@class,'topnews')]//a[not(contains(@target, '_blank'))]/@href")

    top_title = dom.xpath("//div[contains(@class,'topnews')]//a[not(contains(@target, '_blank'))]//"
                          "h3[contains(@class, 'title')]/text()")

    titles = dom.xpath("//div[contains(@class,'topnews')]//a[not(contains(@target, '_blank'))]//"
                       "span[contains(@class, 'title')]/text()")
    titles.insert(0, *top_title)

    links = [url + href for href in hrefs]
    dates = ['.'.join(href.split('/')[2:5]) for href in hrefs]

    data_dict = {}

    for link, title, date, i in zip(links, titles, dates, range(len(links))):

        data = {'link': link, 'title': title, 'date': date}
        data_dict[i] = data
    return data_dict


if __name__ == '__main__':
    pprint(news_scraper())




