# -*- coding: utf-8 -*-
import scrapy
from fangRedis.items import NewHouseItem,EsfItem

class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']


    def parse(self, response):
        province_global = None
        table = response.css("#c02 table.table01")
        for tr in table.css('tr'):
            province_str = tr.xpath('./td[2]//text()').get().strip()
            if(province_str):
                province_global = province_str
            for a in tr.css('td:nth-child(3) a'):
                province = province_global
                city = a.xpath('./text()').get()
                city_url = a.xpath('./@href').get()
                tail_url = city_url.split('//')[1]
                if 'bj' in tail_url:
                    newhouse_url = 'https://newhouse.fang.com/house/s/'
                    esf_url = 'https://esf.fang.com/house/s/'
                else:
                    newhouse_url = "https://" +tail_url.split(".")[0] + ".newhouse.fang.com/house/s/"
                    esf_url = "https://" +tail_url.split(".")[0] + ".esf.fang.com/house/s/"
                meta = {"province":province,"city":city}
                yield scrapy.Request(newhouse_url,callback=self.parse_newhouse,meta=meta)
                yield scrapy.Request(esf_url,callback=self.parse_esf,meta=meta)

    def parse_newhouse(self,response):
        province = response.meta['province']
        city = response.meta['city']
        lis = response.xpath('//div[@class="nhouse_list"]//ul/li')
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]//a//text()').get()
            if(not name):
                continue
            else:
                name = name.strip()
            item = NewHouseItem()
            item.setdefault("province",province)
            item.setdefault("city",city)
            item.setdefault("name",name)
            yield item
        next_url = response.urljoin(response.xpath('//div[@class="page"]//a[@class="next"]/@href').get())
        yield scrapy.Request(next_url,callback=self.parse_newhouse,meta={"province":province,"city":city})



    def parse_esf(self,response):
        province = response.meta['province']
        city = response.meta['city']
        lis = response.css('.shop_list')
        for dl in lis.xpath('dl'):
            name = dl.xpath('./dd[1]/h4/a/@title').get()
            if (not name):
                continue
            else:
                name = name.strip()
            item = EsfItem()
            item.setdefault("province",province)
            item.setdefault("city",city)
            item.setdefault("name",name)
            yield item
        next_url = response.urljoin(response.xpath('//div[id="list_D10_15"]/p[1]/a/@href').get())
        yield scrapy.Request(next_url,callback=self.parse_esf,meta={"province":province,"city":city})

