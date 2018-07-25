import scrapy


class Address(scrapy.Item):
    address = scrapy.Field()
    town = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()