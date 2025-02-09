# Movie Scraper

A Python-based web scraper for extracting detailed movie information from Wikipedia and IMDb. This project scrapes movie data like the title, genre, director, country, year, and IMDb rating, then saves the data into a CSV file.

## Features
- Scrapes movie details from Wikipedia including:
    - Title
    - Genre
    - Director
    - Country
    - Year
- Extracts IMDb ratings from IMDb movie pages.
- Saves the scraped data to a CSV file.
- Handles pagination of movie lists on the Wikipedia page.

## Requirements
- Python 3.8+
- pdm for managing dependencies.

## Installation
1. Install pdm
If you don't have pdm installed yet, you can install it via pip:
```bash
pip install pdm
```
2. Clone the repository
Clone the repository to your local machine
```bash
git clone https://github.com/s1lver29/movies_scraper/tree/main
cd movies_scraper
```
3. Install dependencies
Install the required dependencies using pdm:
```bash
pdm install
```

## Usage
### Run the Scraper
To start the scraper and collect movie data, use the following command:
```bash
cd scraper_movie
pdm run scrapy crawl movies

```
or
```bash
cd scraper_movie
eval $(pdm venv activate)
scrapy crawl movies
```
### Output
The scraper will collect the following movie information:
- Title
- Genre
- Director
- Country
- Year
- IMDb Rating
```csv
country;director;genre;imdb_rating;title;year
['Франция'];['Жан-Луи Гийерму'];['комедия'];3.4;2 дурня в снегу;1977
```