# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse


class SETTradeSpider(scrapy.Spider):
    name = 'settrade'

    def __init__(self, symbols=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if symbols:
            self.symbol_list = symbols.split(',')
        else:
            self.symbol_list = []

    def start_requests(self):
        for symbol in self.symbol_list:
            request_url = 'https://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol={}&selectPage=2'.format(
                symbol)
            yield scrapy.Request(request_url, self.parse)

    def parse(self, response):


        for article_id in response.xpath('//article/@id').getall():
            article_id = article_id.split('-')[1]
            yield scrapy.Request(response.urljoin('/content/{article_id}'.format(
                article_id=article_id)), self.parse_article)
            break

    def parse_article(self, response):
        excerpt = response.xpath('//p[@class="entry-excerpt"]/text()').getall()[0]
        _, _, date_text = excerpt.rpartition('on')
        article_date = parse(date_text)

        tables = response.xpath('//article/descendant::table')
        symbols_for_top_purchased_by_value = self._symbols_from_table(tables[2])
        symbols_for_top_sold_by_value = self._symbols_from_table(tables[3])

    def _symbols_from_table(self, table):
        return [table_row.xpath('.//td/text()').getall() for table_row in table.xpath('.//tr')[1:]]
