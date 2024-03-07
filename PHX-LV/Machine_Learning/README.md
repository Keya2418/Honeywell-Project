Date: 3/7/2024
# Data Gathering

## Past Work: Global Airport Database

I got the lat, long, etc. data about every airport in the world from [The Global Airport Database](https://www.partow.net/miscellaneous/airportdatabase/), a free database for airport information. I then converted that data from a TXT file to a CSV and then filtered it so it only included all the airports in the USA. These airport coordinates will be used for later on as airport starting+ending points because the Flightaware data does not include the starting and ending coordinates of the flight. This will also come in handy when modeling the flights in Cesium.JS. 

## Current Work: Web Scraping

After getting the airport coordinates squared away, I started building a webscraper that could scrape the Flightaware website for all the latitude, longitude, and height coordinates of each flight. So far it does not work quite correctly as of 3/7/24 but it will be adjusted so that mass amounts of data can be collected soon. I am hoping to be able to store all these in CSV files. 

## Future Work: Model Training

After gathering a bunch of data, we plan to write a script for a 3-layer feed-forward neural network model. We will then train the model on the data and see how the results look. In the absence of detailed fuel usage data, we plan to consider the aircraft type instead. We will train the model on all types of aircraft first and also train it on a few specific common aircraft types to measure whether the aircraft type makes a difference on ETA. 

## Future Work: Incorporating METAR data

We will complete the initial model without considering for weather first to test whether our process is correct and then collect METAR data for the specific dates and times of the flights. 
