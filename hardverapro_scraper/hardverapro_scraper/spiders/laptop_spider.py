import scrapy

class LaptopSpider(scrapy.Spider):
    name = "laptop"
    start_urls = [
        "https://hardverapro.hu/aprok/notebook/index.html",
    ]

    def parse(self, response):
        listings = response.css('ul.list-unstyled > li[class]')
        
        for listing in listings:
            data_uadid = listing.attrib.get('data-uadid')
            iced_status = listing.css("div[class='uad-col uad-col-price'] div::attr(class)").get()
            if iced_status == "uad-price uad-price-iced":
                iced_status = True
            elif iced_status == "uad-price":
                iced_status = False
            price = listing.css("div[class='uad-col uad-col-price'] span::text").get()
            if price == "Keresem":
                continue

            product_url = listing.css("div[class='uad-col uad-col-title'] > h1 > a::attr(href)").get()

            yield response.follow(
                product_url,
                callback=self.parse_product,
                meta={
                    'data_uadid': data_uadid,
                    'iced_status': iced_status,
                    'price': price,
                }
            )

        next_page = response.css('li.nav-arrow a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        data_uadid = response.meta.get('data_uadid')
        iced_status = response.meta.get('iced_status')
        price = response.meta.get('price')

        title = response.css("head title::text").get()
        seller = response.css("td > b > a[style][href]::text").get()
        seller_profile_url_relativ = response.css("td > b > a[style][href]::attr(href)").get()
        seller_profile_url_absolute = response.urljoin(seller_profile_url_relativ)
        listed_at = response.css('span[title][data-toggle="tooltip"]::text').get().strip()

        description_div = response.css('div.uad-content div.rtif-content')
        description_text = description_div.xpath('string(.)').get()


        yield {
            'data_uadid': data_uadid,
            'iced_status': iced_status,
            'price': price,
            'title': title,
            'seller': seller,
            'seller_profile_url': seller_profile_url_absolute,
            'listed_at': listed_at,
            'listing_url': response.url,
            'description': description_text,
        }


# FEAT: if id is in a set, then only check attributes that are collected before the request
# and do not send the request at all (dont go to product page)