import os
import logging
import time
import gc
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from .model import DigitRecognizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Digit Recognition API", description="API for recognizing handwritten digits using TensorFlow")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the digit recognizer with the Keras model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'my_model.keras')

# Log the model path for debugging
logger.info(f"Model path: {model_path}")
logger.info(f"Model file exists: {os.path.exists(model_path)}")

# Try to initialize the digit recognizer
try:
    digit_recognizer = DigitRecognizer(model_path)
    if digit_recognizer.model is None:
        logger.error("Failed to load the model. The model object is None.")
        # Try to reload the model
        logger.info("Attempting to reload the model...")
        digit_recognizer.load_model()
        
        if digit_recognizer.model is None:
            logger.error("Model reload attempt failed. The model is still None.")
            # Set a flag to indicate model loading failure
            model_load_failed = True
        else:
            logger.info("Model reload successful!")
            model_load_failed = False
    else:
        logger.info("Model loaded successfully on first attempt!")
        model_load_failed = False
except Exception as e:
    logger.error(f"Error initializing digit recognizer: {str(e)}")
    import traceback
    logger.error(f"Stack trace: {traceback.format_exc()}")
    digit_recognizer = None
    model_load_failed = True

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Define request model
class ImageRequest(BaseModel):
    image: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse(os.path.join(static_dir, 'index.html'))

@app.get("/health")
async def health_check():
    if digit_recognizer is None:
        return {"status": "error", "model_loaded": False, "error": "Digit recognizer not initialized"}
    
    model_status = digit_recognizer.model is not None
    return {
        "status": "ok" if model_status else "error", 
        "model_loaded": model_status,
        "model_path": model_path,
        "model_path_exists": os.path.exists(model_path)
    }

@app.get("/test-prediction")
async def test_prediction():
    """Endpoint to test model prediction with a dummy input to ensure model is fully initialized."""
    if digit_recognizer is None or digit_recognizer.model is None:
        return {"status": "error", "model_loaded": False, "error": "Model not initialized"}
    
    try:
        # Create a dummy input (all zeros)
        test_input = np.zeros((1, 28, 28, 1))
        
        # Time the prediction
        start_time = time.time()
        logger.info("Running test prediction...")
        
        # Run prediction with verbose=0 to reduce logging
        logits = digit_recognizer.model.predict(test_input, verbose=0)[0]
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        logger.info(f"Test prediction completed in {elapsed_time:.2f} seconds")
        
        # Convert logits to probabilities
        probabilities = tf.nn.softmax(logits).numpy()
        predicted_digit = np.argmax(probabilities)
        
        return {
            "status": "ok",
            "prediction_time_ms": int(elapsed_time * 1000),
            "test_digit": int(predicted_digit),
            "model_ready": True
        }
    except Exception as e:
        logger.error(f"Error in test prediction: {str(e)}")
        return {"status": "error", "error": str(e)}

@app.post("/predict")
async def predict_digit(image_request: ImageRequest):
    if not image_request.image:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    # Check if digit recognizer is initialized
    if digit_recognizer is None:
        logger.error("Digit recognizer not initialized")
        try:
            logger.warning("Model not initialized, attempting to reload...")
            global digit_recognizer
            digit_recognizer = DigitRecognizer(model_path)
            
            # Run a test prediction to ensure model is ready
            test_input = np.zeros((1, 28, 28, 1))
            logger.info("Running test prediction after reload...")
            digit_recognizer.model.predict(test_input, verbose=0)
            logger.info("Test prediction after reload successful")
        except Exception as e:
            logger.error(f"Failed to reload model: {str(e)}")
            raise HTTPException(status_code=500, detail="Model not initialized and reload failed")
    
    # Check if model is loaded
    if digit_recognizer.model is None:
        logger.error("Model not loaded")
        # Try to reload the model
        logger.info("Attempting to reload the model before prediction...")
        model_loaded = digit_recognizer.load_model()
        
        if not model_loaded or digit_recognizer.model is None:
            logger.error("Model reload failed before prediction")
            raise HTTPException(status_code=500, detail="Model not loaded and reload attempt failed")
    
    try:
        # Log request received timestamp
        request_time = time.time()
        logger.info(f"Prediction request received at {request_time}")
        
        # Process the prediction with timing
        result = digit_recognizer.predict_digit(image_request.image)
        
        # Log total request processing time
        total_time = time.time() - request_time
        logger.info(f"Total prediction request processed in {total_time:.4f} seconds")
        
        # Add total processing time to the response
        result["total_processing_time_ms"] = int(total_time * 1000)
        
        if "error" in result:
            logger.error(f"Error in prediction: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)