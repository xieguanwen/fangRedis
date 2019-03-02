# **redis+scrapy+selenium**
redis分布式爬虫修改步骤
## **1.第一步**
from scrapy_redis.spiders import RedisSpider
class FangSpider(scrapy.Spider): 修改成 class FangSpider(RedisSpider):

## **2.第二步**
去掉 start_urls = ['https://www.fang.com/SoufunFamily.htm']
添加 redis_key = "fang:start_urls"

## **3.第三步**
在settings.py文件中加入
#### 使用scrapy_redis的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
#### 在Redis中保持scrapy-redis用到的各个队列，从而允许暂停和恢复
SCHEDULER_PERSIST = True
#### 使用scrapy_redis的去重
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
#### 使用scrapy_redis的存储
ITEM_PIPELINES = {
'scrapy_redis.pipelines.RedisPipeline':300,
}
#### 定义Redis的 ip和端口
REDIS_HOST = '127.0.0.1' #ip地址
REDIS_PORT = 6379

注意原来的：
ITEM_PIPELINES注释

**这个浏览器要和你本计算机对应(chromedriver)**