Date: 3/8/2024
# LINKS TO DATA: 
# [Scraped_LAT_LONG_ALT_Data](https://drive.google.com/drive/folders/1s7jP6ba0UHtX865Id0fC97EOh2bNMHgx?usp=sharing)
# [Scraped_WAYPOINTS](https://drive.google.com/drive/folders/1c-i0-p0QLCpPKcamd_9Phn2Dy6Tub3qG?usp=sharing)

Note: If you are not signed in to an ASU email you will not be able to view the folder.

# Data Gathering

## Past Work: Global Airport Database

I got the lat, long, etc. data about every airport in the world from [The Global Airport Database](https://www.partow.net/miscellaneous/airportdatabase/), a free database for airport information. I then converted that data from a TXT file to a CSV and then filtered it so it only included all the airports in the USA. These airport coordinates will be used for later on as airport starting+ending points because the Flightaware data does not include the starting and ending coordinates of the flight. This will also come in handy when modeling the flights in Cesium.JS. 

## Past Work: Web Scraping

After getting the airport coordinates squared away, I started building a webscraper that could scrape the Flightaware website for all the latitude, longitude, and height coordinates of each flight. The webscraper should be run every day in the morning and the evening to achieve the maximum amount of data as flights arrive at their gates. It stores all of the scraped data in CSVs. I also scraped the waypoints data so that we can gather weather data based on the longitude and latitude coordinates and also consider which waypoints were chosen in the route. 

## Current Work: Possible Addition of Noise

We are currently researching a way to add noise to the data so that more data can be generated (our main issue is a lack of a large amount of data). We are able to get about 40 flights per day using the webscraper which is not anywhere near the amount of data we need to accomplish this project. 

## Current Work: Model Creation and Training

After gathering a bunch of data, we plan to write a script for a 3-layer feed-forward neural network model. We will then train the model on the data and see how the results look. In the absence of detailed fuel usage data, we plan to consider the aircraft type instead. We will train the model on all types of aircraft first and also train it on a few specific common aircraft types to measure whether the aircraft type makes a difference on ETA. 

## Future Work: Incorporating Weather Data
We will complete the initial model without considering weather first to test whether our process is correct and then collect METAR data for the specific dates and times of the flights. I found this great API that lets you plug in lat/long coordinates and get the weather data for those coordinates: [Visual Crossing](https://www.visualcrossing.com/weather-history/40.7128,-74.0060/us/2024-03-08/2024-03-08). This will be great to use in conjunction with the waypoint and lat/long information. 

## Feedforward Neural Network: Background
A feedforward neural network processes data in a one-way direction, from input nodes through hidden layers to output nodes. It consists of interconnected layers of artificial neurons, learning complex patterns and making predictions. The network comprises an input layer for data input, hidden layers for computations and feature extraction, and an output layer for final results. Each connection between neurons has a weight and bias, determining connection strength and complexity captures. During processing, data moves through layers, with neurons calculating weighted sums, applying activation functions, and passing results onwards. Backpropagation adjusts weights and biases via an optimization algorithm to minimize prediction errors, enabling accurate predictions and generalization. Feedforward networks serve as fundamental models in deep learning alognside more complex architectures like convolutional and recurrent neural networks.

