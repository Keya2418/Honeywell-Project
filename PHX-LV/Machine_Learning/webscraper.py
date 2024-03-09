#WEBSCRAPER FOR LAT LONG ALT TIME

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import re
import os

# the singular function:

def remove_spaces_and_colons(input_string):
    cleaned_string = input_string.replace(' ', '').replace(':', '')
    return cleaned_string

webdriver_path = './geckodriver'

browser = webdriver.Firefox()

url = 'https://www.flightaware.com/live/findflight?origin=kphx&destination=klas'

browser.get(url)

table = browser.find_element(By.ID, 'Results')
table_body = table.find_element(By.TAG_NAME, 'tbody')

#LTA stands for Link, Time, Aircraft 
allLTA = []

##conditions: the plane must be a B38M AND it must have arrived at the gate 

for row in table_body.find_elements(By.CSS_SELECTOR, 'tr.ffinder-results-row-bordertop'):
    aircraft_td = row.find_element(By.CSS_SELECTOR, 'td.ffinder-results-aircraft')
    aircraft = aircraft_td.text
    #print("aircraft: ", aircraft)
    arrived_or_not_td = row.find_element(By.CSS_SELECTOR, 'td.ffinder-results-status')
    status = arrived_or_not_td.text
    #print("status: ", status)
    departure_time_td = row.find_element(By.CSS_SELECTOR, 'td.ffinder-results-departure')
    departure_unclean_text = departure_time_td.text
    #print("departure unclean: ", departure_unclean_text)
    departure = remove_spaces_and_colons(departure_unclean_text)
    #print("departure: ", departure)
    ident_td = row.find_element(By.CSS_SELECTOR, 'td.ffinder-results-ident')
    ident_span = ident_td.find_element(By.TAG_NAME, 'span')
    anchor_tag = ident_span.find_element(By.TAG_NAME, 'a')
    link = anchor_tag.get_attribute('href')
    #these links are gold!! hooray
    #print("link: ", link)
    if "Arrive" in status: 
        #print("arrive is in status")
        if (departure != "" and aircraft != ""):
            allLTA.append([link, departure, aircraft])

            
if allLTA:
    print("\n\n")
    for node in allLTA:
        print("link: ", node[0])
        print("time: ", node[1])
        print("aircraft: ", node[2])
        print("\n")
        
#logLinks = []
        
if allLTA:
    for node in allLTA:
        #linkNotAcquired = True;
        url = node[0]
        browser.get(url)
        try: 
            log_anchor_tag = browser.find_element(By.ID, 'trackLogLink')
            log_link = log_anchor_tag.get_attribute('href')
            print("log link: ", log_link)
        except NoSuchElementException:
            print("Log link not found for ", url)
            continue
        
        url = log_link
        browser.get(url)
        big_table = browser.find_element(By.ID, 'tracklogTable')
        headers = ["Time (EST)", "Latitude", "Longitude", "Course", "kts", "mph", "feet"]
        table_body = big_table.find_element(By.TAG_NAME, 'tbody')
        
        
        output_path = "./scraped_data/"
        
        title_string = os.path.join(output_path, node[1] + "_" + node[2] + ".csv")
        
        
        
        with open(title_string, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(headers)
        
            for row in table_body.find_elements(By.TAG_NAME, 'tr'):
                cells = [re.sub(r'[^\x00-\x7F]+', '', cell.text.encode('utf-8', 'ignore').decode('utf-8')) for cell in row.find_elements(By.TAG_NAME, 'td')[:7]]
                
                writer.writerow(cells)
        #logLinks.append([log_link, node[1], node[2]])
        #linkNotAcquired = False
        
            
        

            
    

browser.quit()



















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
            