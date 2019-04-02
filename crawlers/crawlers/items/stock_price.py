# -*- coding: utf-8 -*-
import scrapy


class StockPrice(scrapy.Item):
    symbol = scrapy.Field()
    date = scrapy.Field()  # วันที่
    price_open = scrapy.Field()  # ราคาเปิด
    price_high = scrapy.Field()  # ราคาสูงสุด
    price_low = scrapy.Field()  # ราคาต่ำสุด
    price_avg = scrapy.Field()  # ราคาเฉลี่ย
    price_close = scrapy.Field()  # ราคาปิด
    price_change = scrapy.Field()  # เปลี่ยนแปลง
    price_change_percentage = scrapy.Field()  # %เปลี่ยนแปลง
    trade_volume = scrapy.Field()  # ปริมาณ (พันหุ้น)
    trade_value = scrapy.Field()  # มูลค่า (ล้านบาท)

    # MongoDB
    UNIQUE_KEYS = ['symbol', 'date']
