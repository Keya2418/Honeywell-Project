#inputs: actual flight departure, estimated flight departure, estimated flight arrival 
#output: actual time of arrival

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn import linear_model

df = pandas.read_csv("")

X = df[['Takeoff Actual', 'Takeoff Estimated', 'Gate Arrival Estimated']]
y = df['Gate Arrival Actual']

regr = linear_model.LinearRegression()
regr.fit(X, y)

predictedCO2 = regr.predict([[]])

print(predictedCO2) 