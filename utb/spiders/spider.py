import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import UtbItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class UtbSpider(scrapy.Spider):
	name = 'utb'
	start_urls = ['https://www.utb-bank.be/announcements/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="loop-document-item"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="paginatie"]/a[@class="next page-numbers"]').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//span[@class="special-span"]//text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="single-content"]/p//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=UtbItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
