from flask import Flask, render_template, request, jsonify
import json
import csv 
import pandas as pd
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from datetime import datetime
from datetime import time

app = Flask(__name__, static_url_path='/static')

@app.route('/')

def index():
    #latLongData = []
    #altitudeData = []

    flight_data = []

    try:
        with open('Thu0945PMMST_A20N.csv') as csvfile:
            reader = csv.reader(csvfile)  

            next(reader)  
            #next(reader)

            latitudes = []
            longitudes = []
            altitudes = []

            for row in reader:
                latitude = float(row[1])  
                longitude = float(row[2]) 
                height = float(row[6]) 
                
                latitudes.append(latitude)
                longitudes.append(longitude)
                altitudes.append(height)
                
                if math.isnan(longitude) or math.isnan(latitude) or math.isnan(height):
                    break

                
                flight_data.append({"longitude": longitude, "latitude": latitude, "height": height})
            
            
    except Exception as e:
        print(f"An error has occurred: {e}")

    return render_template('phx-las.html', flight_data=json.dumps(flight_data))

# I put this outside of the /submit area because I don't want to have to load the model a bajillion times 

# Define neural network architecture
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(3, 64)  # Input layer
        self.fc2 = nn.Linear(64, 32)                  # Hidden layer
        self.fc3 = nn.Linear(32, 1)                   # Output layer

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))  # Apply ReLU activation function to second layer
        x = self.fc3(x)              # Output layer (no activation function)
        return x

    def predict_actual_time_of_arrival(self, sample_input_data):
        features = ['Takeoff Actual', 'Average Delay Takeoff Numeric', 'Day Numeric']
        new_data = []
        for feature in features:
            if feature in sample_input_data:
                if feature == 'Landing Actual' and sample_input_data[feature] is None:
                    new_data.append(0)  # You can replace this with any default value
                else:
                    new_data.append(sample_input_data[feature])

        new_data_tensor = torch.tensor([new_data], dtype=torch.float32)

        predicted_arrival_time_tensor = self(new_data_tensor)
        
        predicted_arrival_time = predicted_arrival_time_tensor.item()

        return predicted_arrival_time

# Load the model
loaded_model = NeuralNetwork()
loaded_model.load_state_dict(torch.load('model.pth'))

# Handle the AJAX request
@app.route('/submit', methods=['POST'])
def submit():
    user_input_time = request.json['userInputTime']
    user_input_date = request.json['userInputDate']

    print("userInputTime: ", user_input_time)
    print("userInputDate: ", user_input_date)

    predicted_arrival_time = "it didn't work"
    try:
        print("inside try block")

        hours, minutes = map(int, user_input_time.split(":"))
        takeoff_actual = hours * 60 + minutes
        date = datetime.strptime(user_input_date, '%Y-%m-%d')
        day_of_week = date.weekday()


        sample_input_data = {
            'Takeoff Actual': takeoff_actual,
            'Average Delay Takeoff Numeric': 2,
            'Day Numeric': day_of_week
        }
        predicted_arrival_time = loaded_model.predict_actual_time_of_arrival(sample_input_data)
        intermediary_minutes = takeoff_actual + predicted_arrival_time
        hours = int(intermediary_minutes // 60)
        minutes = int(intermediary_minutes % 60)
        predicted_arrival_time = '{:02d}:{:02d}'.format(hours, minutes)
        
        print(f"Predicted Actual Time of Arrival: {predicted_arrival_time}")
        #print("predicted_arrival_time", predicted_arrival_time)

    except Exception as e:
        print(f"An error has occurred: {e}")

    print("predicted_arrival_time: ", predicted_arrival_time)
    return jsonify({'predicted_arrival_time': predicted_arrival_time})




@app.route('/templates/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
