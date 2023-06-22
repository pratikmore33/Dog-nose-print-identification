from fastapi import FastAPI,UploadFile,File
import uvicorn
import shutil
import tempfile
from scipy.spatial.distance import cosine
import sqlite3
import numpy as np
from feature_extract import extract_features

app = FastAPI()

@app.get('/')
async def welcome():
    return 'welcome to nexsol'

@app.post("/reg")
async def upload_file(file: UploadFile = File(...)):
    print(file)
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # Save the uploaded file
    file_path = f"{temp_dir}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # Connect to the SQLite database
    conn = sqlite3.connect('Database/example.db')
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


    print(len(list(retrieved_dataset.values())))

    target_array = extract_features(file_path)
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

        # Close the database connection
        conn.close()

        return "Your dog information has save sucessfully."
    else:
        return "The dog you want to registred is already present in our dataset."


    
@app.post('/scanning')
async def find_my_dog(file: UploadFile = File(...)):
    # Create a temporary directory
    temp_dir2 = tempfile.mkdtemp()
    # Save the uploaded file
    file_path_for_scanning = f"{temp_dir2}/{file.filename}"
    with open(file_path_for_scanning, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # Connect to the SQLite database
    conn = sqlite3.connect('Database/example.db')
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

    # Extract features from the new image
    new_image_features = extract_features(file_path_for_scanning)

    # Compare the new image features with the dataset using cosine similarity
    max_similarity = -1
    max_similarity_image_id = None
 
    for image_id, features in retrieved_dataset.items():
        similarity = 1 - cosine(features, new_image_features)
        if similarity > max_similarity:
            max_similarity = similarity
            max_similarity_image_id = image_id

    return {'Most similar image ID': max_similarity_image_id,'similarity_score':max_similarity}




if __name__ == '__main__':
    uvicorn.run(app)



