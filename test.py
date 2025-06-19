
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load model once when this script is imported
MODEL_PATH = 'model/IncepV3-8-Class.h5'  # or the saved model path
model = tf.keras.models.load_model(MODEL_PATH)

# with open('model/OpenAPI.txt','r') as keyFile:
#     key = keyFile.read()

# API_KEY : str = key.strip()

# Optional: class names if you have them
CLASS_NAMES = ['BA- cellulitis', 'BA-impetigo', 'FU-athlete-foot', 'FU-nail-fungus', 'FU-ringworm', 'PA-cutaneous-larva-migrans', 'VI-chickenpox', 'VI-shingles']
def model_predict(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Batch size of 1

    preds = model.predict(img_array)
    pred_idx = np.argmax(preds, axis=1)[0]
    confidence = np.max(preds)

    predicted_class = CLASS_NAMES[pred_idx] if CLASS_NAMES else str(pred_idx)
    return f"{predicted_class} ({confidence:.2%} confidence)",confidence

def customModelPredict(img_path:str='',target_size:tuple=(224,224),model:object=None):
    """
    Predicts the class of an input image using a trained classification model.

    Args:
        img_path (str): Path to the image file to be predicted.
        target_size (tuple): Desired size to resize the image to before prediction (default is (224, 224)).
        model (object): A trained Keras/TensorFlow model used to make the prediction.

    Returns:
        tuple:
            - str: Human-readable prediction string in the format "ClassName (XX.XX% confidence)" or error message.
            - float: Prediction confidence score (between 0.0 and 1.0). Returns 0 on error.

    Raises:
        None: All exceptions are caught and returned as part of the result.
    """

    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Batch size of 1

        preds = model.predict(img_array)
        pred_idx = np.argmax(preds, axis=1)[0]
        confidence = np.max(preds)

        predicted_class = CLASS_NAMES[pred_idx] if CLASS_NAMES else str(pred_idx)
        return f"{predicted_class} ({confidence:.2%} confidence)",confidence
    except Exception as e:
        return f'Error : {e}',0

    

