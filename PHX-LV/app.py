from flask import Flask, render_template
import csv
import json
import pandas as pd
import math

app = Flask(__name__)

@app.route('/')

def index():
    #latLongData = []
    #altitudeData = []

    flight_data = []

    try:
        excel_reader = pd.read_excel('Simbrief_Comparisons/PHX_LAS_022724_1942.xlsx')

        for index, row in excel_reader.iterrows():
            #skip the first two rows because they have stuff in them (the title and the departure time)
            if index < 2:
                continue
            
            longitude = float(row['Longitude'])
            latitude = float(row['Latitude'])
            height = float(row['feet'])

            #this if statement checks to see if we made it to the very last row or not (or if any of the datapoints are faulty in some way)
            if math.isnan(longitude) or math.isnan(latitude) or math.isnan(height):
                continue

            flight_data.append({"longitude": longitude, "latitude": latitude, "height": height})

            #print(f"Latitude: {latitude}, Longitude: {longitude}, Height: {height}")
                
    except Exception as e:
        print(f"An error has occurred: {e}")

    #print(f"Flight data: {flight_data}")

    return render_template('phx-las.html', flight_data=json.dumps(flight_data))

if __name__ == '__main__':
    app.run(debug=True)
