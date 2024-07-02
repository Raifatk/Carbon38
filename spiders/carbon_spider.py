
import scrapy

class Carbon38Spider(scrapy.Spider):
    name = "carbon38"
    start_urls = ['https://carbon38.com/en-in/collections/tops?filter.p.m.custom.available_or_waitlist=1',
                  'https://carbon38.com/en-in/collections/carbon38?filter.p.m.custom.available_or_waitlist=1',
                  'https://carbon38.com/en-in/collections/tennis?filter.p.m.custom.available_or_waitlist=1',
                  'https://carbon38.com/en-in/collections/best-sellers-today?filter.p.m.custom.available_or_waitlist=1',
                 ]

    custom_settings = {
        'FEEDS': {
            'items.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': [
                    'image_url', 'brand', 'product_name','price', 'reviews', 'color_options', 'size_options',
                    'description'
                ],
                'indent': 4,
            },
        },
    }

    def parse(self, response):
        # Extract product links from the current page
        product_links = response.css('a.ProductItem__ImageWrapper::attr(href)').getall()
        for link in product_links:
            yield response.follow(link, self.parse_product)

        # Follow pagination links to next pages
        next_page = response.css('div.Pagination__Nav a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        image_url = response.css('img.Image--fadeIn::attr(src)').get()
        brand = response.css('h2.ProductMeta__Vendor.Heading.u-h1 a::text').get()
        product_name = response.css('h1.ProductMeta__Title.Heading.u-h3::text').get()
        price = response.css('span.ProductMeta__Price.Price::text').get()
        
        reviews = response.css('span.ProductItem__Reviews::text').get()
        if not reviews:
            reviews = "No reviews available"
        
        color_options = response.css('label.ColorSwatch::attr(data-tooltip)').getall()
        
        size_options = response.css('label.SizeSwatch')
        sizes = []
        seen_sizes = set()
        for option in size_options:
            size_label = option.css('::text').get().strip()
            if size_label not in seen_sizes:
                seen_sizes.add(size_label)
                sizes.append({'label': size_label})

        description = response.css('div.Faq__ItemWrapper span::text').get()
        
        yield {
            'image_url': image_url,
            'brand': brand,
            'product_name': product_name,
            'price': price,
            'reviews': reviews,
            'color_options': color_options,
            'size_options': sizes,
            'description': description,
        }
