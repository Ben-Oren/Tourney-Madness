import scrapy
import sys
import string

sys.path.append('/Users/Ben/desktop/code/python/projects/bball')
from bball.items  import BballItem, BballItem2, BballItem3, BballItem4, BballItem5, BballItem6, BballItem7


#creating list of urls

years = range(1998,2015)

confcodes = ['acc', 'big-east', 'big-12', 'big-ten', 'sec', 'cusa', 'mvc', 'patriot', 'horizon', 'pac-10']

urls = ["http://www.sports-reference.com/cbb/conferences/%s"%(confcodes[x]) for x in range(len(confcodes))]

testurl = ["http://www.sports-reference.com/cbb/conferences/acc/2007.html"]


#this is the list that will contain the urls
list = []
for url in urls:
    for year in years:
        list.append(url+'/'+str(year)+'.html')
        
def xtract(data):
    return str(data).split("'")[1]
    #if len(x) == 3 and num == 1:
    #    return x[1]
    #if len(x) > 3 and num == 1:
    #    return x[1]
    #if len(x) > 3 and num == 2:
    #    return x[3]
    
def cochamptest(data):
    for each in str(data).split("'"):
        if each[0] in string.ascii_uppercase:
            return each
    
            
        
class BballSpider(scrapy.Spider):

    name = 'conf'
    allowed_domains = ["http://www.sports-reference.com"]
    start_urls = list
    
    def parse(self, response):
        #getting list of intersection of reg / tournament champions and teams who went to the ncaa
        champlist = []
        for sel in response.xpath('//div[@id="info_box"]/p[4]/a[position()<last()]'):
            champlist.append(cochamptest(sel.xpath('text()').extract()))
        
            
        ncaalist = []
        for sel in response.xpath('//div[@id="info_box"]/p[5]/span/a'):
            ncaalist.append(xtract(sel.xpath('text()').extract()))
               
        bothlist = [x for x in ncaalist if x in champlist]
        
        for x in range(len(ncaalist)):
            if x == 0:
                item = BballItem()
            if x == 1:
                item = BballItem2()
            if x == 2:    
                item = BballItem3()
            if x == 3:
                item = BballItem4()
            if x == 4:
                item = BballItem5()
            if x == 5:
                item = BballItem6()
            if x == 6:
                item = BballItem7()
            if x == 7:
                item = BbalItem8()
            if x == 8:
                item = BballItem9()
            if x == 9:
                item = BballItem10()
            if x == 10:
                item = BballItem11()
            
            #the team in the item is at the current position in the ncaalist
            item['team'] = ncaalist[x]
            
            if item['team'] in champlist:
                item['regchamp'] = "Y"
            #if item['team'] == xtract(response.xpath('//div[@id="info_box"]/p[4]/a[position()<last()]/text()').extract(), 2):
             #   item['regchamp'] = "Y"
            else:
                item['regchamp'] = "N"
            if item['team'] == xtract(response.xpath('//div[@id="info_box"]/p[4]/a[last()]/text()').extract()):
                item['tournchamp'] = "Y"
            else:
                item['tournchamp'] = "N"
            #get reg season champ, conference and year
    	    #for sel in response.xpath('//div[@id="info_box"]/p[4]/a[1]'):
    	    #    item['team'] = sel.xpath('text()').extract()
    	    #    item['team'] = xtract(item['team'])
    	    for sel in response.xpath('//div[@id="you_are_here"]/p'):
    	        item['conf'] = sel.xpath('span[4]/a/span/text()').extract()
    	        item['conf'] = xtract(item['conf'])
                item['year'] = sel.xpath('span[5]/span/span/text()').extract()
                item['year'] = xtract(item['year'])
        
            #get the number of tourney wins. only return one search at a time, and necessary to distinguish between eg Iowa and Iowa State, so subract the search that contains "Team_name " from the search that contains "Team_name"
        
            # "team" eg Iowa or Iowa State
            c = len(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[position()>(last()-11)]/td/a[contains(., "%s")]'%(item['team'])))
        
            # "team " eg Iowa State
            d = len(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[position()>(last()-11)]/td/a[contains(., "%s ")]'%(item['team'])))
        
            #eg Iowa and/or Iowa State - Iowa State
            wins = abs(c - d)

        #if len(b) != 0:
        #    print wins
        #    wins =  abs(len(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr/td/a[contains(.,"%s")]'%(item['team']))))
        #    print wins
            
            #counting the winner of the last game
            if wins == 3 and item['team'] == xtract(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[last()]/td[@class="bold_text"]/a/text()').extract()):
                wins = 4
            
            #Horizon league structure works a little differently . . .    
            if wins == 2 and item['team'] == xtract(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[last()]/td[@class="bold_text"]/a/text()').extract()) and item['conf'] == "Horizon League":
                wins = 3
        
               
                #str(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[last()]/td[@class="bold_text"]/a/text()').extract()).split("'")[1]
                
            item["result"] = wins
        
            yield item
         
         #tryin to figure out score . . . will do later, how about
         #sel = response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr/td/a[contains(.,"%s")]'%item['team']).pop()
         
         #item['score'] 

        #if champlist[1] in ncaalist:    
        #    item = BballItem2() 
            
        #    item["team"] = champlist[1]
            #get reg season champ, conference and year
    	    #for sel in response.xpath('//div[@id="info_box"]/p[4]/a[1]'):
    	    #    item['team'] = sel.xpath('text()').extract()
    	    #    item['team'] = xtract(item['team'])
    	#    for sel in response.xpath('//div[@id="you_are_here"]/p'):
    	#        item['conf'] = sel.xpath('span[4]/a/span/text()').extract()
    	#        item['conf'] = xtract(item['conf'])
        #        item['year'] = sel.xpath('span[5]/span/span/text()').extract()
        #        item['year'] = xtract(item['year'])
        
            #get the number of tourney wins. only return one search at a time, and necessary to distinguish between eg Iowa and Iowa State, so subract the search that contains "Team_name " from the search that contains "Team_name"
        
            # "team" eg Iowa or Iowa State
        #    c = len(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr/td/a[contains(., "%s")]'%(item['team'])))
        
            # "team " eg Iowa State
        #    d = len(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr/td/a[contains(., "%s ")]'%(item['team'])))
        
            #eg Iowa and/or Iowa State - Iowa State
        #    wins = abs(c - d)

        #if len(b) != 0:
        #    print wins
        #    wins =  abs(len(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr/td/a[contains(.,"%s")]'%(item['team']))))
        #    print wins
            
            #counting the winner of the last game
        #    if wins == 3 and item['team'] == xtract(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[last()]/td[@class="bold_text"]/a/text()').extract()):
        #        wins = 4
            
            #Horizon league structure works a little differently . . .    
        #    if wins == 2 and item['team'] == xtract(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[last()]/td[@class="bold_text"]/a/text()').extract()) and item['conf'] == "Horizon League":
        #        wins = 3
        
               
                #str(response.xpath('//div[@id="all_ctourn"]/div[2]/table/tr[last()]/td[@class="bold_text"]/a/text()').extract()).split("'")[1]
                
        #    item["result"] = wins
        
        #    yield item
        #    item = BballItem()    
    
    