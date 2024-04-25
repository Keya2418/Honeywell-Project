import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = "output.csv"
df = pd.read_csv(file_path)

# Drop rows with NaN values
df = df.dropna()

# Extract day from Date column and create a new column 'Day'
df['Day'] = pd.to_datetime(df['Date']).dt.day_name()

import re
# Define a function to extract the numeric part from the string
def extract_numeric(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    else:
        return None

# Apply the function to clean the "Taxi Landing" column
df['Taxi Landing'] = df['Taxi Landing'].apply(extract_numeric)
df['Taxi Takeoff'] = df['Taxi Takeoff'].apply(extract_numeric)

# Define the time-related columns
time_columns = ['Gate Departure Actual', 'Gate Departure Estimated', 'Takeoff Actual', 'Takeoff Estimated', 'Gate Arrival Actual', 'Gate Arrival Estimated', 'Landing Actual', 'Landing Estimated']

# Replace non-time values ('--') with NaN
df[time_columns] = df[time_columns].replace('--', pd.NA)

# Convert time columns to 24-hour format
for column in time_columns:
    # Convert to datetime objects
    df[column] = pd.to_datetime(df[column], errors='coerce')
    # Convert to 24-hour format
    df[column] = df[column].dt.strftime('%H:%M')

# Display the DataFrame after conversion
# print(df[time_columns])
print(df.head())


# Convert time columns to numerical format (hours and minutes)
for column in ['Takeoff Actual', 'Takeoff Estimated', 'Landing Actual', 'Landing Estimated']:
    df[column] = pd.to_datetime(df[column]).dt.hour * 60 + pd.to_datetime(df[column]).dt.minute

def map_day_to_numeric(day):
    if day == 'Monday':
        return 1
    elif day == 'Tuesday':
        return 2
    elif day == 'Wednesday':
        return 3
    elif day == 'Thursday':
        return 4
    elif day == 'Friday':
        return 5
    elif day == 'Saturday':
        return 6
    elif day == 'Sunday':
        return 7
    else:
        return -1  # Handle unknown cases if any

# Assuming 'Day' column contains the days of the week
df['Day Numeric'] = df['Day'].apply(map_day_to_numeric)

# Define a function to map categories to numerical values
def map_delay_to_numeric(text):
    if 'Less than 10 minutes' in text:
        return 0
    elif '10-20 minutes' in text:
        return 1
    elif '20-40 minutes' in text:
        return 2
    elif '40 minutes - 1 hour' in text:
        return 3
    elif 'More than 1 hour' in text:
        return 4
    else:
        return -1  # Handle unknown cases if any

# Convert all values in 'Average Delay Takeoff' column to strings
df['Average Delay Takeoff'] = df['Average Delay Takeoff'].astype(str)

# Apply the mapping function to convert categories to numerical values
df['Average Delay Takeoff Numeric'] = df['Average Delay Takeoff'].apply(map_delay_to_numeric)

# Define features and target
features = ['Takeoff Actual', 'Average Delay Takeoff Numeric', 'Day Numeric']
target = 'Landing Actual'

# Extract features and target
X = df[features]
y = df[target]

# Convert data to PyTorch tensors
X_tensor = torch.tensor(X.values, dtype=torch.float32)
y_tensor = torch.tensor(y.values.reshape(-1, 1), dtype=torch.float32)

# Split the data into training and testing sets
X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = train_test_split(X_tensor, y_tensor, test_size=0.2, random_state=42)

# Check the first few rows of the modified DataFrame
print(df[['Average Delay Takeoff', 'Average Delay Takeoff Numeric']].head())

import torch.nn.functional as F

# Define the correct number of input features
num_input_features = X_train_tensor.shape[1]

# Define neural network architecture
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(num_input_features, 64)  # Input layer
        self.fc2 = nn.Linear(64, 32)                  # Hidden layer
        self.fc3 = nn.Linear(32, 1)                   # Output layer

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))  # Apply ReLU activation function to second layer
        x = self.fc3(x)              # Output layer (no activation function)
        return x

# Instantiate the model
model = NeuralNetwork()
# Make predictions on the training data
model.eval()
with torch.no_grad():
    y_pred_train_tensor = model(X_train_tensor)
    
# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 100000
train_losses = []
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    train_losses.append(loss.item())
    
    # Print loss every 100 epochs
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


# Evaluate the model
model.eval()
with torch.no_grad():
    y_pred_tensor = model(X_test_tensor)
    mse = criterion(y_pred_tensor, y_test_tensor)
    print(f'Mean Squared Error on Test Data: {mse.item():.4f}')
    
import matplotlib.pyplot as plt
import seaborn as sns

# Calculate the absolute difference between actual and estimated time of arrival
arrival_time_difference = torch.abs(y_test_tensor - y_pred_tensor).numpy()

# Analyze the difference
mean_difference = arrival_time_difference.mean()
max_difference = arrival_time_difference.max()
min_difference = arrival_time_difference.min()

#print("Mean difference:", mean_difference)
#print("Maximum difference:", max_difference)
#print("Minimum difference:", min_difference)

from sklearn.metrics import mean_squared_error, mean_absolute_error

# Convert predicted values to numpy arrays
y_pred_train = model(X_train_tensor).detach().numpy().reshape(-1)
y_pred_test = model(X_test_tensor).detach().numpy().reshape(-1)

# Calculate Mean Squared Error (MSE) and Mean Absolute Error (MAE) for training and test data
mse_train = mean_squared_error(y_train_tensor, torch.tensor(y_pred_train, dtype=torch.float32))
mae_train = mean_absolute_error(y_train_tensor, torch.tensor(y_pred_train, dtype=torch.float32))
mse_test = mean_squared_error(y_test_tensor, torch.tensor(y_pred_test, dtype=torch.float32))
mae_test = mean_absolute_error(y_test_tensor, torch.tensor(y_pred_test, dtype=torch.float32))

#print("Mean Squared Error (MSE) - Train:", mse_train)
#print("Mean Absolute Error (MAE) - Train:", mae_train)
#print("Mean Squared Error (MSE) - Test:", mse_test)
#print("Mean Absolute Error (MAE) - Test:", mae_test)

from sklearn.metrics import r2_score, mean_absolute_percentage_error, mean_squared_log_error, explained_variance_score

# R² Score (coefficient of determination) = 1 - (SS_res / SS_tot)
# Measures the proportion of the variance in the dependent variable that is predictable from the independent variables.
r2_train = r2_score(y_train_tensor, y_pred_train_tensor)
r2_test = r2_score(y_test_tensor, y_pred_tensor)

# MAPE = (1/n) * Σ(|actual - predicted| / |actual|) * 100%
# Calculates the mean of the absolute percentage errors between the predicted and actual values 
mape_train = mean_absolute_percentage_error(y_train_tensor, y_pred_train_tensor)
mape_test = mean_absolute_percentage_error(y_test_tensor, y_pred_tensor)

# Clip negative values to zero
y_train_tensor_clipped = np.clip(y_train_tensor, 0, None)
y_pred_train_tensor_clipped = np.clip(y_pred_train_tensor, 0, None)
y_test_tensor_clipped = np.clip(y_test_tensor, 0, None)
y_pred_tensor_clipped = np.clip(y_pred_tensor, 0, None)

# Calculate RMSLE with clipped targets
rmsle_train = np.sqrt(mean_squared_log_error(y_train_tensor_clipped, y_pred_train_tensor_clipped))
rmsle_test = np.sqrt(mean_squared_log_error(y_test_tensor_clipped, y_pred_tensor_clipped))

# Calculate Explained Variance Score = 1 - (Var(y_true - y_pred) / Var(y_true))
# Explained Variance Score measures the proportion to which a mathematical model accounts for the variation (dispersion) of a given data set.
explained_variance_train = explained_variance_score(y_train_tensor, y_pred_train_tensor)
explained_variance_test = explained_variance_score(y_test_tensor, y_pred_tensor)

#print("R² Score (Train):", r2_train)
#print("R² Score (Test):", r2_test)
#print("MAPE (Train):", mape_train)
#print("MAPE (Test):", mape_test)
#print("RMSLE (Train):", rmsle_train)
#print("RMSLE (Test):", rmsle_test)
#print("Explained Variance Score (Train):", explained_variance_train)
#print("Explained Variance Score (Test):", explained_variance_test)

from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

# Initialize Ridge and Lasso regression models
ridge_model = Ridge(alpha=1.0)  # You can adjust the alpha parameter for regularization strength

# Train Ridge and Lasso models
ridge_model.fit(X_train_tensor, y_train_tensor)

# Predictions
y_pred_ridge_train = ridge_model.predict(X_train_tensor)
y_pred_ridge_test = ridge_model.predict(X_test_tensor)


# Evaluate the models
mse_ridge_train = mean_squared_error(y_train_tensor, y_pred_ridge_train)
mse_ridge_test = mean_squared_error(y_test_tensor, y_pred_ridge_test)

###############################

import datetime
# Sample input data for testing
sample_input_data = {
    'Takeoff Actual': 14 * 60 + 13,  # Takeoff time  (8:30 AM)
    'Average Delay Takeoff Numeric': 2,  # Numeric representation of average delay
    'Day Numeric': 3  # Numeric representation of day (1 for Monday)
}

# Function to predict actual time of arrival using sample input data
def predict_actual_time_of_arrival(model, sample_input_data):
    new_data = []
    for feature in features:
        if feature in sample_input_data:
            if feature == 'Landing Actual' and sample_input_data[feature] is None:
                new_data.append(0)  # You can replace this with any default value
            else:
                new_data.append(sample_input_data[feature])

    # Convert new flight data to tensor
    new_data_tensor = torch.tensor([new_data], dtype=torch.float32)

    # Make prediction
    predicted_arrival_time_tensor = model(new_data_tensor)
    
    # Convert tensor to float
    predicted_arrival_time = predicted_arrival_time_tensor.item()

    # Print the predicted arrival time
    #print(f"Predicted Actual Time of Arrival: {predicted_arrival_time:.2f} minutes")

    return predicted_arrival_time

# Use the function to predict actual time of arrival for a new flight with sample input data
predicted_arrival_time = predict_actual_time_of_arrival(model, sample_input_data)

# Function to convert minutes to time of day
def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return datetime.time(hour=int(hours), minute=int(minutes))

# Convert the predicted arrival time from minutes to time of day
predicted_arrival_time_hours = minutes_to_time(predicted_arrival_time)

# Print the predicted arrival time
print(f"Predicted Actual Time of Arrival: {predicted_arrival_time_hours}")

try:
    # Save the entire model
    torch.save(model.state_dict(), 'model.pth')
    print("Model state dictionary saved successfully.")
except Exception as e:
    print("An error occurred while saving the model:", e)

import os

file_path = 'model.pth'
if os.path.exists(file_path):
    print(f"'{file_path}' exists in the directory.")
else:
    print(f"'{file_path}' does not exist in the directory.")