from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
import io
import base64
import os

app = Flask(__name__)

# Load the model once when the app starts
model = None

def load_model():
    """Load the trained model"""
    global model
    try:
        # Try different loading methods for compatibility
        try:
            model = tf.keras.models.load_model('my_model.keras')
        except Exception as e1:
            print(f"First loading attempt failed: {e1}")
            try:
                # Try loading with compile=False
                model = tf.keras.models.load_model('my_model.keras', compile=False)
            except Exception as e2:
                print(f"Second loading attempt failed: {e2}")
                # Try loading with custom objects
                model = tf.keras.models.load_model('my_model.keras', compile=False, safe_mode=False)
        
        print("Model loaded successfully!")
        print(f"Model input shape: {model.input_shape}")
        print(f"Model output shape: {model.output_shape}")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def preprocess_canvas_image(image_data):
    """Preprocess the canvas image for prediction"""
    try:
        # Remove the data URL prefix (data:image/png;base64,)
        image_data = image_data.split(',')[1]
        
        # Decode base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        print(f"DEBUG: Original image size: {image.size}, mode: {image.mode}")
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Resize to 28x28
        image = image.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # The canvas has white background with black drawings
        # MNIST expects white digits on black background, so we need to invert
        img_array = 255 - img_array
        
        # Normalize to 0-1 range
        img_array = img_array.astype('float32') / 255.0
        
        # Add batch and channel dimensions
        img_array = img_array.reshape(1, 28, 28, 1)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get the image data from the request
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Preprocess the image
        processed_image = preprocess_canvas_image(image_data)
        
        if processed_image is None:
            return jsonify({'error': 'Failed to process image'}), 400
        
        # Make prediction
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        prediction = model.predict(processed_image)
        predicted_digit = int(np.argmax(prediction))
        confidence = float(np.max(prediction))
        
        # Get all predictions for confidence chart
        all_predictions = prediction[0].tolist()
        
        return jsonify({
            'digit': predicted_digit,
            'confidence': confidence,
            'all_predictions': all_predictions
        })
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    # Load the model
    if load_model():
        print("Starting Flask app...")
        print("Open your browser and go to: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model. Please check if 'my_model.keras' exists.")
