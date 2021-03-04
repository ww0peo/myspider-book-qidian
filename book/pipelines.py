# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re

class BookPipeline:
    def process_item(self, item, spider):
        item["intro"] = self.process_content(item["intro"])
        print(item)
        return item

    def process_content(self, content):
        content = re.sub(r" |\r", '', content)
        return content
