from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from bookparser.spiders.labirint import LabirintSpider
from time import time

if __name__ == '__main__':
    start = time()
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(LabirintSpider)
    # runner.crawl(SjruSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    print(time() - start)
