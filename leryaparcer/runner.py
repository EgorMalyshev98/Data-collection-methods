
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from leryaparcer.spiders.leroy import LeroySpider
from time import time

if __name__ == '__main__':
    start = time()
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    search = input('Введите запрос для поиска:')
    runner.crawl(LeroySpider, search=search)
    # runner.crawl(SjruSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    print(time() - start)
