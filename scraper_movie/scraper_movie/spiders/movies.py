import logging
from typing import Generator

import scrapy
from scrapy.http import Response

from ..items import ScraperMovieItem


class MoviesSpider(scrapy.Spider):
    name: str = "movies"
    allowed_domains: list[str] = ["ru.wikipedia.org", "imdb.com"]

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

        logging.info("Parsing page: %s", response.url)

        movie_links = category_block.xpath(
            ".//div[@class='mw-category-group']/ul/li/a/@href"
        ).getall()

        if movie_links:
            # Process first movie
            first_movie_link = response.urljoin(movie_links[0])
            remaining_movies = movie_links[1:]  # Remaining movies to parse

            # Continue processing the remaining movies after the first one
            yield from self.process_movie_links(
                first_movie_link, remaining_movies, response
            )

        # Check for next page and continue parsing
        next_page = response.xpath(
            "//a[contains(text(), 'Следующая страница')]/@href"
        ).get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            logging.info("Following next page: %s", next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def process_movie_links(
        self, first_movie_link: str, remaining_movies: list, response: Response
    ) -> Generator[scrapy.Request, None, None]:
        """Helper method to process movie links and pass them to parse_movie."""
        # Process first movie
        yield scrapy.Request(
            url=first_movie_link,
            callback=self.parse_movie,
            meta={
                "remaining_movies": remaining_movies,
                "next_page": response.meta.get("next_page"),
            },
            priority=1,  # FIFO processing
        )

        # Process remaining movies
        for next_movie in remaining_movies:
            yield scrapy.Request(
                url=response.urljoin(next_movie),
                callback=self.parse_movie,
                meta={
                    "remaining_movies": remaining_movies[1:],
                    "next_page": response.meta.get("next_page"),
                },
                priority=1,
            )

    def parse_movie(self, response: Response) -> Generator[scrapy.Request, None, None]:
        """Parse individual movie details and follow IMDb link if available."""
        item = ScraperMovieItem()

        # Extract fields using XPATHs
        for field, xpath in self.XPATHS.items():
            item[field] = self.extract_text(response, xpath, field)

        # Check for IMDb link
        imdb_link = response.xpath(
            f"{self.BASE_PATH}//td//span/a[contains(@href, 'imdb.com/title')]/@href"
        ).get()
        if imdb_link:
            imdb_id = imdb_link.split("/")[-2]
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
            logging.info("Found IMDb link for movie: %s", imdb_url)

            yield scrapy.Request(
                imdb_url,
                callback=self.parse_imdb_rating,
                meta={"item": item},
                priority=2,  # IMDb processing priority
            )
        else:
            logging.warning("No IMDb link found for movie.")

            # Return the item after parsing (with or without IMDb rating)
            yield item

        # If there are more movies left, continue processing
        remaining_movies = response.meta.get("remaining_movies", [])
        if remaining_movies:
            next_movie = response.urljoin(remaining_movies[0])
            yield scrapy.Request(
                next_movie,
                callback=self.parse_movie,
                meta={
                    "remaining_movies": remaining_movies[1:],
                    "next_page": response.meta.get("next_page"),
                },
                priority=1,
            )

    def parse_imdb_rating(self, response):
        item = response.meta["item"]

        imdb_rating = response.xpath(
            "//div[contains(text(), 'IMDb RATING')]/following-sibling::a//div[contains(@data-testid, 'rating')]/span/text()"
        ).get()
        if imdb_rating:
            item["imdb_rating"] = imdb_rating.strip()
            logging.info("Extracted IMDb rating: %s", imdb_rating)
        else:
            logging.warning("No IMDb rating found for movie %s", item["title"])

        yield item

    def extract_text(
        self, response: Response, xpath: str, field_name: str
    ) -> list[str]:
        # logging.debug("Extracting %s using xpath: %s", field_name, xpath)

        extracted = response.xpath(xpath).getall()
        if not extracted:
            logging.warning(
                "No data found for %s on page: %s", field_name, response.url
            )
        return extracted
