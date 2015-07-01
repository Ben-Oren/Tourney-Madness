import scrapy
import sys
import re

sys.path.append('/Users/Ben/desktop/code/python/projects/bball')
from bball.items import BballItem

from datacleaning import teamyear

def urllist(list):
    urls = []
    for x in list:
        year = x.pop()
        team = x.pop()
        team = team.lower()
        team = re.sub(' ', '-', team)
        url = "http://www.sports-reference.com/cbb/schools/"+team+"/"+year+".html"
        urls.append(url)
    return urls
    
def testurl(list):
    urls = []
    year = list[0].pop()
    team = list[0].pop() 
    urls.append("http://www.sports-reference.com/cbb/schools/"+team+"/"+year+".html")
    return urls

def xtract(data):
    return str(data).split("'")[1]

class BigDanceSpider(scrapy.Spider):
    name = 'dance'
    allowed_domains = ["http://www.sports-reference.com"]
    start_urls = urllist(teamyear)
    
    def parse(self, response):
        item = BballItem()
        dump = []
        found = ""
        
        for sel in response.xpath('//ul[@class="hovermenu large_text menu"]/li[1]'):
            x = sel.xpath('a/text()').extract()
            item["mteam"] = xtract(x)[:len(x)-8]
        for sel in response.xpath('//div[@id="info_box"]'):
            item["myear"] = xtract(sel.xpath('h1/text()').extract())[0:7]
            x = sel.xpath('p[4]/text()').extract()
            x = str(x)
            dump.append(x)
            
        #print dump
        
        count = 0
        for each in dump:
            count = count + each.count("Won")
            
        item["mresult"] = count
        
        m = str(dump).find("#")
        #print m
        
        rank = str(dump)[m+1]+str(dump)[m+2]
        
        #print rank
        item["mrank"] = rank
        
        yield item       
        
