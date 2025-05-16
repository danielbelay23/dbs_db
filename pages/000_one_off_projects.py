import requests
from bs4 import BeautifulSoup
import time
import random

USERNAME = 'dbtwothree'
BASE_URL = f'https://letterboxd.com/{USERNAME}/films/page/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def get_film_titles_from_page(page_num):
    url = BASE_URL + str(page_num)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch page {page_num}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    films = soup.select('li.poster-container')
    
    film_titles = []
    for film in films:
        film_title = film.get('data-film-name')
        if film_title:
            film_titles.append(film_title.strip())

    return film_titles

def scrape_all_films(max_pages=20):
    all_films = []
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        titles = get_film_titles_from_page(page)
        if not titles:
            break
        all_films.extend(titles)
        time.sleep(random.uniform(1.5, 3.0))  # polite delay
    return all_films

if __name__ == "__main__":
    films = scrape_all_films()
    print(f"Total films scraped: {len(films)}")
    for title in films:
        print(title)
