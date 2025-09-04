# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Pipelines are for post-processing scraped items, e.g., cleansing HTML data,
# Or: clean data, manipulate, validate data, store in database, etc.


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime


class ScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('id') is not None:
            adapter['id'] = int(adapter['id'])

        if adapter.get('listed_at'):
            listed_at = adapter.get('listed_at')
            try:
                if isinstance(listed_at, str):
                    adapter['listed_at'] = datetime.strptime(listed_at.strip(), "%Y-%m-%d %H:%M")
            except Exception as e:
                spider.logger.warning(f"Failed to convert date: {listed_at}. Error: {e}")

        if spider.name == 'hardver':
            if adapter.get('title'):
                title = adapter.get('title')
                adapter['title'] = title[:-len(" - HardverApró")] # type: ignore

            if adapter.get('price'):
                price_str = adapter.get('price')
                if isinstance(price_str, str):
                    cleaned_price = price_str.replace(' ', '').replace('Ft', '').strip()
                    try:
                        adapter['price'] = int(cleaned_price)
                    except ValueError:
                        spider.logger.warning(f"Could not convert price: {price_str}")

            if adapter.get('category'):
                category = adapter.get('category')
                if isinstance(category, str):
                    adapter['category'] = category.replace("/ ", "").strip().split("/")



        return item