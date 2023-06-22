import os
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from scipy.spatial.distance import cosine
import numpy as np
import csv
import sqlite3
from feature_extract import extract_features

# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet', include_top=False)



# load data 
train_data = r'C:\Users\pratik\Desktop\Data for ML\pet_biometric_challenge_2022\train\images'
train_file = os.listdir(train_data)

# Create an empty dictionary to store feature vectors and unique IDs
dataset = {}


# Iterate over your dataset and extract features, assign unique IDs, and store in the dataset dictionary
i = 1
for image_path in train_file:
    path = train_data+'/'+image_path
    image_id = i  # Replace with your logic to generate a unique ID
    i = i+1
    features = extract_features(path)
    dataset[image_id] = features

# Connect to the SQLite database
conn = sqlite3.connect('Database/example.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (key INTEGER, value BLOB)''')

# Insert the dictionary data into the table
for key, value in dataset.items():
    cursor.execute("INSERT INTO users VALUES (?, ?)",
                   (key, value))

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

# Connect to the SQLite database
conn = sqlite3.connect('Database/example.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute a SELECT query to retrieve the data
cursor.execute("SELECT * FROM users")

# Fetch all rows returned by the query
rows = cursor.fetchall()

# Check if any rows were returned
if len(rows) > 0:
    print("Data is stored in the database.")
else:
    print("No data found in the database.")

# Close the database connection
conn.close()