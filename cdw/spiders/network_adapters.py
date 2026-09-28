import scrapy
from scrapy import Request
from cdw.items import CdwProductItem
import uuid
from datetime import datetime, timezone

class CdwNetworkAdaptersSpider(scrapy.Spider):
    """
    Scrapes CDW's network-adapters search results (all pages) and follows
    each product link to pick up detail-page data.

    Structure follows the usual three-method pattern:
      start_requests -> parse -> parse_details
    """

    name = "cdw_network_adapters"
    allowed_domains = ["cdw.com"]
    start_urls = [
        "https://www.cdw.com/search/networking/network-adapters/?w=RB&pcurrent=1"
    ]

    dev = "Sudha" 

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        },
    }

    # ------------------------------------------------------------------ #
    # 1. start_requests
    # ------------------------------------------------------------------ #
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # ------------------------------------------------------------------ #
    # 2. parse — one product block per iteration + pagination
    # ------------------------------------------------------------------ #
    def parse(self, response):
        blocks = response.css("div.search-result.coupon-check")
        self.logger.info("Found %d product blocks on %s", len(blocks), response.url)

        for block in blocks:
            item = self.parse_result_block(block, response)
            if item.get("product_url"):
                yield scrapy.Request(
                    item["product_url"],
                    callback=self.parse_details,
                    cb_kwargs={"item": item},
                )
            else:
                # No detail URL to follow — yield what the listing gave us
                self.logger.warning(
                    "No product_url for product_code=%s, yielding listing-only item",
                    item.get("product_code"),
                )
                yield item

        yield from self.follow_pagination(response)

    def parse_result_block(self, block, response):
        item = CdwProductItem()
        item["dev"] = self.dev
        item["scraped_from"] = response.url

        item["run_id"] = str(uuid.uuid4())
        item["scraped_at"] = datetime.now(timezone.utc).isoformat()
        item["schema_version"] = "1.0"

        # --- identifiers (data-* attributes on the block itself) ---
        try:
            item["product_code"] = block.attrib.get("data-product-code")
        except Exception as e:
            self.logger.warning("product_code extraction failed: %s", e)

        try:
            item["brand_code"] = block.attrib.get("data-brand-code")
        except Exception as e:
            self.logger.warning("brand_code extraction failed: %s", e)

        try:
            item["web_class"] = block.attrib.get("data-web-class")
        except Exception as e:
            self.logger.warning("web_class extraction failed: %s", e)

        try:
            item["sort_rank"] = block.attrib.get("data-sort-rank")
        except Exception as e:
            self.logger.warning("sort_rank extraction failed: %s", e)

        try:
            item["is_dropship"] = block.attrib.get("data-dropship") == "1"
        except Exception as e:
            self.logger.warning("is_dropship extraction failed: %s", e)

        # --- name + url + image ---
        try:
            item["product_name"] = (
                block.css("a.search-result-product-url::text").get(default="").strip()
            )
        except Exception as e:
            self.logger.warning("product_name extraction failed: %s", e)

        try:
            relative_url = block.css("a.search-result-product-url::attr(href)").get()
            item["product_url"] = response.urljoin(relative_url) if relative_url else None
        except Exception as e:
            self.logger.warning("product_url extraction failed: %s", e)
            item["product_url"] = None

        try:
            image_src = block.css("a.search-result-product-image img::attr(src)").get()
            item["image_url"] = response.urljoin(image_src) if image_src else None
        except Exception as e:
            self.logger.warning("image_url extraction failed: %s", e)

        # --- mfg / cdw codes ---
        try:
            item["mfg_code"] = (
                block.css("span.mfg-code::text").get(default="")
                .replace("MFG#:", "")
                .strip()
            )
        except Exception as e:
            self.logger.warning("mfg_code extraction failed: %s", e)

        try:
            item["cdw_code"] = (
                block.css("span.cdw-code::text").get(default="")
                .replace("CDW#:", "")
                .strip()
            )
        except Exception as e:
            self.logger.warning("cdw_code extraction failed: %s", e)

        # --- quick specs shown in the listing (key/value pairs) ---
        try:
            headers = block.css(
                ".expanded-specs .product-spec-listing .product-spec-header::text"
            ).getall()
            values = block.css(
                ".expanded-specs .product-spec-listing .product-spec-value::text"
            ).getall()
            item["list_specs"] = {
                h.strip().rstrip(":"): v.strip()
                for h, v in zip(headers, values)
                if h.strip()
            }
        except Exception as e:
            self.logger.warning("list_specs extraction failed: %s", e)
            item["list_specs"] = {}

        # --- pricing ---
        try:
            msrp_text = "".join(
                block.css(".price-msrp.single::text").getall()
            ).strip()
            item["price_msrp"] = msrp_text or None
        except Exception as e:
            self.logger.warning("price_msrp extraction failed: %s", e)
            item["price_msrp"] = None

        try:
            advertised = block.css(".price-type-price::text").get()
            if advertised and advertised.strip():
                item["price_advertised"] = advertised.strip()
                item["price_type"] = "advertised"
            elif block.css(".price-type-request"):
                item["price_advertised"] = None
                item["price_type"] = "request_pricing"
            else:
                item["price_advertised"] = None
                item["price_type"] = "unknown"
        except Exception as e:
            self.logger.warning("pricing extraction failed: %s", e)
            item["price_advertised"] = None
            item["price_type"] = "unknown"

        # --- rating / reviews ---
        try:
            item["rating_review_count"] = block.css(
                ".rating_review-count-value::text"
            ).get()
        except Exception as e:
            self.logger.warning("rating_review_count extraction failed: %s", e)

        # --- stock / shipping (custom elements: text sits alongside the
        #     shadow-dom <template>, as direct light-DOM text of <ui-text>) ---
        try:
            item["stock_status"] = (
                block.css(".component-l0 ui-text::text").get(default="").strip()
                or None
            )
        except Exception as e:
            self.logger.warning("stock_status extraction failed: %s", e)

        try:
            shipping_lines = block.css(".component-l1 ui-text::text").getall()
            item["shipping_info"] = (
                " ".join(s.strip() for s in shipping_lines if s.strip()) or None
            )
        except Exception as e:
            self.logger.warning("shipping_info extraction failed: %s", e)

        return item

    # ------------------------------------------------------------------ #
    # 3. parse_details — enrich each item from its own product page
    # ------------------------------------------------------------------ #
    def parse_details(self, response, item):
        """
        IMPORTANT (flagging rather than guessing silently): I only had the
        search-results HTML to work from, not a real CDW product-detail
        page. The selectors below are a best-effort guess at CDW's typical
        "Technical Specifications" table / description block layout, and
        have NOT been validated against live markup. Before you rely on
        detail_specs / description, view-source a real product page (e.g.
        https://www.cdw.com/product/.../7904020) and confirm or correct the
        CSS selectors in this method.
        """
        try:
            spec_rows = response.css(
                "#TS tr, .tech-specs-table tr, "
                "div[id*='Specification'] .prod-spec-row"
            )
            detail_specs = {}
            for row in spec_rows:
                cells = [c.strip() for c in row.css("::text").getall() if c.strip()]
                if len(cells) >= 2:
                    detail_specs[cells[0]] = " ".join(cells[1:])
            item["detail_specs"] = detail_specs
        except Exception as e:
            self.logger.warning("detail_specs extraction failed: %s", e)
            item["detail_specs"] = {}

        try:
            desc_text = " ".join(
                t.strip()
                for t in response.css(
                    ".product-description ::text, #productOverview ::text"
                ).getall()
                if t.strip()
            )
            item["description"] = desc_text or None
        except Exception as e:
            self.logger.warning("description extraction failed: %s", e)
            item["description"] = None

        yield item

    # ------------------------------------------------------------------ #
    # Pagination — follow the "Next Page" link until it disappears
    # ------------------------------------------------------------------ #
    def follow_pagination(self, response):
        try:
            next_href = response.css("a[aria-label='Next Page']::attr(href)").get()
        except Exception as e:
            self.logger.warning("pagination extraction failed: %s", e)
            next_href = None

        if next_href:
            next_url = response.urljoin(next_href)
            self.logger.info("Following pagination -> %s", next_url)
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            self.logger.info("No further pagination link found on %s — stopping.", response.url)