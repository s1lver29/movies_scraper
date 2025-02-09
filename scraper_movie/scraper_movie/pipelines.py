# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import logging
from atexit import register
from re import match, sub

from itemadapter import ItemAdapter
from scrapy import Spider


class FilterPipeline:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
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
        """Очищает название, превращая список в строку"""
        if isinstance(value, list):
            clean_value = " ".join(value).strip()
        else:
            clean_value = value.strip()

        self.logger.debug("Cleaned title: %s", clean_value)
        return clean_value

    def clean_list(self, values):
        """Удаляет мусор и возвращает список значений."""
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
        """Извлекает только год и выбирает максимальный"""
        years = [int(y) for y in values if y.isdigit() and 1800 <= int(y) <= 2100]
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
            fieldnames=["title", "genre", "director", "country", "year"],
            delimiter=";",
        )
        self.writer.writeheader()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        register(self.close_file)

    def process_item(self, item: dict, spider: Spider) -> dict:
        """Записывает данные в файл."""
        self.logger.info(f"Writing movie to file: {item['title']}")

        try:
            self.writer.writerow(item)
            self.file.flush()
            self.logger.debug(f"Movie written to file: {item['title']}")
        except Exception as e:
            self.logger.error(
                f"Error writing movie to file: {item['title']}. Error: {e}"
            )

        return item

    def close_spider(self, spider: Spider):
        """Закрытие файла после окончания парсинга."""
        self.logger.info("Closing file and spider.")
        self.close_file()

    def close_file(self):
        """Гарантированное закрытие файла даже при аварийном завершении."""
        if not self.file.closed:
            self.logger.info("Closing file due to script exit.")
            self.file.close()
