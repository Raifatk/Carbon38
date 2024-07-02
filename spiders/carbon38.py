import scrapy

class CarbonSpider(scrapy.Spider):
    name = "carbon_spider"
    start_urls = ['https://carbon38.com/en-in/collections/tops?filter.p.m.custom.available_or_waitlist=1',
                  'https://carbon38.com/en-in/collections/carbon38?filter.p.m.custom.available_or_waitlist=1',
                  'https://carbon38.com/en-in/collections/tennis?filter.p.m.custom.available_or_waitlist=1',
                  'https://carbon38.com/en-in/collections/best-sellers-today?filter.p.m.custom.available_or_waitlist=1',
            ]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'DNT': '1',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }
    }

    def parse(self, response):
        for product in response.css('div.ProductItem'):
            yield {
                'title': product.css('h2.ProductItem__Title.Heading a::text').get(),
                'price': product.css('span.ProductItem__Price.Price::text').get().strip(),
                'image_src': product.css('img.ProductItem__Image.ProductItem__Image--alternate::attr(src)').get()
            }

        # Follow pagination links dynamically
        next_page = response.css('div.Pagination__Nav a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
