import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_movie_data():
    # Create a directory named "tmp" if it doesn't exist
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    movie_links = []

    # Iterate over the years from 2020 to 2024
    for year in range(2020, 2025):
        url = f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_{year}"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        wikitables = soup.find_all('table', class_='wikitable')
        for table in wikitables:
            rows = table.find_all('tr')
            for row in rows:
                first_td_with_a = row.find(lambda tag: tag.name == 'td' and tag.find('a'))
                if first_td_with_a:
                    first_a_tag = first_td_with_a.find('a')
                    if first_a_tag:
                        movie_links.append(first_a_tag['href'])

    base_url = "https://en.wikipedia.org"

    for link in movie_links:
        page_url = base_url + link
        response = requests.get(page_url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.find('h1', class_='firstHeading').text
            # Replace '/' character with '-'
            json_filename = f"{title.replace('/', '-')}.json"
            page_content = soup.get_text()
            page_data = {
                "title": title,
                "content": page_content
            }
            with open(os.path.join("tmp", json_filename), "w") as file:
                json.dump(page_data, file, indent=4)
        else:
            print("Error:", response.status_code)
