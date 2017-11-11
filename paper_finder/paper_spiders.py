from scrapy import Spider
import abc
from functools import wraps


class PaperSpider(Spider):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [
            self.query_keyword(**kwargs)

        ]

    def query_keyword(self, **kwargs):
        return self.search_url.format(
            **kwargs
        )

    @classmethod
    def _assert_output_format(cls, parse_fun):
        # assert that parse_fun returns properly formatted dictionaries
        # that have keys for all info we want to extract.
        # This ensures all spiders parse the same kind of information.
        # Later, we can remove this, since our database insertion procedures
        # will check that.

        expected_output_keys = {
            'query', 'date', 'origin', 'title',
            'journal', 'abstract', 'href'
        }

        @wraps(parse_fun)
        def wrapped(*args, **kwargs):
            return_dicts = list(parse_fun(*args, **kwargs))
            assert all(hasattr(return_dict, "keys") for return_dict in return_dicts)

            for return_dict in return_dicts:
                return_keys = set(return_dict.keys())
                assert return_keys == expected_output_keys

            yield from return_dicts
        return wrapped

    @abc.abstractmethod
    def parse(self, response):
        raise NotImplementedError("Not implemented in base class!")


class ScraperPaperSpider(PaperSpider):
    # XXX Collect scraper specific stuff here
    __metaclass__ = abc.ABCMeta


class APIKeyMissing(ValueError):
    """ Raised if an API requires a key and that key was not provided.
        Keys are set in 'paper_finder/settings.py' and imported from there.
    """
