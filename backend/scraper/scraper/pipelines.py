# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Pipelines are for post-processing scraped items, e.g., cleansing HTML data,
# Or: clean data, manipulate, validate data, store in database, etc.


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).parent.parent.parent))

import db


class CleanDataPipeline:
    def process_item(self, item, spider):
        print("\033[92mCleanDataPipeline: Processing item\033[0m")
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

            if adapter.get('img'):
                img = adapter.get('img')
                if isinstance(img, str):
                    if img.endswith("/100"):
                        adapter['img'] = img[:-4]

        return item
    
class SQLitePipeline:
    def __init__(self):
        print("\033[94mSQLitePipeline: Initializing\033[0m")
        self.conn = db.get_connection()
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print("\033[94mSQLitePipeline: Processing item\033[0m")
        adapter = ItemAdapter(item)

        is_iced_update = (
            adapter.get("id") is not None
            and adapter.get("iced_status") is not None
            and adapter.get("description") is None
        )

        if is_iced_update:
            iced_status_int = 1 if adapter.get("iced_status") else 0
            iced_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if iced_status_int else None
            query = "UPDATE listings SET iced_status = ?, iced_at = ? WHERE id = ?"
            values = [iced_status_int, iced_at, adapter["id"]]

            try:
                self.cursor.execute(query, values)
                self.conn.commit()
                print("\033[92mSQLitePipeline: Iced status updated successfully\033[0m")
            except Exception as e:
                print(f"\033[91mSQLitePipeline: Failed to update iced status: {e}\033[0m")

            return item

        columns, placeholders, values = [], [], []

        for field in adapter.keys():
            columns.append(field)
            placeholders.append("?")
            value = adapter.get(field)
            if isinstance(value, list):
                value = json.dumps(value, ensure_ascii=False)
            values.append(value)

        category = adapter.get("category")
        if isinstance(category, list) and len(category) > 1:
            product_type = category[1]
            columns.append("product_type")
            placeholders.append("?")
            values.append(product_type)
        else:
            pass

        query = f"INSERT OR REPLACE INTO listings ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print("\033[92mSQLitePipeline: Item inserted successfully\033[0m")
        except Exception as e:
            print("\033[91mSQLitePipeline: Failed to insert Item: {e}\033[0m")

        return item
    
    def close_spider(self, spider):
        print("\033[91mSQLitePipeline: Closing spider\033[0m")
        self.conn.close()

