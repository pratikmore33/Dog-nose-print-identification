

from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from scipy.spatial.distance import cosine
import numpy as np

# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet', include_top=False)


# Function to extract feature vector from an image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_preprocessed = preprocess_input(np.expand_dims(img_array, axis=0))
    features = model.predict(img_preprocessed)
    feature_vector = features.flatten()
    return feature_vector


