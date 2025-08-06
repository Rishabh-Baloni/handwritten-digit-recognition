#!/bin/bash

# Startup script for Render deployment
# This script will be executed before the application starts

echo "Starting application initialization..."

# Set TensorFlow environment variables for optimization
export TF_CPP_MIN_LOG_LEVEL=2
export TF_ENABLE_ONEDNN_OPTS=1
export TF_GPU_ALLOCATOR=cuda_malloc_async
export MALLOC_TRIM_THRESHOLD_=65536

# Run a Python script to pre-initialize the model
echo "Pre-initializing TensorFlow model..."
python -c "

import os
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras

print('TensorFlow version:', tf.__version__)
print('Keras version:', keras.__version__)

# Define custom InputLayer to handle batch_shape parameter
class CustomInputLayer(tf.keras.layers.InputLayer):
    def __init__(self, batch_shape=None, **kwargs):
        if batch_shape is not None:
            kwargs['input_shape'] = batch_shape[1:]
        super().__init__(**kwargs)

# Try loading with custom objects
custom_objects = {'InputLayer': CustomInputLayer}

# Get model path
model_path = os.path.join(os.getcwd(), 'my_model.keras')
print('Loading model from:', model_path)

# Load the model with custom objects and compile=False
start_time = time.time()
model = keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
load_time = time.time() - start_time
print(f'Model loaded in {load_time:.2f} seconds')

# Perform multiple warm-up predictions
print('Performing warm-up predictions...')
test_input = np.zeros((1, 28, 28, 1))

# First warm-up
start_time = time.time()
model.predict(test_input, verbose=0)
first_pred_time = time.time() - start_time
print(f'First prediction time: {first_pred_time:.2f} seconds')

# Second warm-up
start_time = time.time()
model.predict(test_input, verbose=0)
second_pred_time = time.time() - start_time
print(f'Second prediction time: {second_pred_time:.2f} seconds')

# Third warm-up
start_time = time.time()
model.predict(test_input, verbose=0)
third_pred_time = time.time() - start_time
print(f'Third prediction time: {third_pred_time:.2f} seconds')

print('Model initialization complete!')
"

echo "Initialization complete, starting application..."

# Start the application with the command from render.yaml
exec gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --graceful-timeout 120 --bind 0.0.0.0:$PORT