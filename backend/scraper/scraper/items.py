# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    site = scrapy.Field()
    id = scrapy.Field()
    category = scrapy.Field()
    iced_status = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    title = scrapy.Field()
    seller = scrapy.Field()
    seller_rating = scrapy.Field()
    seller_profile_url = scrapy.Field()
    location = scrapy.Field()
    delivery_options = scrapy.Field()
    listed_at = scrapy.Field()
    listing_url = scrapy.Field()
    description = scrapy.Field()