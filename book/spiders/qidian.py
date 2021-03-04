import scrapy
from copy import deepcopy

class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com']
    start_urls = ['https://www.qidian.com/all?orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0']

    def parse(self, response):
        lis = response.xpath("//div[@class='work-filter type-filter']/ul/li")[1:]
        for i in lis:
            item = {}
            item["type"] = i.xpath("./a/text()").extract_first()
            type_url = "https://" + i.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=type_url, callback=self.parse_type, meta={"item": item}, dont_filter=True)

    def parse_type(self, response):
        item = response.meta["item"]
        lis = response.xpath("//div[@class='book-img-text']/ul/li")
        for i in lis:
            item["url"] = "https:" + i.xpath("./div[@class='book-img-box']/a/@href").extract_first()
            item["img"] = "http:" + i.xpath("./div[@class='book-img-box']/a/img/@src").extract_first()
            item["title"] = i.xpath("./div[@class='book-mid-info']/h4/a/text()").extract_first()
            item["author"] = i.xpath("./div[@class='book-mid-info']/p[@class='author']/a[@class='name']/text()").extract_first()
            item["intro"] = i.xpath("./div[@class='book-mid-info']/p[@class='intro']/text()").extract_first()
            yield scrapy.Request(url=item["url"], callback=self.parse_detail, meta={"item": deepcopy(item)}, dont_filter=True)

        next_url = response.xpath("//div[@class='lbf-pagination']/ul/li/a[@class='lbf-pagination-next ']/@href").extract_first()
        if next_url != "javascript:;" and next_url is not None:
            next_url = "https:" + next_url
            yield scrapy.Request(url=next_url, callback=self.parse_type, meta={"item": deepcopy(item)}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta["item"]
        item["tag"] = response.xpath("//div[@class='book-info ']/p[@class='tag']/*/text() | //div[@class='detail']/p[@class='tag-wrap']/a/text()").extract()
        yield item