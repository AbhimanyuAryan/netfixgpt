import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import unquote


def scrape_movie_data(year):
    if not os.path.exists("./brutil/tmp"):
        os.makedirs("./brutil/tmp")
    
    wiki_url = f'https://pt.wikipedia.org/wiki/Categoria:Filmes_do_Brasil_de_{year}'  

    response = requests.get(wiki_url)
    
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        pages_div = soup.find('div', id='mw-pages')
        data = []
        
        if pages_div:

            category_groups = pages_div.find_all('div', class_='mw-category-group')

            for group in category_groups:
                items = group.find_all('li')

                for item in items:
                    link = item.find('a')

                    if link:
                        href = link.get('href')
                        data.append((unquote(href), link.text.strip())
            )

            for url,title in data:
                print(f"{year} - {url}")
                response = requests.get('https://pt.wikipedia.org' + url)
                if response.status_code == 200:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    json_filename = f"{title.replace('/', '-')}.json"
                    page_content = soup.get_text()
                    page_data = {
                        "title": title,
                        "content": page_content
                    }
                    with open(os.path.join("./brutil/tmp", json_filename), "w", encoding='utf-8') as file:
                        json.dump(page_data, file, ensure_ascii=False, indent=4)
                else:
                    print("Error:", response.status_code)
        
    
         

        

    
for year in range(2020, 2025):
    print(f"================={year}====================")
    scrape_movie_data(year)


print("Completed! :)")