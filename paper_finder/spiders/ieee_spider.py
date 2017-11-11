import json

from paper_finder.paper_spiders import PaperSpider, APIKeyMissing
from paper_finder.scraping_utils import dig_dictionary
from paper_finder.settings import IEEE_API_KEY


class IEEESpider(PaperSpider):
    name = "IEEE"
    search_url = "http://ieeexploreapi.ieee.org/api/v1/search/articles?querytext=({query})&apikey={api_key}"

    def __init__(self, query, *args, **kwargs):
        if IEEE_API_KEY is None:
            raise APIKeyMissing(
                "Please provide an API key for the api: 'IEEE'.\n"
                "Set your key by assigning to variable 'IEEE_API_KEY' in "
                "the file 'paper_finder/settings.py'."
            )

        kwargs.update({"query": query, "api_key": IEEE_API_KEY})
        super().__init__(*args, **kwargs)

    @PaperSpider._assert_output_format
    def parse(self, response):
        raise NotImplementedError()
        # json_results = json.loads(response.body_as_unicode())

        """
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
        """
