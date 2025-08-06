#!/usr/bin/env python
"""
Test script to evaluate model loading and prediction performance.
This script helps identify potential bottlenecks before deployment.
"""

import os
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging
import argparse
import gc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure TensorFlow for better performance
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(2)
tf.config.set_soft_device_placement(True)

# Set TensorFlow log level
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0=DEBUG, 1=INFO, 2=WARNING, 3=ERROR

def test_model_performance(model_path, num_warmup=3, num_predictions=10):
    """
    Test model loading and prediction performance.
    
    Args:
        model_path: Path to the Keras model file
        num_warmup: Number of warmup predictions to perform
        num_predictions: Number of predictions to test after warmup
    """
    try:
        # Define custom InputLayer to handle batch_shape parameter
        class CustomInputLayer(tf.keras.layers.InputLayer):
            def __init__(self, batch_shape=None, **kwargs):
                if batch_shape is not None:
                    kwargs['input_shape'] = batch_shape[1:]
                super().__init__(**kwargs)
        
        # Try loading with custom objects
        custom_objects = {'InputLayer': CustomInputLayer}
        
        # Time the model loading
        logger.info(f"Loading model from {model_path}")
        start_time = time.time()
        model = keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
        load_time = time.time() - start_time
        logger.info(f"Model loaded successfully in {load_time:.4f} seconds")
        
        # Print model summary
        model.summary(print_fn=logger.info)
        
        # Create test input
        test_input = np.zeros((1, 28, 28, 1))
        
        # Perform warmup predictions
        logger.info(f"Performing {num_warmup} warmup predictions...")
        warmup_times = []
        
        for i in range(num_warmup):
            start_time = time.time()
            model.predict(test_input, verbose=0)
            pred_time = time.time() - start_time
            warmup_times.append(pred_time)
            logger.info(f"Warmup prediction {i+1}/{num_warmup} completed in {pred_time:.4f} seconds")
            
            # Run garbage collection between predictions
            gc.collect()
        
        # Perform test predictions
        logger.info(f"Performing {num_predictions} test predictions...")
        prediction_times = []
        
        for i in range(num_predictions):
            # Create random test input
            random_input = np.random.rand(1, 28, 28, 1)
            
            start_time = time.time()
            result = model.predict(random_input, verbose=0)
            pred_time = time.time() - start_time
            prediction_times.append(pred_time)
            
            # Get prediction result
            logits = result[0]
            probabilities = tf.nn.softmax(logits).numpy()
            predicted_digit = np.argmax(probabilities)
            confidence = float(probabilities[predicted_digit])
            
            logger.info(f"Test prediction {i+1}/{num_predictions} completed in {pred_time:.4f} seconds")
            logger.info(f"Predicted digit: {predicted_digit}, confidence: {confidence:.4f}")
            
            # Run garbage collection between predictions
            gc.collect()
        
        # Print performance summary
        logger.info("\nPerformance Summary:")
        logger.info(f"Model loading time: {load_time:.4f} seconds")
        logger.info(f"Warmup prediction times: {[f'{t:.4f}' for t in warmup_times]} seconds")
        logger.info(f"Average warmup time: {sum(warmup_times)/len(warmup_times):.4f} seconds")
        logger.info(f"Test prediction times: {[f'{t:.4f}' for t in prediction_times]} seconds")
        logger.info(f"Average prediction time: {sum(prediction_times)/len(prediction_times):.4f} seconds")
        logger.info(f"Min prediction time: {min(prediction_times):.4f} seconds")
        logger.info(f"Max prediction time: {max(prediction_times):.4f} seconds")
        
        return True
    
    except Exception as e:
        logger.error(f"Error testing model: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test Keras model loading and prediction performance')
    parser.add_argument('--model_path', type=str, default='my_model.keras', help='Path to the Keras model file')
    parser.add_argument('--warmup', type=int, default=3, help='Number of warmup predictions')
    parser.add_argument('--predictions', type=int, default=10, help='Number of test predictions')
    args = parser.parse_args()
    
    # Ensure model path exists
    if not os.path.exists(args.model_path):
        logger.error(f"Model file not found: {args.model_path}")
        return False
    
    # Test model performance
    success = test_model_performance(
        model_path=args.model_path,
        num_warmup=args.warmup,
        num_predictions=args.predictions
    )
    
    return success

if __name__ == "__main__":
    main()