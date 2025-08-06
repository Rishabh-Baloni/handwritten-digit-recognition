import os
import logging
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
digit_recognizer = DigitRecognizer(model_path)

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
    return {"status": "ok", "model_loaded": digit_recognizer.model is not None}

@app.post("/predict")
async def predict_digit(image_request: ImageRequest):
    if not image_request.image:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = digit_recognizer.predict_digit(image_request.image)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)