import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.flightaware.com/live/findflight?origin=kphx&destination=klax'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    big_div = soup.find('div', id='ffinder-main')
    div_inside_big_div = big_div.find('div', id='ffinder-results')
    table = div_inside_big_div.find('table', id='Results')
    table_body = table.find('tbody')
    
    allLinks = []
    
    #conditions: the plane must be a B38M AND it must have arrived at the gate 
    for row in table_body.find_all('tr'):
        aircraft_td = row.find('td', class='ffinder-results-aircraft')
        arrived_td = row.find('td', class='ffinder-results-status')
        status = arrived_td.text
        aircraft_type = aircraft_td.text
        if aircraft_td.text == "B38M":
            if "Arrive" in status:
                ident_td = row.find('td', class='ffinder-result-ident')
                ident_span = ident_td.find('span')
                ahref = ident_span.find('a')
                link = ahref['href']
                allLinks.append(link)
                print(link)
    
    dataLinks = []
    
    if allLinks:
        for link in allLinks:
            url = 'https://www.flightaware.com' + link
            response = requests.get(url)
            if response.status_code = 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                nextLink_A = soup.find('a', id='trackLogLink')
                nextLink = nextLink_A['href']
                dataLinks.append(nextLink)
                print(nextLink)
                
        if dataLinks:
            for link in dataLinks:
                url = 'https://www.flightaware.com' + link
                response = requests.get(url)
                
                if response.status_code = 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    data = []
                    
                    table = soup.find('table', id='tracklogTable')
                    table_body = table.find('tbody')
                    rows = table_body.find_all('tr', class=['smallrow1', 'smallrow2']):
                    
                    for row in rows:
                        cells = [cell.text.strip() for cell in row
                
                

            