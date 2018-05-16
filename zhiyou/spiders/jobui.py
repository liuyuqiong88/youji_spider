# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from zhiyou.items import ZhiyouItem
from scrapy_redis.spiders import RedisCrawlSpider

class JobuiSpider(RedisCrawlSpider):
    name = 'jobui'
    allowed_domains = ['jobui.com']
    # start_urls = ['http://www.jobui.com/cmp?keyword=%E6%B1%87%E6%A1%94%E7%BD%91']

    rules = (
        Rule(LinkExtractor(allow=r'cmp?keyword='), follow=True),
        Rule(LinkExtractor(allow=r'/company/\d+/$'), callback='parse_item')
    )

        # ----4 设置redis_key
    redis_key = 'johui'

    # ----5 动态获取允许的域
    # def __init__(self, *args, **kwargs):
    #     domain = kwargs.pop(('jobui.com',))
    #
    #     # filter()必须强转为列表
    #     self.allowed_domains = list(filter(None, domain.split(',')))
    #     super(JobuiSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item = ZhiyouItem()
        item['data_source'] = response.url
        item['time_stamp'] = time.time()
        item['company_name'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        try:

            item['category'] = response.xpath('//*[@id="cmp-intro"]//dl/dd[1]/text()').extract_first().split('/')[0]
            item['num'] = response.xpath('//*[@id="cmp-intro"]//dl/dd[1]/text()').extract_first().split('/')[1]
        except:
            item['num'],item['category'] = "此页该项数据未写","此页该项数据未写"


        item['industry'] = response.xpath('//*[@id="cmp-intro"]//dl/dd[2]/a/text()|//*[@id="cmp-intro"]//dl/dd/a/text()').extract_first()
        item['desc'] = ''.join(response.xpath('//*[@id="textShowMore"]/text()').extract()).strip()
        item['good'] = response.xpath('//div[@class="swf-contA"]//h3[@class="swf-tit"]/text()').extract_first()
        item['salary'] = response.xpath('//div[@class="swf-contB"]//h3[@class="swf-tit"]/text()').extract_first()


        node_list = response.xpath('//div[@class="jk-matter jk-box fs16"]/ul')

        data_list = []
        for node in node_list:
            temp = {}
            temp['date'] = node.xpath('./li/span[1]/text()').extract_first()
            temp['status'] = node.xpath('./li/h3/text()').extract_first()
            temp['sum'] = node.xpath('./li/span[2]/text()').extract_first()
            temp['boss'] = node.xpath('./li/span[3]/text()').extract_first()
            data_list.append(temp)

        item['fancing_info'] = data_list
        item['address'] = response.xpath('//dl[@class="dlli fs16"]/dd[1]/text()').extract_first()
        item['contact'] = response.xpath('//dl[@class="dlli fs16"]/div[@class="j-shower1 dn"]/dd/text()').extract_first()
        item['qq'] = response.xpath('//dd[@class="cfix"]/span/text()').extract_first()



        print(item['company_name'],item['industry'])

        yield item





