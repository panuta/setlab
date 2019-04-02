# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from decimal import Decimal

from crawlers.items.stock_price import StockPrice


class SETTradeSpider(scrapy.Spider):
    name = 'settrade'

    # MongoDB
    collection_name = 'stock_price'
    unique_indexes = [('symbol', 1), ('date', 1)]

    # TODO => How to query by date range

    # db.getCollection('stock_price').createIndex({"symbol": 1, "date": 1}, {unique: true})
    #
    def __init__(self, symbols=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if symbols:
            self.symbol_list = symbols.split(',')
        else:
            self.symbol_list = []

    def start_requests(self):
        for symbol in self.symbol_list:
            request_url = 'https://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol={}&selectPage=2'.format(
                symbol.upper())
            yield scrapy.Request(request_url, self.parse, meta={'symbol': symbol})

    def parse(self, response):
        price_table = response.xpath('//div[@id="maincontent"]/descendant::table')[0]

        for table_row in price_table.xpath('.//tbody/tr'):
            values = table_row.xpath('.//td/text()').getall()

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

            yield StockPrice(
                symbol=response.meta['symbol'],
                date=datetime.strptime(values[0], '%d/%m/%y'),
                price_open=Decimal(values[1]),
                price_high=Decimal(values[2]),
                price_low=Decimal(values[3]),
                price_avg=Decimal(values[4]),
                price_close=Decimal(values[5]),
                price_change=Decimal(values[6]),
                price_change_percentage=Decimal(values[7]),
                trade_volume=Decimal(values[8].replace(',', '')),
                trade_value=Decimal(values[9].replace(',', '')),
            )

            # TODO => Do update_or_create