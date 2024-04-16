import requests
from bs4 import BeautifulSoup

# Initialize an empty list to store the movie links
movie_links = []

# Iterate over the years from 2020 to 2024
for year in range(2020, 2025):
    # Generate the URL for the Wikipedia page of the corresponding year
    url = f"https://en.wikipedia.org/wiki/List_of_Hindi_films_of_{year}"

    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables with class 'wikitable' in the HTML content
    wikitables = soup.find_all('table', class_='wikitable')

    # Iterate through each table
    for table in wikitables:
        # Find all table rows (tr) within the table
        rows = table.find_all('tr')
        # Iterate through each row
        for row in rows:
            # Find the first table data (td) element within the row that contains an <a> tag
            first_td_with_a = row.find(lambda tag: tag.name == 'td' and tag.find('a'))
            if first_td_with_a:
                # Find the first <a> tag within the <td> and append its href attribute to the movie_links list
                first_a_tag = first_td_with_a.find('a')
                if first_a_tag:
                    movie_links.append(first_a_tag['href'])

# Print the movie links
for link in movie_links:
    print(link)
