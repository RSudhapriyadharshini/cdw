import scrapy


class CdwProductItem(scrapy.Item):
    # --- identifiers (from data-* attributes on the search-result block) ---
    product_code = scrapy.Field()
    mfg_code = scrapy.Field()
    cdw_code = scrapy.Field()
    brand_code = scrapy.Field()
    web_class = scrapy.Field()
    sort_rank = scrapy.Field()
    is_dropship = scrapy.Field()

    # --- core info ---
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()

    # --- quick specs shown directly in the search-result listing ---
    list_specs = scrapy.Field()  # dict: {"Data Link Protocols": "...", ...}

    # --- pricing ---
    price_msrp = scrapy.Field()          # original/struck-through price, may be None
    price_advertised = scrapy.Field()    # discounted/advertised price, may be None
    price_type = scrapy.Field()          # "advertised" | "request_pricing" | "unknown"

    # --- ratings ---
    rating_review_count = scrapy.Field()

    # --- availability ---
    stock_status = scrapy.Field()        # e.g. "In Stock"
    shipping_info = scrapy.Field()       # e.g. "Ships same day if ordered before 2 PM CT"

    # --- detail-page fields (populated in parse_details) ---
    detail_specs = scrapy.Field()        # dict of full technical specifications
    description = scrapy.Field()

    # --- scrape metadata ---
    dev = scrapy.Field()
    scraped_from = scrapy.Field()        # the search-results page URL this came from

    run_id = scrapy.Field()
    scraped_at = scrapy.Field()
    schema_version = scrapy.Field()