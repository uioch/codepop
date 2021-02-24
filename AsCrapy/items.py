# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

ASPW = {
    'q'  : '【习题】',
    'qa' : '【答案】',
}

class AsItem(scrapy.Item):
    qc     = scrapy.Field()
    qt     = scrapy.Field()
    qname  = scrapy.Field()

    qurl   = scrapy.Field()
    qtext  = scrapy.Field()
    qimg   = scrapy.Field()
    
    qaurl  = scrapy.Field()
    qatext = scrapy.Field()
    qaimg  = scrapy.Field()
    
    pw     = scrapy.Field()

    file_urls = scrapy.Field()
    files     = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
