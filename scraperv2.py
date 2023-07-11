import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import time
import logging
import pyscopg2

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file]
    return urls

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

def save_data(departamento):
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="postgres",
            user="xbz",
            password="1234"
        )
        cur = conn.cursor()
        # Inserta en la tabla Departamentos
        cur.execute("""
            INSERT INTO Departamentos (titulo, descripcion, precio, ubicacion_id, dormitorios, banios, area) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_departamento
        """, (departamento['titulo'], departamento['descripcion'], departamento['precio'], departamento['ubicacion_id'], 
              departamento['dormitorios'], departamento['banios'], departamento['area']))
        id_departamento = cur.fetchone()[0]
        # Inserta en la tabla Ubicaciones si no existe
        cur.execute("""
            INSERT INTO Ubicaciones (id_ubicacion, nombre) 
            VALUES (%s, %s)
            ON CONFLICT (id_ubicacion) DO NOTHING
        """, (departamento['ubicacion_id'], departamento['ubicacion_nombre']))

        # Inserta en las tablas Amenidades y Departamento_Amenidad
        for amenidad in departamento['amenidades']:
            cur.execute("""
                INSERT INTO Amenidades (nombre) 
                VALUES (%s)
                ON CONFLICT (nombre) DO UPDATE SET nombre = excluded.nombre
                RETURNING id_amenidad
            """, (amenidad,))
            
            id_amenidad = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO Departamento_Amenidad (id_departamento, id_amenidad) 
                VALUES (%s, %s)
            """, (id_departamento, id_amenidad))
        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        return None
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
urls_file_path = 'urls.txt'  # Replace with your file path
urls = read_urls_from_file(urls_file_path)
for url in urls:
    scrape_website(url)

