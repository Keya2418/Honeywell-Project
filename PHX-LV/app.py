from flask import Flask, render_template, g
import csv
import json
import pandas as pd
import math
import joblib
import datetime
import torch.nn as nn

import torch
import numpy as np


# class NeuralNetwork(nn.Module):
#     def __init__(self):
#         """This is just an interface for when we load in the trained model"""
#         pass

#     def forward(self, x):
#         """This is just an interface for when we load in the trained model"""
#         pass

#     def predict(self, take_off_actual, take_off_estimated, landing_estimated, average_delay):
#         """This is just an interface for when we load in the trained model"""
#         pass
    
#     def __str__(self):      # The toString method for the class
#         """This is just an interface for when we load in the trained model"""
#         pass

app = Flask(__name__, static_url_path='/static')

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/etaCalculation')
def calculateEta():

    model = ensureGetModel()
    time = model.predict(8 * 60 + 30, 8 * 60 + 40, 9 * 60 + 50, 1)
    print(time)

    hours = time / 60
    minutes = time % 60

    dt = str(datetime.time(hour=int(hours), minute=int(minutes)))
    print(dt)
    return dt


def ensureGetModel():
    model = getattr(g, '_model', None)
    if model is None:
        g._model = torch.jit.load('trained-model.pt').eval()
    return g._model

if __name__ == '__main__':
    app.run(debug=True)
    # print(model)

