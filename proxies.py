import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

def scrape_proxies():
    url = "https://free-proxy-list.net/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('table')
    list_proxies = []

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            ip = columns[0].get_text()
            port = columns[1].get_text()
            code = columns[2].get_text()
            country = columns[3].get_text()
            anonymity = columns[4].get_text()
            google = columns[5].get_text()
            https = columns[6].get_text()
            last_checked = columns[7].get_text()

            proxy = {
                'IP Address': ip,
                'Port': port,
                'Code': code,
                'Country': country,
                'Anonymity': anonymity,
                'Google': google,
                'Https': https,
                'Last Checked': last_checked
            }

            list_proxies.append(proxy)

    return list_proxies

def create_proxies_table():
    conn = psycopg2.connect(database="proxies", user="xbz", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()
    
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS proxies (
            id SERIAL PRIMARY KEY,
            ip_address VARCHAR(255),
            port INTEGER,
            code VARCHAR(255),
            country VARCHAR(255),
            anonymity VARCHAR(255),
            google VARCHAR(255),
            https VARCHAR(255),
            last_checked VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    '''
    
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_proxies(proxies):
    conn = psycopg2.connect(database="proxies", user="xbz", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()
    
    with open('proxies.txt', 'w') as file:
        for proxy in proxies:
            ip_address = proxy['IP Address']
            port = proxy['Port']
            code = proxy['Code']
            country = proxy['Country']
            anonymity = proxy['Anonymity']
            google = proxy['Google']
            https = proxy['Https']
            last_checked = proxy['Last Checked']
            
            insert_query = '''
                INSERT INTO proxies (ip_address, port, code, country, anonymity, google, https, last_checked)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            
            cursor.execute(insert_query, (ip_address, port, code, country, anonymity, google, https, last_checked))
            
            file.write(f"{ip_address}\t{port}\t{code}\t{country}\t{anonymity}\t{google}\t{https}\t{last_checked}\n")
    
    conn.commit()
    cursor.close()
    conn.close()

def update_records_timestamp():
    conn = psycopg2.connect(database="proxies", user="xbz", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()

    update_query = '''
        UPDATE proxies
        SET created_at = %s
        WHERE id = (SELECT id FROM proxies ORDER BY created_at DESC LIMIT 1)
    '''

    cursor.execute(update_query, (datetime.now(),))
    conn.commit()
    cursor.close()
    conn.close()

# Usage
proxies = scrape_proxies()
create_proxies_table()
insert_proxies(proxies)
update_records_timestamp()
def truncate_proxies_table():
    conn = psycopg2.connect(database="proxies", user="xbz", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()
    
    truncate_table_query = '''
        TRUNCATE TABLE proxies;
    '''
    
    cursor.execute(truncate_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_proxies(proxies):
    conn = psycopg2.connect(database="proxies", user="xbz", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()
    
    for proxy in proxies:
        ip_address = proxy['IP Address']
        port = proxy['Port']
        code = proxy['Code']
        country = proxy['Country']
        anonymity = proxy['Anonymity']
        google = proxy['Google']
        https = proxy['Https']
        last_checked = proxy['Last Checked']
        
        insert_query = '''
            INSERT INTO proxies (ip_address, port, code, country, anonymity, google, https, last_checked)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        cursor.execute(insert_query, (ip_address, port, code, country, anonymity, google, https, last_checked))
    
    conn.commit()
    cursor.close()
    conn.close()

def update_records_timestamp():
    conn = psycopg2.connect(database="proxies", user="xbz", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()

    update_query = '''
        UPDATE proxies
        SET created_at = %s
        WHERE id = (SELECT id FROM proxies ORDER BY created_at DESC LIMIT 1)
    '''

    cursor.execute(update_query, (datetime.now(),))
    conn.commit()
    cursor.close()
    conn.close()

# Usage
proxies = scrape_proxies()
create_proxies_table()
truncate_proxies_table()
insert_proxies(proxies)
update_records_timestamp()
