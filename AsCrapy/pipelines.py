# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
from As.items import AsItem

class AsPipeline():
    def __init__(self, *args, **kwargs):
        pass

    def process_item(self, item, spider):
        logging.warn('>>>>> %s', str(item))
        # TODO save item
        return item

