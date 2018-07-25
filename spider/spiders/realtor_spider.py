import scrapy

from spider.item.address import Address


class RealtorSpider(scrapy.Spider):
    name = 'RealtorSpider'
    start_urls = ['https://www.realtor.com/propertyrecord-search/Winchester_MA']

    def parse(self, response):
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
