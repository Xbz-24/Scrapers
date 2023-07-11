import time
import random
from itertools import cycle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import psycopg2

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file]
    return proxies

def save_data(apartment_data):
    conn = psycopg2.connect(
        host="localhost",
        database="apartamentos",
        user="xbz",
        password="1234"
    )
    cursor = conn.cursor()
    
    for apartment in apartment_data:
        location = apartment['location']
        price = apartment['price']
        link = apartment['link']
        last_updated = apartment['last_updated']
        description = apartment['description']
        area = apartment['area']
        bedrooms = apartment['bedrooms']
        bathrooms = apartment['bathrooms']
        amenities = apartment['amenities']
        contact_name = apartment['contact_name']
        contact_email = apartment['contact_email']
        contact_phone = apartment['contact_phone']
        image_url = apartment['image_url']
        
        insert_query = '''
            INSERT INTO apartment_data (
                location, price, link, last_updated, description, area, bedrooms, bathrooms,
                amenities, contact_name, contact_email, contact_phone, image_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        cursor.execute(
            insert_query,
            (
                location, price, link, last_updated, description, area, bedrooms, bathrooms,
                amenities, contact_name, contact_email, contact_phone, image_url
            )
        )
    
    conn.commit()
    cursor.close()
    conn.close()

def real_estate_scraper(urls, proxies):
    # Initialize proxy and user-agent cycles
    proxy_pool = cycle(proxies)
    ua = UserAgent()

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    for url in urls:
        # Change the user-agent for each URL
        chrome_options.add_argument('user-agent=%s' % ua.random)

        # Set a new proxy for each request
        proxy = next(proxy_pool)
        chrome_options.add_argument('--proxy-server=%s' % proxy)

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        time.sleep(5)  # Give JavaScript time to execute

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        apartment_data = []

        for property in soup.find_all('div', class_='property-details'):
            title = property.find('h2').text
            price = property.find('span', class_='price').text
            # Extract other details as per your requirement
            
            # Create a dictionary for the apartment data
            apartment = {
                'location': '',  # Replace with the actual location data
                'price': price,
                'link': '',  # Replace with the actual link data
                'last_updated': '',  # Replace with the actual last updated data
                'description': '',  # Replace with the actual description data
                'area': '',  # Replace with the actual area data
                'bedrooms': '',  # Replace with the actual bedrooms data
                'bathrooms': '',  # Replace with the actual bathrooms data
                'amenities': [],  # Replace with the actual amenities data
                'contact_name': '',  # Replace with the actual contact name data
                'contact_email': '',  # Replace with the actual contact email data
                'contact_phone': '',  # Replace with the actual contact phone data
                'image_url': []  # Replace with the actual image URL data
            }
            
            apartment_data.append(apartment)

        save_data(apartment_data)

        time.sleep(1)  # Sleep for a bit so we don't overload the server
        driver.quit()

# Example usage
urls_file_path = 'websites.txt'  # Replace with your file path
proxies_file_path = 'proxies.txt'  # Replace with your file path
urls = read_urls_from_file(urls_file_path)
proxies = read_proxies_from_file(proxies_file_path)

real_estate_scraper(urls, proxies)
