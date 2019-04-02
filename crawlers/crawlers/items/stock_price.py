import scrapy


class StockPrice(scrapy.Item):
    symbol = scrapy.Field()
    date = scrapy.Field()
    price_open = scrapy.Field()
    price_high = scrapy.Field()
    price_low = scrapy.Field()
    price_avg = scrapy.Field()
    price_close = scrapy.Field()
    price_change = scrapy.Field()
    price_change_percentage = scrapy.Field()
    trade_volume = scrapy.Field()
    trade_value = scrapy.Field()

    # MongoDB
    UNIQUE_KEYS = ['symbol', 'date']
