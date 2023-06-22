# Dog Nose Print Identification

This repository contains the code for identifying dogs based on their unique nose prints. The goal is to develop a biometric identification system using dog nose prints. Research has shown that each dog has distinct features in their nose prints, making it an ideal biometric identifier.

## Problem Statement

The problem is to identify each dog using their nose print. The repository provides a solution using an API created with FastAPI. The API takes a dog nose image as input and processes it using a pre-trained VGG16 model to extract unique features from the nose print. The output feature array is then cross-checked with a dataset. If a similar array is found in the dataset, the registration does not take place. However, if no similar array is found, the nose print is added to the dataset. This is achieved through a separate FastAPI endpoint named "reg". In case a dog is lost and someone sends a scanned nose image, it will be matched with the features stored in the dataset. If a match is found, important information is returned via the API.

## Usage

To create the initial dataset, you can use the `create_database.py` script provided in the repository.

### Local Setup

To run the project on your local system, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
2. Install the required packages or dependencies:
   pip install -r requirements.txt
3.python main.py
4.Access the API at http://localhost:8000

## Docker Setup
To run the project using Docker, follow these steps:

Build the Docker image:

bash
Copy code
docker build -t dog_nose_print .
Run the Docker container:

bash
Copy code
docker run dog_nose_print
That's it! The project should now be running.

## Dataset
The dataset used in this project is available on Kaggle with the name "PRT Biometric". To create your own dataset, you can use the create_dataset.py script. Make sure to replace the input link in the script with the link to your stored dataset directory.

## Contributions
Contributions to this project are welcome. If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

## License
MIT License
