# Handwritten Digit Recognition Application

This application uses a pre-trained Keras/TensorFlow model to recognize handwritten digits. The model is loaded from `my_model.keras` and is used to make real-time predictions on digits drawn by the user.

## Features

- Interactive canvas for drawing digits
- Real-time digit recognition using a PyTorch model
- Visualization of prediction probabilities for each digit
- Responsive design that works on both desktop and mobile devices

## Technical Details

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **Model**: Keras/TensorFlow model for digit recognition
- **Image Processing**: OpenCV and PIL for preprocessing drawn digits
- **Server**: Uvicorn/Gunicorn

## How It Works

1. The user draws a digit on the canvas
2. The drawn image is sent to the FastAPI backend
3. The backend preprocesses the image:
   - Converts to grayscale
   - Applies Gaussian blur to reduce noise
   - Thresholds the image to make the digit more distinct
   - Crops to the content area
   - Adds padding to center the digit
   - Resizes to 28x28 pixels (MNIST format)
4. The preprocessed image is fed into the Keras/TensorFlow model
5. The model returns prediction probabilities for each digit (0-9)
6. The results are displayed to the user

## Project Structure

```
digit-recognition-app/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app
│   ├── model.py           # Load model and predict
│   └── utils.py           # Image preprocessing
├── static/
│   ├── index.html         # Landing page
│   └── digit-recognition.html  # Frontend with canvas + JS
├── my_model.keras         # Trained Keras/TensorFlow model
├── requirements.txt
└── README.md
```

## Setup and Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the FastAPI application with Uvicorn:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. For production deployment with Gunicorn:
   ```
   gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

4. Open a web browser and navigate to:
   ```
   http://localhost:8000
   ```

## Deployment

This application can be easily deployed to platforms like Render, Railway, or Heroku. For Render, you can use the following configuration:

1. Create a `render.yaml` file with:
   ```yaml
   services:
     - type: web
       name: digit-recognition
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.8
   ```

2. Or set the start command in the Render dashboard to:
   ```
   gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```