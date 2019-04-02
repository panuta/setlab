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
        price_table = response.xpath('//div[@id="maincontent"]/descendant::table')[0]

        """
        วันที่
        ราคาเปิด
        ราคาสูงสุด
        ราคาต่ำสุด
        ราคาเฉลี่ย
        ราคาปิด
        เปลี่ยนแปลง
        %เปลี่ยนแปลง
        ปริมาณ (พันหุ้น)
        มูลค่า (ล้านบาท)
        SET Index
        %เปลี่ยนแปลง
        """

        for table_row in price_table.xpath('.//tbody/tr'):
            table_row.xpath('.//td').getall()

            # StockPrice
