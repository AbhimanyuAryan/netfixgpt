import os
import requests
from bs4 import BeautifulSoup

def get_movies(start: int, end: int):
    """
    Fetch movie data from Wikipedia for the given range of years.

    Params:
        start: Starting year.
        end: Ending year.

    Returns:
        DataFrame containing movie titles and their Wikipedia links.
    """
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    movie_data = []

    for year in range(start, end + 1):
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
                        movie_link = first_a_tag['href']
                        movie_title = first_a_tag.text.strip()
                        movie_data.append({
                            "title": movie_title,
                            "link": f"https://en.wikipedia.org{movie_link}"
                        })

    return pd.DataFrame(movie_data)