import scrapy
from ..items import ScraperMovieItem


class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

    def parse(self, response):
        category_block = response.xpath(
            "//h2[contains(text(), 'Фильмы по алфавиту')]/following-sibling::div[@class='mw-content-ltr'][1]"
        )

        self.logger.info(f"Parsing page: {response.url}")

        for movie in category_block.xpath(
            ".//div[@class='mw-category-group']//ul/li/a"
        ):
            movie_link = response.urljoin(movie.attrib["href"])
            self.logger.info(f"Found movie link: {movie_link}")

            yield response.follow(movie_link, self.parse_movie)

        next_page = response.xpath(
            "//a[contains(text(), 'Следующая страница')]/@href"
        ).get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Following next page: {next_page_url}")

            yield response.follow(next_page_url, self.parse)

    def parse_movie(self, response):
        item = ScraperMovieItem()

        item["title"] = self.extract_text(
            response,
            """
            //table[contains(@class, 'infobox')]//th[@class='infobox-above']/text() |
            //table[contains(@class, 'infobox')]//th[@class='infobox-above']//span//text()
            """.strip(),
            "title",
        )
        item["genre"] = self.extract_text(
            response,
            """
            //table[contains(@class, 'infobox')]//th[contains(., 'Жанр') or contains(., 'Жанры')]/following-sibling::td//a/text() |
            //table[contains(@class, 'infobox')]//th[contains(., 'Жанр') or contains(., 'Жанры')]/following-sibling::td//span[contains(@class, "no-wikidata")]/text()
            """.strip(),
            "genre",
        )
        item["director"] = self.extract_text(
            response,
            """
            //table[contains(@class, 'infobox')]//th[contains(text(), 'Режиссёр') or contains(text(), 'Режиссёры')]/following-sibling::td//a//text() |
            //table[contains(@class, 'infobox')]//th[contains(text(), 'Режиссёр') or contains(text(), 'Режиссёры')]/following-sibling::td//span[contains(@class, "no-wikidata")]//text()
            """.strip(),
            "director",
        )
        item["country"] = self.extract_text(
            response,
            """
            //table[contains(@class, 'infobox')]//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//a/text() |
            //table[contains(@class, 'infobox')]//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//span[@data-sort-value]/@data-sort-value |
            //table[contains(@class, 'infobox')]//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//span[contains(@class, "no-wikidata")]/text() |
            //table[contains(@class, 'infobox')]//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td/text()
            """.strip(),
            "country",
        )
        item["year"] = self.extract_text(
            response,
            """
            //table[contains(@class, 'infobox')]//th[contains(text(), 'Год') or contains(text(), 'Дата')]/following-sibling::td//text() |
            //table[contains(@class, 'infobox')]//th[contains(text(), 'Год') or contains(text(), 'Дата')]/following-sibling::td//a[contains(@title, 'год')]//text()
            """.strip(),
            "year",
        )

        yield item

    def extract_text(self, response, xpath, field_name):
        self.logger.debug(f"Extracting {field_name} using xpath: {xpath}")

        extracted = response.xpath(xpath).getall()
        if not extracted:
            self.logger.warning(
                f"No data found for {field_name} on page: {response.url}"
            )
        return extracted
