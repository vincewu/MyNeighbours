import redis
import scrapy

from MyNeighbours.item.address import Address


class RealtorSpider(scrapy.Spider):
    name = 'RealtorSpider'
    start_urls = ['https://www.realtor.com/propertyrecord-search/Winchester_MA']
    key = 'urlsToScrapy'

    def __init__(self):
        self.r = redis.Redis(host='server', charset="utf-8", decode_responses=True)

    def start_requests(self):
        url = self.r.lpop(self.key)
        while url:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        if response.status == 401:
            self.r.lpush(self.key, response.url)
            return

        address_table = response.css('.address-table').extract_first()

        if address_table:
            """Properties page"""
            for address in response.css('.address-table td a::text').extract():
                addr, town, state_zip = address.split(', ')
                state, zipcode = state_zip.split(' ')
                yield Address(address=addr, town=town, state=state, zipcode=zipcode)
        else:
            """Street page"""
            for street in response.css('.row .row a::attr(href)').extract():
                yield response.follow(street, self.parse)

        for town in response.css('a.next::attr(href)').extract():
            yield response.follow(town, self.parse)
