#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
import argparse
from subprocess import check_output


def list_apis(args):
    spiders = [
        spider_name for spider_name in
        map(lambda spider: spider.strip(),
            check_output(["scrapy", "list"]).decode().split("\n"))
        if spider_name
    ]
    return spiders


def query_apis(args):
    from paper_finder.paper_spiders import ScraperPaperSpider
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.misc import walk_modules
    from scrapy.utils.spider import iter_spider_classes
    from scrapy.utils.project import get_project_settings
    from itertools import chain as iter_chain

    # Iterator over all our spider classes
    spider_iter = iter_chain(*[
        iter_spider_classes(module)
        for module in walk_modules("paper_finder.spiders")
    ])

    crawler_process = CrawlerProcess(get_project_settings())
    for spider in spider_iter:
        # name = spider.name is_scraper = spider.is_scraper
        # XXX Remove hardcoded query
        if not args.scrape and isinstance(spider, ScraperPaperSpider):
            continue
        crawler_process.crawl(spider, query=args.search_term)
    crawler_process.start()


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    list_apis_parser = subparsers.add_parser(
        "list", help="List all supported information sources."
    )

    list_apis_parser.set_defaults(fun=list_apis)

    find_papers_parser = subparsers.add_parser(
        "find",
        help="Query (all) information sources for papers matching the given TERM."
    )

    find_papers_parser.add_argument(
        "search_term", help="Search term to find papers for."
    )

    find_papers_parser.add_argument(
        "--scrape",
        help="Boolean flag that turns on scraping for papers. "
             "Note that scraping may be disallowed by some information sources "
             "and specifiying this flag may result in IP-bans by the respective "
             "information source.",
        default=False,
        dest="scrape",
        action="store_true"
    )

    find_papers_parser.set_defaults(fun=query_apis)

    args = parser.parse_args()

    args.fun(args)

if __name__ == "__main__":
    main()
