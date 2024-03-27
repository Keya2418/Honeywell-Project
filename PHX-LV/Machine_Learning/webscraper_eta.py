#WEBSCRAPER ETA 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import os

# the singular function:

def remove_spaces_and_colons(input_string):
    cleaned_string = input_string.replace(' ', '').replace(':', '')
    return cleaned_string

webdriver_path = './geckodriver'

browser = webdriver.Firefox()

url = 'https://www.flightaware.com/live/findflight?origin=KPHX&destination=KLAS'

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
    flight_number_text = ident_span.text
    anchor_tag = ident_span.find_element(By.TAG_NAME, 'a')
    link = anchor_tag.get_attribute('href')
    #these links are gold!! hooray
    #print("link: ", link)
    if "Arrive" in status: 
        #print("arrive is in status")
        if (departure != "" and aircraft != ""):
            allLTA.append([link, departure, aircraft, flight_number_text])

            
if allLTA:
    print("\n\n")
    for node in allLTA:
        print("link: ", node[0])
        print("time: ", node[1])
        print("aircraft: ", node[2])
        print("flight number:", node[3])
        print("\n")
        
#logLinks = []
        
output_path = "./scraped_eta_KPHX_KLAS/"
#title_string = os.path.join(output_path, node[1] + "_" + node[2] + "_ETA" + ".csv")

headers = ["Flight Number", "Date", "Taxi Takeoff", "Average Delay Takeoff", "Gate Departure Actual", "Gate Departure Estimated", "Takeoff Actual", "Takeoff Estimated", "Taxi Landing", "Average Delay Landing", "Landing Actual", "Landing Estimated", "Gate Arrival Actual", "Gate Arrival Estimated"]

with open(os.path.join(output_path, "output.csv"), 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write headers only if file is empty
    if os.path.getsize(os.path.join(output_path, "output.csv")) == 0:
        writer.writerow(headers)
        
    
    if allLTA:
        for node in allLTA:
            #linkNotAcquired = True;
            url = node[0]
            browser.get(url)

            list_of_stuff = []
            
            list_of_stuff.append(node[3])

            retry_attempts = 3
            for attempt in range(retry_attempts):
                try: 
                    date = browser.find_element(By.CSS_SELECTOR, 'span.flightPageSummaryDepartureDay')
                    dateText = date.text
                    list_of_stuff.append(dateText) 
                    largeContainer = browser.find_element(By.CLASS_NAME, 'flightPageDetails')
                    smallerContainer = largeContainer.find_element(By.CSS_SELECTOR, 'div[data-template="live/flight/detailMain"]')
                    timesTable = smallerContainer.find_element(By.CLASS_NAME, 'flightPageDataTableContainer')
                    littleSections = timesTable.find_elements(By.CLASS_NAME, 'flightPageDataTable')

                    # Print the number of sections found
                    #print("Number of sections found:", len(littleSections))

                    for section in littleSections:
                        sectionInLittleSections = section.find_elements(By.CSS_SELECTOR, 'div.flightPageDataTimesChild')
                        ancillaryTextSection = timesTable.find_element(By.CLASS_NAME, 'flightPageDataAncillaryTextContainer')
                        taxi_and_delay = ancillaryTextSection.find_elements(By.CLASS_NAME, 'flightPageDataAncillaryText')
                        #print("number of sections in taxi_and_delay: ", len(taxi_and_delay))

                        for anotherSection in taxi_and_delay:
                            info = anotherSection.find_element(By.CSS_SELECTOR, 'div')
                            infoText = info.text
                            list_of_stuff.append(infoText)

                        for smallerSection in sectionInLittleSections:
                            #print("inside smallerSection in sectionInLittleSections loop")
                            flightPageDataActualTime = smallerSection.find_element(By.CSS_SELECTOR, 'div.flightPageDataActualTimeText')
                            text_Actual = flightPageDataActualTime.text
                            #print("Actual Time Text:", text_Actual)
                            flightPageDataAncillary = smallerSection.find_element(By.CSS_SELECTOR, 'div.flightPageDataAncillaryText')
                            text_Estimated = flightPageDataAncillary.text
                            list_of_stuff.append(text_Actual)
                            list_of_stuff.append(text_Estimated)
                    break
                except NoSuchElementException:
                    print("Elements not found for ", url)
                    continue
                except StaleElementReferenceException:
                    if attempt < (retry_attempts - 1):
                            print("Stale element exception occurred. Retrying...")
                    else:
                        print("Maximum retry attempts reached. Exiting.")
                        break    

            writer.writerow(list_of_stuff)

            print("printing everything in list of stuff:")
            for stuff in list_of_stuff:
                print(stuff)


            

browser.quit()



















