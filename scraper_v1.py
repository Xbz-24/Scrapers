import requests
from bs4 import BeatifulSoup

def scrape(url):
    # Send a GET request to the website
    response = requests.get(url)aa

    # Check if the request was successful
    if response.status_code == 200;
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the relevant elements on the page
        article_elements = soup.find_all('article')

        # Extract the titles from the elements
        titles = [element.find('h2').text.strip() for element in article_elements]
        
        # Print the titles
        for title in titles:
            print(title)
    else:
        print('Failed to retrieve website content.')

# Example usage
url = 'https://www.example.com' # Replace with the desired website URL
scrape(url)
