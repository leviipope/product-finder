import scrapy
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.db import get_connection


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

    def start_requests(self):
        with get_connection() as conn:

            conn.row_factory = lambda cursor, row: {col[0]: row[i] for i, col in enumerate(cursor.description)}
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    SELECT l.id, l.listing_url
                    FROM listings l
                    JOIN verification_queue v ON l.id = v.id
                    WHERE l.archived_at IS NULL
                """)
                rows = cursor.fetchall()
            except Exception as e:
                self.logger.error(f"Failed to fetch listings for verification: {e}")
                self.logger.error("Verification queue may be empty.")
                return
            
            if not rows:
                self.logger.info("No listings found in the verification queue.")
                conn.close()
                return
            
            for row in rows:
                yield scrapy.Request(
                    url=row['listing_url'],
                    callback=self.parse,
                    meta={'id': row['id'], 'listing_url': row['listing_url']},
                )

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

