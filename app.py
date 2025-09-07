import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
import io
from streamlit_drawable_canvas import st_canvas

# Configure the page
st.set_page_config(
    page_title="Handwritten Digit Recognition",
    page_icon="🔢",
    layout="centered"
)

# Load the model
@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        model = tf.keras.models.load_model('my_model.keras')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def preprocess_image(image_data):
    """Preprocess the drawn image for prediction"""
    if image_data is None:
        return None
    
    # Convert to PIL Image
    img = Image.fromarray(image_data.astype('uint8'), 'RGBA')
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Invert colors (make background black, drawing white)
    img = ImageOps.invert(img)
    
    # Resize to 28x28
    img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Normalize to 0-1 range
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = img_array.reshape(1, 28, 28, 1)
    
    return img_array

def predict_digit(model, image_array):
    """Make prediction on the preprocessed image"""
    if model is None or image_array is None:
        return None, None
    
    prediction = model.predict(image_array)
    predicted_digit = np.argmax(prediction)
    confidence = np.max(prediction)
    
    return predicted_digit, confidence

# Main app
def main():
    st.title("🔢 Handwritten Digit Recognition")
    st.write("Draw a digit (0-9) in the canvas below and get instant predictions!")
    
    # Load model
    model = load_model()
    
    if model is None:
        st.error("Failed to load the model. Please check if 'my_model.keras' exists.")
        return
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Draw Here:")
        
        # Create canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0.0)",  # Transparent fill
            stroke_width=20,
            stroke_color="black",
            background_color="white",
            height=280,
            width=280,
            drawing_mode="freedraw",
            key="canvas",
        )
    
    with col2:
        st.subheader("Prediction:")
        
        if canvas_result.image_data is not None:
            # Preprocess the image
            processed_image = preprocess_image(canvas_result.image_data)
            
            if processed_image is not None:
                # Make prediction
                digit, confidence = predict_digit(model, processed_image)
                
                if digit is not None:
                    # Display prediction
                    st.markdown(f"""
                    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin: 10px 0;">
                        <h1 style="color: #1f77b4; font-size: 3em; margin: 0;">{digit}</h1>
                        <p style="color: #666; margin: 5px 0;">Confidence: {confidence:.1%}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show confidence bar
                    st.progress(confidence)
                    
                    # Show processed image (for debugging)
                    with st.expander("View Processed Image"):
                        processed_img_display = processed_image[0, :, :, 0]
                        st.image(processed_img_display, caption="28x28 processed image", width=140)
        
        # Clear button
        if st.button("Clear Canvas", type="secondary"):
            st.rerun()
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    **Instructions:**
    1. Draw a single digit (0-9) in the canvas
    2. Make sure the digit is centered and clearly visible
    3. The model will predict the digit in real-time
    4. Use the "Clear Canvas" button to start over
    
    **Tips for better predictions:**
    - Draw digits similar to how they appear in handwritten text
    - Make sure the digit fills most of the canvas
    - Use clear, bold strokes
    """)

if __name__ == "__main__":
    main()
