import requests
from bs4 import BeautifulSoup
import json

# URL of the Wikipedia page
page_title = "Shaitaan_(2024_film)"
api_url = f"https://en.wikipedia.org/api/rest_v1/page/html/{page_title}"

# Send a GET request to fetch the HTML content of the page using the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the HTML content from the response
    html_content = response.text
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the text content of the page
    page_content = soup.get_text()
    
    # Create a dictionary to store the page content
    page_data = {
        "title": page_title,
        "content": page_content
    }
    
    # Convert the dictionary to JSON format
    json_data = json.dumps(page_data, indent=4)

    # Save the JSON data to a file
    with open(f"{page_title}.json", "w") as file:
        file.write(json_data)
else:
    print("Error:", response.status_code)
