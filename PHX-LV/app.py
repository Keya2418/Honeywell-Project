from flask import Flask, render_template
import csv
import json

app = Flask(__name__)

@app.route('/')

def index():
    #latLongData = []
    #altitudeData = []

    flight_data = []

    try:
        with open('flightData/WN616_Feb_08_PHX_LAS.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                #latLongData.append(row[3]) #3 is column for Position
                #altitudeData.append(row[4]) #4 is column for Altitude 
                latitude, longitude = map(float, row[3].split(','))
                height = float(row[4])
                flight_data.append({"longitude":longitude, "latitude":latitude, "height":height})
                print(f"Latitude: {latitude}, Longitude: {longitude}, Height: {height}")

        #return render_template('phx-las.html', latLongData=latLongData, altitudeData=altitudeData)
                
    except Exception as e:
        print(f"An error has occurred: {e}")

    print(f"Flight data: {flight_data}")

    return render_template('phx-las.html', flight_data=json.dumps(flight_data))

if __name__ == '__main__':
    app.run(debug=True)
