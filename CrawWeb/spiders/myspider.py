import scrapy
from CrawWeb.items import CrawwebItem


class Hongxiuwangzhan(scrapy.Spider):
    name = 'nk'
    allowed_domain = ['www.nowcoder.com']
    start_urls = ['https://www.nowcoder.com/ta/review-java/review?page=1']

    def parse(self, response):
        que = response.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/text()').extract()
        ans = response.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/text()').extract()
        #删除列表中的换行字符\n
        a = [x.strip() for x in ans if x.strip()!='']
        q = [x.strip() for x in que if x.strip()!='']
        #将存储方式由array数组变为字符串
        answer = "\n".join(a)
        question = "\n".join(q)
        item = CrawwebItem()
        item['question'] = question
        item['answer'] = answer
        yield item
        pass

        for i in range(2, 120):
            next_page = 'https://www.nowcoder.com/ta/review-java/review?page='+str(i)
            yield scrapy.Request(next_page, callback=self.parse, method="Get")