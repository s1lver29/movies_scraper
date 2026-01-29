# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import logging
from atexit import register
from re import compile, match, sub

from itemadapter import ItemAdapter
from scrapy import Spider

from .items import ScraperMovieItem


class FilterPipeline:
    def __init__(self):
        pass
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.logger.debug("Start cleaning data for movie: %s", item.get("title"))

        adapter["title"] = self.clean_title(adapter.get("title", ""))
        adapter["genre"] = self.clean_list(adapter.get("genre", []))
        adapter["director"] = self.clean_list(adapter.get("director", []))
        adapter["country"] = self.clean_list(adapter.get("country", []))
        adapter["year"] = self.extract_max_year(adapter.get("year", []))

        self.logger.info("Cleaned data: %s", adapter.asdict())

        return adapter.item

    def clean_title(self, value):
        """Cleans the title by converting a list to a string."""
        self.logger.debug("Processing clening title: %s", value)

        if isinstance(value, list):
            clean_value = " ".join(value).strip()
        else:
            clean_value = value.strip()

        self.logger.debug("Cleaned title: %s", clean_value)
        return clean_value

    def clean_list(self, values):
        """emoves unnecessary characters and returns a cleaned list of values."""
        self.logger.debug("Processing cleaning list: %s", values)
        if not isinstance(values, list):
            values = [values]

        cleaned_values = []
        for value in values:
            clean_value = sub(
                r"[^\w\s-]", "", sub(r"\[.*?\]|\(.*?\)", "", value)
            ).strip()
            if clean_value and not match(r"^\[.*\]$|(\d+)", clean_value):
                cleaned_values.append(clean_value)

        self.logger.debug("Cleaned list: %s", cleaned_values)
        return cleaned_values

    def extract_max_year(self, values):
        """Extracts the year and returns the maximum one."""
        self.logger.debug("Processing extract year: %s", values)

        year_pattern = compile(r"\b(?:15|16|17|18|19|20)\d{2}\b")

        years = []
        for value in values:
            found_years = year_pattern.findall(value)
            years.extend(map(int, found_years))

        max_year = max(years, default=None)
        if max_year:
            self.logger.debug("Extracted max year: %d", max_year)
        else:
            self.logger.warning("No valid years found. Returning None.")

        return max_year


class MoviesSavePipeline:
    def __init__(self):
        self.file = open("movies.csv", mode="w+", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=ScraperMovieItem.fields.keys(),
            delimiter=";",
        )
        self.writer.writeheader()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        register(self.close_file)

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Writes data to a file."""
        self.logger.info(f"Writing movie to file: {item['title']}")

        try:
            self.writer.writerow(item)
            self.logger.debug(f"Movie written to file: {item['title']}")
        except Exception as e:
            self.logger.error(
                f"Error writing movie to file: {item['title']}. Error: {e}"
            )

        return item

    def close_spider(self, spider: Spider):
        """Closes the file after the spider finishes processing."""
        self.logger.info("Closing file and spider.")
        self.close_file()

    def close_file(self):
        """Ensures the file is closed even if the script exits unexpectedly."""
        if not self.file.closed:
            self.logger.info("Closing file due to script exit.")
            self.file.close()
