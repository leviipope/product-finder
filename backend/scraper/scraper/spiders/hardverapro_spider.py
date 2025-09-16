import scrapy
from scraper.items import ScraperItem
from datetime import datetime
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.db import get_active_listing_ids, get_latest_price

class HardverSpider(scrapy.Spider):
    name = "hardver"
    start_urls = [
        #"https://hardverapro.hu/aprok/hardver/videokartya/nvidia/geforce_30xx/index.html",
        #"https://hardverapro.hu/index.html",
        #'https://hardverapro.hu/aprok/notebook/index.html'
        "https://hardverapro.hu/aprok/notebook/pc/keres.php?stext=&stcid_text=&stcid=&stmid_text=&stmid=&minprice=210000&maxprice=211000&cmpid_text=&cmpid=&usrid_text=&usrid=&__buying=1&__buying=0&stext_none=&__brandnew=1&__brandnew=0",
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_listings = get_active_listing_ids()
        self.seen_ids = set()

    def parse(self, response):
        listings = response.css('ul.list-unstyled > li[class]')

        for listing in listings:
            data_uadid = listing.attrib.get('data-uadid')
            self.seen_ids.add(data_uadid)

            iced_status = listing.css("div[class='uad-col uad-col-price'] div::attr(class)").get()
            if iced_status == "uad-price uad-price-iced":
                iced_status = True
            elif iced_status == "uad-price":
                iced_status = False

            price = listing.css("div[class='uad-col uad-col-price'] span::text").get()
            if price == "Keresem":
                continue

            if data_uadid in self.active_listings:
                current_price = int(price.replace(' ', '').replace('Ft', '').strip())

                latest_price_in_db = get_latest_price(data_uadid)
                iced_status_in_db = self.active_listings[data_uadid]

                price_changed = current_price != latest_price_in_db
                iced_status_changed = iced_status != iced_status_in_db

                if price_changed or iced_status_changed:
                    print(f"\033[38;5;153mSending item as iced item or price update item: {data_uadid}\033[0m")
                    yield {
                        'id': data_uadid,
                        'iced_status': iced_status,
                        'price': price,
                    }
                else:
                    print(f"\033[38;5;215mSkipped because duplicate: {data_uadid} (this item will not go to any pipeline)\033[0m")
                
                continue

            img = listing.css("div[class='uad-col uad-col-image'] > a > img::attr(src)").get()
            product_url = listing.css("div[class='uad-col uad-col-title'] > h1 > a::attr(href)").get()

            yield response.follow(
                product_url,
                callback=self.parse_product,
                meta={
                    'data_uadid': data_uadid,
                    'iced_status': iced_status,
                    'price': price,
                    'img': img,
                }
            )

        next_page = response.css('li.nav-arrow a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        data_uadid = response.meta.get('data_uadid')
        iced_status = response.meta.get('iced_status')
        price = response.meta.get('price')
        img = response.meta.get('img')

        title = response.css('head title::text').get()
        category_div = response.css("div.container > div > ol.breadcrumb")
        category_text = category_div.xpath('string(.)').get().replace("\t", " ").replace("\n", " ").replace("  ", " ").replace("  ", "/").strip()

        seller = response.css('td > b > a[style][href]::text').get()
        seller_profile_url_relativ = response.css('td > b > a[style][href]::attr(href)').get()
        seller_profile_url_absolute = response.urljoin(seller_profile_url_relativ)
        seller_rating_div = response.css("a[class='uad-rating-link']")
        seller_rating = seller_rating_div.xpath('string(.)').get()

        location_delivery_div = response.css("div[class='uad-time-location']")
        location_delivery_data = location_delivery_div.xpath('string(.)').get()
        location_delivery_data = location_delivery_data.split('\n\t\t\t\t\n\t\t\t\t\n\t\t\t\t\t\n\t\t\t\t\t')
        location = location_delivery_data[0].replace("\n", "").replace("\t", "").strip()
        delivery_options = location_delivery_data[1].replace("\n", "").replace("\t", "").strip()

        listed_at = response.css('span[title][data-toggle="tooltip"]::text').get().strip()

        description_div = response.css('div.uad-content div.rtif-content')
        description_text = description_div.xpath('string(.)').get()

        scraper_item = ScraperItem()

        scraper_item['site'] = "HardverApró"
        scraper_item['category'] = category_text
        scraper_item['id'] = data_uadid
        scraper_item['iced_status'] = iced_status
        scraper_item['price'] = price
        scraper_item['img'] = img
        scraper_item['currency'] = "HUF"
        scraper_item['title'] = title
        scraper_item['seller'] = seller
        scraper_item['seller_rating'] = seller_rating
        scraper_item['seller_profile_url'] = seller_profile_url_absolute
        scraper_item['location'] = location
        scraper_item['delivery_options'] = delivery_options
        scraper_item['listed_at'] = listed_at
        scraper_item['listing_url'] = response.url
        scraper_item['description'] = description_text
        scraper_item['scraped_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield scraper_item