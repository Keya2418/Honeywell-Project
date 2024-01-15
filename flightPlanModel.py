# Capstone Project
# Honeywell Aerospace: Improving Flight Plan Routes Based on Big Data and AI/ML
# Keya Gholap, Ashley Nichols, Shardul Dhaul, John Baker, Yonatan Rosenbloom
# Sponsor: Sreenivasan "KG" Govindillam
 
# Importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset (replace 'dataset.csv' with actual data)
data = pd.read_csv('dataset.csv')

# Explore and understand the dataset
print(data.head())
print(data.info())

# Preprocess the data
X = data[['param1', 'param2', 'param3', 'param4', 'param5']]  # Replace with actual column names
y = data['target']  # Replace with actual target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a model (using K-Nearest Neighbors as an example)
model = KNeighborsClassifier(n_neighbors=3)  # Choose a different algorithm and adjust parameters
model.fit(X_train_scaled, y_train)

# Make predictions
predictions = model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Additional evaluation metrics and details
print(classification_report(y_test, predictions))