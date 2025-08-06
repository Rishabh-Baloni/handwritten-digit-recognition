import os
import logging
import numpy as np
import tensorflow as tf
from tensorflow import keras
from .utils import preprocess_image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DigitRecognizer:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the Keras model from the specified path."""
        try:
            # Check if model file exists
            if not os.path.exists(self.model_path):
                logger.error(f"Model file not found at path: {self.model_path}")
                logger.info(f"Current working directory: {os.getcwd()}")
                logger.info(f"Directory contents: {os.listdir(os.path.dirname(self.model_path))}")
                return False
                
            # Log model path for debugging
            logger.info(f"Attempting to load model from: {self.model_path}")
            
            # Load the model
            self.model = keras.models.load_model(self.model_path)
            
            # Log model summary
            self.model.summary(print_fn=logger.info)
            
            # Verify the model works with a test prediction
            test_input = np.zeros((1, 28, 28, 1))
            test_prediction = self.model.predict(test_input)
            logger.info(f"Successfully loaded and verified Keras model from {self.model_path}")
            logger.info(f"Model verification successful with output shape: {test_prediction.shape}")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            # Print stack trace for debugging
            import traceback
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return False
    
    def predict_digit(self, image_data):
        """Predict the digit from the image data."""
        try:
            # Preprocess the image
            processed_image = preprocess_image(image_data)
            if processed_image is None:
                return {"error": "Failed to process image"}
            
            logger.info(f"Received prediction request with shape: {processed_image.shape}")
            
            # Make prediction using the Keras model
            logits = self.model.predict(processed_image)[0]
            logger.info(f"Raw logits: {logits}")
            
            # Convert logits to probabilities
            probabilities = tf.nn.softmax(logits).numpy()
            logger.info(f"Probabilities: {probabilities}")
            
            # Get the predicted digit and confidence
            predicted_digit = np.argmax(probabilities)
            confidence = float(probabilities[predicted_digit]) * 100
            
            return {
                "digit": int(predicted_digit),
                "confidence": confidence,
                "probabilities": [float(p) * 100 for p in probabilities]
            }
        except Exception as e:
            logger.error(f"Error predicting digit: {str(e)}")
            return {"error": str(e)}