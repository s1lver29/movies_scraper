from typing import Generator

import scrapy
from scrapy.http import Response

from ..items import ScraperMovieItem


class MoviesSpider(scrapy.Spider):
    name: str = "movies"
    allowed_domains: list[str] = ["ru.wikipedia.org"]

    BASE_PATH: str = "//table[contains(@class, 'infobox')]"

    XPATHS: dict[str, str] = {
        "title": f"{BASE_PATH}//th[@class='infobox-above']/text() | {BASE_PATH}//th[@class='infobox-above']//span//text()",
        "genre": f"""
            {BASE_PATH}//th[contains(., 'Жанр') or contains(., 'Жанры')]/following-sibling::td//a/text() |
            {BASE_PATH}//th[contains(., 'Жанр') or contains(., 'Жанры')]/following-sibling::td//span[contains(@class, "no-wikidata")]/text()
            """.strip(),
        "director": f"""
            {BASE_PATH}//th[contains(text(), 'Режиссёр') or contains(text(), 'Режиссёры')]/following-sibling::td//a//text() |
            {BASE_PATH}//th[contains(text(), 'Режиссёр') or contains(text(), 'Режиссёры')]/following-sibling::td//span[contains(@class, "no-wikidata")]//text()
            """.strip(),
        "country": f"""
            {BASE_PATH}//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//a/text() |
            {BASE_PATH}//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//span[@data-sort-value]/@data-sort-value |
            {BASE_PATH}//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td//span[contains(@class, "no-wikidata")]/text() |
            {BASE_PATH}//th[contains(text(), "Страна") or contains(text(), "Страны")]/following-sibling::td/text()
            """.strip(),
        "year": f"""
            {BASE_PATH}//th[contains(text(), 'Год') or contains(text(), 'Дата')]/following-sibling::td//text() |
            {BASE_PATH}//th[contains(text(), 'Год') or contains(text(), 'Дата')]/following-sibling::td//a[contains(@title, 'год')]//text()
            """.strip(),
    }

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        start_url = "https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response: Response) -> Generator[scrapy.Request, None, None]:
        category_block = response.xpath(
            "//h2[contains(text(), 'Фильмы по алфавиту')]/following-sibling::div[@class='mw-content-ltr'][1]"
        )

        self.logger.info(f"Parsing page: {response.url}")

        for movie in category_block.xpath(
            ".//div[@class='mw-category-group']//ul/li/a"
        ):
            self.logger.info(
                f"Found movie link: {response.urljoin(movie.attrib['href'])}"
            )

            yield response.follow(movie.attrib["href"], self.parse_movie)

        next_page = response.xpath(
            "//a[contains(text(), 'Следующая страница')]/@href"
        ).get()
        if next_page:
            self.logger.info(f"Following next page: {response.urljoin(next_page)}")

            yield response.follow(next_page, self.parse)

    def parse_movie(
        self, response: Response
    ) -> Generator[ScraperMovieItem, None, None]:
        item = ScraperMovieItem()

        for item_values in self.XPATHS.keys():
            item[item_values] = self.extract_text(
                response, self.XPATHS[item_values], item_values
            )

        yield item

    def extract_text(
        self, response: Response, xpath: str, field_name: str
    ) -> list[str]:
        self.logger.debug(f"Extracting {field_name} using xpath: {xpath}")

        extracted = response.xpath(xpath).getall()
        if not extracted:
            self.logger.warning(
                f"No data found for {field_name} on page: {response.url}"
            )
        return extracted
