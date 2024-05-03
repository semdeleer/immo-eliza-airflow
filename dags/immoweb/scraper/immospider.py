import scrapy


class ImmospiderSpider(scrapy.Spider):
    name = "immospider"
    allowed_domains = ["www.immoweb.be"]
    start_urls = ["https://www.immoweb.be/nl/zoeken/huis-en-appartement/te-koop"]

    def parse(self, response):
        pass
