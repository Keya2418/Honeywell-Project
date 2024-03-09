# WEBSCRAPER FOR WAYPOINTS

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
            surrounding_div = browser.find_element(By.CSS_SELECTOR, 'div[data-template="live/flight/data"]')
            div_with_link = surrounding_div.find_element(By.CSS_SELECTOR, '.flightPageDataRowTall')
            anchor_tag = div_with_link.find_element(By.CSS_SELECTOR, '.flightPageLink')
            log_link = anchor_tag.get_attribute('href')
            print("log link: ", log_link)
        except NoSuchElementException:
            print("Log link not found for ", url)
            continue
        
        url = log_link
        browser.get(url)
        headers = ["Name", "Latitude", "Longitude", "Outbound Course", "Distance this Leg", "Distance Remaining", "Distance Flown", "Type"]
        big_table_body = browser.find_element(By.TAG_NAME, 'tbody')
        table_body = big_table_body.find_element(By.TAG_NAME, 'tbody')
        
        
        output_path = "./scraped_data_waypoints/"
        
        title_string = os.path.join(output_path, node[1] + "_" + node[2] + "_WAYPOINTS" + ".csv")
        
        
        
        with open(title_string, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(headers)
        
            for row in table_body.find_elements(By.TAG_NAME, 'tr'):
                cells = [re.sub(r'[^\x00-\x7F]+', '', cell.text.encode('utf-8', 'ignore').decode('utf-8')) for cell in row.find_elements(By.TAG_NAME, 'td')]
                
                writer.writerow(cells)
        #logLinks.append([log_link, node[1], node[2]])
        #linkNotAcquired = False
            
                

            
        

            
    

browser.quit()
















            