import json

from paper_finder.paper_spiders import PaperSpider, APIKeyMissing
from paper_finder.scraping_utils import dig_dictionary
from paper_finder.settings import SPRINGER_API_KEY


class SpringerSpider(PaperSpider):
    name = "Springer"
    search_url = "http://api.springer.com/metadata/json?q={keyword}&api_key={api_key}"

    def __init__(self, query, max_results=1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if SPRINGER_API_KEY is None:
            raise APIKeyMissing(
                "Please provide an API key for the api: 'Springer'.\n"
                "Set your key by assigning to variable 'SPRINGER_API_KEY' in "
                "the file 'paper_finder/settings.py'."
            )

        self.start_urls = [
            self.query_keyword(
                keyword=query, api_key=SPRINGER_API_KEY
            )
        ]

    def query_keyword(self, **kwargs):
        return self.search_url.format(
            **kwargs
        )

    @PaperSpider._assert_output_format
    def parse(self, response):
        json_results = json.loads(response.body_as_unicode())

        for record in json_results["records"]:
            yield {
                "query": response.url,
                "href": dig_dictionary(record, "url", 0, "value"),
                "title": record.get("title"),
                "abstract": record.get("abstract"),
                "date": record.get("publicationDate"),
                # XXX Journals are id encoded here and require
                # additional lookups with different api -
                # this is future work for now
                "journal": None,

                "origin": self.name
            }
