import os
import tensorflow as tf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Print versions
print(f'TensorFlow version: {tf.__version__}')
print(f'Keras version: {tf.keras.__version__}')

# Model path
model_path = os.path.join(os.getcwd(), 'my_model.keras')
print(f'Model path: {model_path}')
print(f'Model exists: {os.path.exists(model_path)}')

# Try to load the model with custom objects
try:
    # Attempt 1: Standard loading
    print("\nAttempt 1: Standard loading")
    try:
        model = tf.keras.models.load_model(model_path)
        print("Standard loading successful!")
    except Exception as e:
        print(f"Standard loading failed: {str(e)}")
    
    # Attempt 2: With custom InputLayer handling
    print("\nAttempt 2: With custom InputLayer handling")
    
    # Custom InputLayer to handle batch_shape
    class CustomInputLayer(tf.keras.layers.InputLayer):
        def __init__(self, batch_shape=None, **kwargs):
            if batch_shape is not None:
                kwargs['input_shape'] = batch_shape[1:]
            super().__init__(**kwargs)
        
        def compute_output_shape(self, input_shape):
            return input_shape
        
        def call(self, inputs):
            return inputs
        
        def get_config(self):
            config = super().get_config()
            return config
    
    # Try loading with custom objects
    custom_objects = {'InputLayer': CustomInputLayer}
    try:
        # Try to load with compile=False to avoid jit_compile issues
        model = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
        print("Loading with custom objects successful!")
        # Print model summary
        model.summary()
    except Exception as e:
        print(f"Loading with custom objects failed: {str(e)}")
    
    # Attempt 3: Try loading with tf.saved_model.load
    print("\nAttempt 3: Using tf.saved_model.load")
    try:
        model = tf.saved_model.load(model_path)
        print("Loading with tf.saved_model.load successful!")
    except Exception as e:
        print(f"Loading with tf.saved_model.load failed: {str(e)}")

except Exception as e:
    print(f"Error in test script: {str(e)}")