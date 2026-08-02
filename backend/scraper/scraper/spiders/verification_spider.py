import scrapy
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.db import get_verification_queue_listings


class VerificationSpiderSpider(scrapy.Spider):
    name = "verifier"

    custom_settings = {
            'DOWNLOAD_DELAY': 0.2,
            'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
            'ROBOTSTXT_OBEY': False,
            'REDIRECT_ENABLED': True,
            'HTTPERROR_ALLOW_ALL': True,
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'COOKIES_ENABLED': False,
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_START_DELAY': 0.5,
            'AUTOTHROTTLE_MAX_DELAY': 10,
            'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            raw_data = get_verification_queue_listings() or []
            self.rows = []

            if hasattr(raw_data, "to_dict"):
                self.rows = raw_data.to_dict("records") # type: ignore
            else:
                for r in raw_data:
                    if isinstance(r, (tuple, list)):
                        self.rows.append({
                            'id': r[0],
                            'listing_url': r[1]
                        })

                    elif isinstance(r, dict):
                        self.rows.append(r)

            self.logger.info(f"\033[92mFetched {len(self.rows)} listings for verification.\033[0m")
        except Exception as e:
            self.logger.error(f"\033[91mFailed to fetch verification queue listings: {e}\033[0m")
            self.rows = []

    def start_requests(self):      
        if not self.rows:
            self.logger.info("No listings found in the verification queue.")
            return
        
        for row in self.rows:
            try:
                url = row.get('listing_url')
                item_id = row.get('id')

                if not url or not str(url).startswith("http"):
                    self.logger.error(f"\033[93mInvalid URL in DB: {url} (ID: {item_id})\033[0m")
                    continue

                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={'id': item_id, 'listing_url': url},
                )

            except Exception as e:
                self.logger.error(f"\033[91mCRASH in start_requests! Row type: {type(row)} | Data: {row}\033[0m")
                self.logger.error(f"\033[91mError: {type(e).__name__} - {e}\033[0m")
                continue

    def parse(self, response):
        data_uadid = response.meta['id']
        listing_url = response.meta['listing_url']
        is_archived = False
        error_message = response.css("h2[class='text-center my-2'] > b::text").get()
        deleted_message = response.css("div[class='uad-content-block text-center flex-column'] > h2[class='m-5']::text").get()

        if response.status in [404, 410]:
            is_archived = True
        elif error_message and "Ez a hirdetés már lejárt!" in error_message:
            is_archived = True
        elif deleted_message and "Törölt hirdetés" in deleted_message:
            is_archived = True

        if is_archived:
            self.logger.info(f"\033[38;5;21m[VERIFIED ARCHIVE] Item {data_uadid} is gone. Archiving. Link: {listing_url}\033[0m")
            yield {
                'id': data_uadid,
                'action': 'archive'
            }
        else:
            self.logger.info(f"\033[38;5;82m[FALSE POSITIVE PREVENTED] Item {data_uadid} is still alive! Link: {listing_url}\033[0m")

