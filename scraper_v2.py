import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import time
import logging

def send_request(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        return response
    except RequestException as e:
        logging.error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def parse_html(response):
    return BeautifulSoup(response.content, 'html.parser')

def extract_titles(soup):
    article_elements = soup.find_all('article')
    return [element.find('h2').text.strip() for element in article_elements]

def save_data(titles):
    # Here you would write the logic to save your titles, e.g., to a CSV file or database

def scrape_website(url):
    for i in range(3):  # Retry up to 3 times
        response = send_request(url)
        if response is not None:
            soup = parse_html(response)
            titles = extract_titles(soup)
            save_data(titles)
            break
        else:
            time.sleep(2**i)  # Exponential backoff
    else:
        logging.error('Failed to retrieve website content after 3 attempts.')

# Example usage
url = 'https://www.example.com'  # Replace with the desired website URL
scrape_website(url)

