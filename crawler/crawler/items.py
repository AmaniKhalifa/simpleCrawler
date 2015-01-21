# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import TakeFirst , MapCompose ,Join


def clean(value):
	return value.replace('\t','').replace('\n','').replace('\r','').strip()

def extract_price(value):
	return value.lower().replace('sale','').replace('price','').replace(':','').strip()

class Product(scrapy.Item):
	name = Field(
		input_processor = MapCompose(clean),
		output_processor = Join()
		)
	url = Field(output_processor = TakeFirst())
	current_price = Field(
		input_processor = MapCompose(extract_price),
		output_processor = TakeFirst()
		)
	old_price = Field(		
		input_processor = MapCompose(extract_price),
		output_processor = TakeFirst()
		)
	availability = Field(output_processor = TakeFirst())
