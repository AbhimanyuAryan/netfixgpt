import os
import requests
from bs4 import BeautifulSoup

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
        # Extract title from the link
        title = link.split('/')[-1]
        title = title.replace('_', ' ')
        # Save PDF file using get_wikipedia_page_as_pdf function
        get_wikipedia_page_as_pdf(title)

def get_wikipedia_page_as_pdf(title, format='a4', type='desktop'):
    base_url = 'https://en.wikipedia.org/api/rest_v1'
    endpoint = f'/page/pdf/{title}/{format}/{type}'
    url = base_url + endpoint

    response = requests.get(url)
    if response.status_code == 200:
        # Save the PDF file in the "tmp" directory
        with open(os.path.join("tmp", f"{title}.pdf"), "wb") as f:
            f.write(response.content)
        print(f"PDF for '{title}' saved successfully.")
    elif response.status_code == 404:
        print(f"Unknown page title: '{title}'.")
    elif response.status_code == 503:
        print("Service queue is busy or full.")
    else:
        print(f"An error occurred for page '{title}': {response.status_code}")

# Call the function to scrape data and save PDF files
scrape_movie_data()
