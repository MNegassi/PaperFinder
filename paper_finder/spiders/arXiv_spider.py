from paper_finder.paper_spider import PaperSpider


class ArxivSpider(PaperSpider):
    name = "arXiv"
    search_url = "http://export.arxiv.org/api/query?search_query=all:{keyword}&start=0&max_results={max_results}"

    def __init__(self, query, max_results=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            self.query_keyword(
                keyword=query, max_results=int(max_results)
            )

        ]

    def query_keyword(self, **kwargs):
        return self.search_url.format(
            **kwargs
        )

    @PaperSpider._assert_output_format
    def parse(self, response):
        selector = response.selector
        selector.remove_namespaces()

        def extract_information(xpath):
            return [
                subselector.extract() for subselector in selector.xpath(xpath)
            ]

        _, *titles = extract_information("//title/text()")

        # we want at least titles to see how many papers there are
        assert titles

        abstracts = extract_information("//summary/text()")

        dates = extract_information("//published/text()")

        journals = extract_information("//journal_ref/text()")

        # XXX: How to properly handle cases of partial information?
        if len(journals) < len(titles):
            journals = [None] * len(titles)

        paper_links = extract_information('//link[@title="pdf"]/@href')

        paper_info = zip(titles, abstracts, dates, journals, paper_links)

        print(len(abstracts), len(titles), len(dates), len(journals))
        assert len(abstracts) == len(titles) == len(dates) == len(journals)

        for title, abstract, date, journal, pdf_href in paper_info:
            yield {
                "query": response.url,
                "pdf_href": pdf_href,
                "title": title,
                "abstract": abstract,
                "date:": date,
                "journal": journal,
                "origin": self.name
            }
