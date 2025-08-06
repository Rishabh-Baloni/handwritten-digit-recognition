import os
import logging
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from .utils import preprocess_image
import gc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure TensorFlow for better performance
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(2)
tf.config.set_soft_device_placement(True)

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
            
            # Define custom InputLayer to handle batch_shape parameter
            class CustomInputLayer(tf.keras.layers.InputLayer):
                def __init__(self, batch_shape=None, **kwargs):
                    if batch_shape is not None:
                        kwargs['input_shape'] = batch_shape[1:]
                    super().__init__(**kwargs)
            
            # Try loading with custom objects
            custom_objects = {'InputLayer': CustomInputLayer}
            
            # Time the model loading
            start_time = time.time()
            # Load the model with custom objects and compile=False to avoid jit_compile issues
            self.model = keras.models.load_model(self.model_path, custom_objects=custom_objects, compile=False)
            load_time = time.time() - start_time
            logger.info(f"Model loaded successfully in {load_time:.2f} seconds")
            
            # Log model summary
            self.model.summary(print_fn=logger.info)
            
            # Perform multiple warm-up predictions to ensure TF optimization is complete
            logger.info("Performing warm-up predictions to initialize TensorFlow optimizations...")
            test_input = np.zeros((1, 28, 28, 1))
            
            # First warm-up with eager execution
            start_time = time.time()
            logger.info("First warm-up prediction (eager execution)...")
            test_prediction = self.model.predict(test_input, verbose=0)
            first_pred_time = time.time() - start_time
            logger.info(f"First warm-up prediction completed in {first_pred_time:.2f} seconds")
            
            # Second warm-up to ensure graph compilation
            start_time = time.time()
            logger.info("Second warm-up prediction (possible graph compilation)...")
            test_prediction = self.model.predict(test_input, verbose=0)
            second_pred_time = time.time() - start_time
            logger.info(f"Second warm-up prediction completed in {second_pred_time:.2f} seconds")
            
            # Third warm-up for good measure
            start_time = time.time()
            logger.info("Third warm-up prediction (final optimization)...")
            test_prediction = self.model.predict(test_input, verbose=0)
            third_pred_time = time.time() - start_time
            logger.info(f"Third warm-up prediction completed in {third_pred_time:.2f} seconds")
            
            # Run garbage collection to clean up memory
            gc.collect()
            
            logger.info(f"Successfully loaded and verified Keras model from {self.model_path}")
            logger.info(f"Model verification successful with output shape: {test_prediction.shape}")
            logger.info("Model initialization complete and ready for predictions")
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
            start_preprocess = time.time()
            processed_image = preprocess_image(image_data)
            preprocess_time = time.time() - start_preprocess
            
            if processed_image is None:
                return {"error": "Failed to process image"}
            
            logger.info(f"Received prediction request with shape: {processed_image.shape} (preprocessing took {preprocess_time:.4f}s)")
            
            # Make prediction using the Keras model with optimized settings
            # Set verbose=0 to reduce logging overhead
            start_time = time.time()
            logger.info("Starting model prediction...")
            
            # Make prediction with optimized settings
            logits = self.model.predict(processed_image, verbose=0)[0]
            
            prediction_time = time.time() - start_time
            logger.info(f"Prediction completed in {prediction_time:.2f} seconds")
            logger.info(f"Raw logits: {logits}")
            
            # Convert logits to probabilities
            probabilities = tf.nn.softmax(logits).numpy()
            logger.info(f"Probabilities: {probabilities}")
            
            # Get the predicted digit and confidence
            predicted_digit = np.argmax(probabilities)
            confidence = float(probabilities[predicted_digit]) * 100
            
            # Run garbage collection after prediction
            gc.collect()
            
            return {
                "digit": int(predicted_digit),
                "confidence": confidence,
                "probabilities": [float(p) * 100 for p in probabilities],
                "prediction_time_ms": int(prediction_time * 1000),
                "preprocessing_time_ms": int(preprocess_time * 1000)
            }
        except Exception as e:
            logger.error(f"Error predicting digit: {str(e)}")
            return {"error": str(e)}