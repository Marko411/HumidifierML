import pandas as pd

dataFrame = pd.read_csv('data3.csv') #data frame from csv file

print(dataFrame.head()) #by default prints first 5 rows of csv, good to see if data's loaded

print(dataFrame.info()) #gives range index, columns, data types of columns, memory usage of the DATA FRAME (not the csv)

print(dataFrame.describe())  #displays some stats analysis of the data set such as count, mean , std dev, 1st,2nd&3rd quartiles

print(dataFrame.isnull().sum()) #counts missing values for each column but data should already be clean

dataFrame.drop(columns=['comfortRating'], inplace=True)

dataFrame.to_csv('data3.csv', index=False) #adding motor control column
print("Updated data frame from the csv file")

