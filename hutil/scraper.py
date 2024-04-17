import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import unquote

def extract_movie_details(url):

    """
    This function takes in a url for a movie's wikipedia page then extracts
    all the movie's details into a dictionary
    """ 
    #extract web site content
    html = requests.get(url)    
    
    if html.status_code == 200:
        #create a soup object with html data
        soup = BeautifulSoup(html.content,features='html.parser')   
        #Removes all the superscript tags
        for tag in soup.find_all("sup"):
          tag.decompose()   
        #find the info-box element
        info_box = soup.find('table',{'class':'infobox vevent'})

        #extract all rows from info box table
        if not info_box:
            return None
        rows = info_box.find_all('tr')  
        #create empty dictionary to store movie info
        movie_info = {} 
        #loop through every row
        for index,row in enumerate(rows):

          #retrieve movie title from first row
          if index == 0:
            movie_info["Title"] = row.find("th").getText()

          else:
            #check every other row for a header tag
            header = row.find('th')
            if header:
              #assign the <th> element as a dictionary key
              key = row.find('th').getText(" ")
              if row.find('td'):
                #assign <td> elements as the value
                value = row.find("td").getText(" ").replace("\xa0","")
              else:
                #if it's  an <li> element, create list with all items and assign as the value
                value = [item.getText() for item in row.find_all('li')]

              #assign the value variable as the dictionary value
              movie_info[key] = value   

        h2_elements = soup.find_all('h2')
        sections = ["Plot", "Cast", "Production", "Release", "Reception"]
        selected_h2_tags = [h2 for h2 in h2_elements if any(sec.lower() in h2.text.lower() for sec in sections)]


        for h2 in selected_h2_tags:

            title = h2.text.strip().replace("[edit]", "")

            paragraphs = []

            next_sibling = h2.find_next_sibling()

            while next_sibling and next_sibling.name != 'h2':

                if next_sibling.name == 'p':

                    paragraphs.append(next_sibling.text.strip())
                elif next_sibling.name == 'ul':
                    paragraphs.extend([li.text.strip() for li in next_sibling.find_all('li')])

                next_sibling = next_sibling.find_next_sibling()

            movie_info[title] = paragraphs

        return movie_info
    else:
        return None


def scrape_movie_data(year):
    if not os.path.exists("./hutil/tmp"):
        os.makedirs("./hutil/tmp")
    
    wiki_url = f'https://en.wikipedia.org/wiki/List_of_American_films_of_{year}'  

    response = requests.get(wiki_url)
    
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')


        tables = soup.find_all('table')
        # Initialize an empty list to store the DataFrames
        data = []
        for table in tables[2:6]:
            for row in table.find_all('tr'):
                cells = row.find_all('td')

                for cell in cells:

                    if cell.find('i') and cell.find('a'):
                        link = cell.find('i').find('a')
                        data.append(
                            (unquote(link['href']), cell.text.strip())
                            )

        for url,title in data:
            print(f"{year} - {url}")
            info_movie  = extract_movie_details('https://en.wikipedia.org' + url)
            if info_movie is not None:
                json_filename = f"{title.replace('/', '-')}.json"
                with open(os.path.join("./hutil/tmp", json_filename), "w") as file:
                    json.dump(info_movie, file, indent=4)
        
    
         

        

    
for year in range(2020, 2025):
    scrape_movie_data(year)


print("Completed! :)")