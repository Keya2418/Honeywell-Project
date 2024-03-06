



















#note as of 3/6/2024 14:56
#this entire thing is obselete now because beautifulsoup can't do dynamically loaded content
#it seems like the flight data is loaded in javascript
#anyway now we have to use selenium 
"""
import requests
from bs4 import BeautifulSoup
import csv

counter = 0

url = 'https://www.flightaware.com/live/findflight?origin=kphx&destination=klax'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    big_div = soup.find('div', id='ffinder-main')
    div_inside_big_div = big_div.find('div', id='ffinder-results')
    table = div_inside_big_div.find('table', id='Results')
    table_body = table.find('tbody')
    
    allLinksAndTime = []
    
    #conditions: the plane must be a B38M AND it must have arrived at the gate 
    for row in table_body.find_all('tr'):
        tds = row.find_all('td')
        print(tds)
        
        aircraft_td = row2.find('td', class_=')
        arrived_or_not_td = row2.find('td', class_='ffinder-results-status')
        arrived_or_not_span = arrived_or_not_td.find('span')
        time_departed = row2.find('td', class_='ffinder-results-departure')
        status = arrived_or_not_span.get_text()
        aircraft_type = aircraft_td.get_text()
        print("status:")
        print(status)
        print("aircraft_type:")
        print(aircraft_type)
        if aircraft_td.text == "B38M":
            if "Arrive" in status:
                ident_td = row.find('td', class_='ffinder-result-ident')
                ident_span = ident_td.find('span')
                ahref = ident_span.find('a')
                link = ahref['href']
                allLinks.append([link, time_departed.get_text()])
                print("link:")
                print(link)
        
    
    dataLinksAndTime = []
    
    if allLinksAndTime:
        for link in allLinksAndTime:
            url = 'https://www.flightaware.com' + link[0]
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                nextLink_A = soup.find('a', id='trackLogLink')
                nextLink = nextLink_A['href']
                dataLinksAndTime.append([nextLink, link[1]])
                print("next link, link[1]:")
                print([nextLink, link[1]])
        
        if dataLinksAndTime:
            for link in dataLinksAndTime:
                url = 'https://www.flightaware.com' + link[0]
                response = requests.get(url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    data = []
                    
                    table = soup.find('table', id='tracklogTable')
                    table_body = table.find('tbody')
                    rows = table_body.find_all('tr', class_='smallrow1') + table_body.find_all('tr', class_='smallrow2')
                    
                    for row in rows:
                        cells = [cell.text.strip() for cell in row.find_all(['td'])]
                        
                        if cells:
                            data.append(cells)
                            
                    output_filename = 'PHX_LV_' + counter + link[1]
                    counter+= 1
                    with open (output_filename, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        write.writerows(data)

else:
    print("big fail")
                
"""
            