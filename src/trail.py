import sqlite3
import numpy as np
from feature_extract import extract_features
# Connect to the SQLite database
conn = sqlite3.connect('example.db')

# Create a cursor to execute SQL queries
cursor = conn.cursor()

# Execute the SQL query to retrieve the image IDs and feature arrays
cursor.execute("SELECT key, value FROM users")

# Fetch all the rows returned by the query
rows = cursor.fetchall()

# Create an empty dictionary to store the retrieved data
retrieved_dataset = {}

# Iterate over the rows and populate the retrieved_dataset dictionary
for row in rows:
    image_id = row[0]
    feature_array_buffer = row[1]
    feature_array = np.frombuffer(feature_array_buffer, dtype=np.float32)
    retrieved_dataset[image_id] = feature_array


print(len(list(retrieved_dataset.values())[0]))

target_array = extract_features('Images\dog5.jpg')
array_present = False

for feature_array in retrieved_dataset.values():
    if np.array_equal(feature_array, target_array):
        array_present = True
        break

# If the array is not present, add it to the dataset
if not array_present:
    # Generate a unique image ID for the new entry
    new_image_id = max(retrieved_dataset.keys(), default=0) + 1

    # Convert the target_array to a binary representation
    target_array_blob = sqlite3.Binary(target_array.tobytes())

    # Insert the new entry into the database
    cursor.execute("INSERT INTO users (key, value) VALUES (?, ?)",
                   (new_image_id, target_array_blob))

    # Commit the changes to the database
    conn.commit()

    # Update the retrieved_dataset dictionary with the new entry
    retrieved_dataset[new_image_id] = target_array

    print("The array has been added to the dataset.")
else:
    print("The array with the exact value is already present in the dataset.")

# Close the database connection
conn.close()





