import base64
import io
import logging
import numpy as np
import cv2
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def decode_base64_image(image_data):
    """Decode base64 image data to a PIL Image."""
    try:
        # Handle data URL format (e.g., "data:image/png;base64,iVBORw0...")
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert('L')  # Convert to grayscale
        return image
    except Exception as e:
        logger.error(f"Error decoding base64 image: {str(e)}")
        return None

def find_bounding_box(img_array, threshold=0.1):
    """Find the bounding box of the content in the image."""
    rows = np.any(img_array > threshold, axis=1)
    cols = np.any(img_array > threshold, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        return None
    
    # Get the non-zero indices
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return cmin, rmin, cmax + 1, rmax + 1

def preprocess_image(image_data):
    """Preprocess the image data for model prediction."""
    try:
        # Decode base64 image
        image = decode_base64_image(image_data)
        if image is None:
            return None
        
        # Step 1: Convert to numpy array and normalize
        img_array = np.array(image).astype('float32') / 255.0
        
        # Step 2: Apply Gaussian blur to reduce noise
        img_array = cv2.GaussianBlur(img_array, (5, 5), 0)
        
        # Step 3: Apply thresholding to make the digit more distinct
        _, img_array = cv2.threshold(img_array, 0.2, 1.0, cv2.THRESH_BINARY)
        
        # Log min and max values for debugging
        logger.info(f"Processed image min: {img_array.min()}, max: {img_array.max()}")
        
        # Step 4: Find the bounding box of the digit
        if np.max(img_array) > 0:  # Check if there's any content
            # Convert to PIL Image for processing
            pil_image = Image.fromarray((img_array * 255).astype(np.uint8))
            
            # Find the bounding box of the content
            bbox = find_bounding_box(img_array)
            if bbox:
                left, top, right, bottom = bbox
                cropped_image = pil_image.crop((left, top, right, bottom))
            else:
                cropped_image = pil_image
        else:
            # If no content, use the original image
            cropped_image = Image.fromarray((img_array * 255).astype(np.uint8))
        
        # Step 5: Add padding to make the image square with some margin
        width, height = cropped_image.size
        # Calculate the size of the square image (max of height and width)
        size = max(width, height)
        # Add 20% padding around the digit for better recognition
        padding = int(size * 0.2)
        new_size = size + 2 * padding
        
        # Create a new, blank image with the new size
        padded_image = Image.new("L", (new_size, new_size), 0)
        # Calculate the position to place the cropped image with padding
        x_offset = padding + (size - width) // 2
        y_offset = padding + (size - height) // 2
        padded_image.paste(cropped_image, (x_offset, y_offset))
        
        # Step 6: Resize the image to 20x20 with antialiasing
        resized_image = padded_image.resize((20, 20), Image.LANCZOS)
        
        # Step 7: Pad to 28x28 (standard MNIST size) with the digit centered
        mnist_image = Image.new("L", (28, 28), 0)
        mnist_image.paste(resized_image, (4, 4))
        
        # Convert back to numpy array and normalize
        final_img = np.array(mnist_image).astype('float32') / 255.0
        
        # Reshape to match Keras/TensorFlow model input shape (1, 28, 28, 1)
        # TensorFlow uses NHWC format (batch, height, width, channels)
        final_img = final_img.reshape(1, 28, 28, 1)
        logger.info(f"Processed digit image shape: {final_img.shape}")
        
        return final_img
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None