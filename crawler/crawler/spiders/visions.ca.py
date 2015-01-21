import re
from scrapy.http import Request

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from crawler.items import Product
from scrapy.contrib.loader import ItemLoader



class VisionsSpider(CrawlSpider):
    name = "visions.ca"
    domain_name = "visions.ca"
    start_urls = ["http://www.visions.ca/"]

    CONCURRENT_REQUESTS = 15
    download_delay = 1

    ##USAGE: scrapy crawl visions.ca , file visions.ca_example.json contains a sample run with nearly 100 products
    ##if you run it again the result will be in visions.ca.json

    rules = (
        # categories
        Rule(SgmlLinkExtractor(restrict_xpaths=(
            "//li[contains(@class,'menulevel-0')]//div/a",
            "//li[contains(@class,'menulevel-0')]/a[not(contains(./following-sibling::div/@id,'menu')) and contains(@href,'837')]"
            ),
                               unique=True), follow=True),

        #pagination
        Rule(SgmlLinkExtractor(restrict_xpaths=("//a[@title='Next']"),
                               unique=True), follow=True),
        #brands for categories with no sub categories (Gift cards)
        Rule(SgmlLinkExtractor(restrict_xpaths=("//div[contains(@id,'subcatemenu-brand-all')]//a"),
                               unique=True),follow=True),
        #products for bundle and normal categories 
        Rule(
            SgmlLinkExtractor(restrict_xpaths=(
                "//div[contains(@class,'bundleItem')]//td[@class='name']/a",
                "//div[contains(@class,'productresult')]//a[contains(@id,'lnk')]"),
                               unique=True),callback='parse_item', follow=True),
    )

    def parse_item(self,response):
        sel = Selector(response)
        il = ItemLoader(item=Product(), response=response)
        il.add_xpath("name","//div[contains(@class,'productdetail-container')]//span[contains(@id,'ProdTitle')]/..//text()")
        #other form of pages are available : http://www.visions.ca/Catalogue/Bundles/Details.aspx?bundleId=2260
        #same for price xpath
        il.add_xpath("name","//div[@class='catalogueTitle']/*/text()")
        il.add_value("url",response.url)
        il.add_xpath("current_price","//div[contains(@class,'pricing') or contains(@class,'price')]//span[contains(@id,'Saleprice') or contains(@class,'salePrice')]//text()")
        il.add_xpath("old_price","//div[contains(@class,'pricing') or contains(@class,'price')]//span[contains(@id,'Regprice') or contains(@class,'regPrice')]//text()")
        limited = sel.xpath("//div[contains(@id,'FinalClearance')]").extract()
        if len(limited) > 0:
            il.add_value("availability","Limited Quantities")
        else:
            il.add_value("availability","Available")
        return il.load_item()
