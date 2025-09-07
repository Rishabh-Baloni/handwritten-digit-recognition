# 🔢 Handwritten Digit Recognition

A simple web application that recognizes handwritten digits (0-9) using a trained neural network model. Draw a digit on the canvas and get instant predictions!

![Demo](https://img.shields.io/badge/Demo-Streamlit-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange?style=for-the-badge)

## 🚀 Features

- **Interactive Drawing Canvas**: Draw digits directly in your browser
- **Real-time Predictions**: Get instant predictions as you draw
- **High Accuracy**: Uses a trained CNN model for accurate digit recognition
- **Clean Interface**: Simple, user-friendly web interface
- **Confidence Scores**: See how confident the model is about its predictions

## 📁 Project Structure

```
handwritten-digit-recognition/
├── app.py              # Main Streamlit application
├── my_model.keras      # Trained neural network model
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── run.bat            # Windows run script (optional)
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No additional packages needed (everything installs in virtual environment)

### Quick Start (Recommended)

#### Windows Users:
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/handwritten-digit-recognition.git
   cd handwritten-digit-recognition
   ```

2. **One-click setup and run**
   ```batch
   run.bat
   ```
   This will:
   - Create a virtual environment (venv folder)
   - Install all dependencies in the virtual environment
   - Start the application
   - **Nothing gets installed globally on your system!**

#### Linux/Mac Users:
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/handwritten-digit-recognition.git
   cd handwritten-digit-recognition
   ```

2. **Make script executable and run**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### 🔒 Virtual Environment Benefits
- **Isolated Environment**: All packages install in the `venv` folder
- **No System Pollution**: Your global Python remains untouched
- **Easy Cleanup**: Just delete the `venv` folder to remove everything
- **Consistent Dependencies**: Everyone gets the exact same package versions

## 🎯 How to Use

1. **Draw a Digit**: Use your mouse to draw a digit (0-9) on the white canvas
2. **Get Prediction**: The model will automatically predict the digit you drew
3. **Check Confidence**: See how confident the model is about its prediction
4. **Clear & Retry**: Click "Clear Canvas" to draw a new digit

### Tips for Better Predictions
- Draw digits clearly and boldly
- Center the digit in the canvas
- Make the digit fill most of the drawing area
- Use continuous strokes when possible

## 🧠 Model Information

- **Architecture**: Convolutional Neural Network (CNN)
- **Training Dataset**: MNIST handwritten digits
- **Input Size**: 28x28 grayscale images
- **Output**: 10 classes (digits 0-9)
- **Performance**: High accuracy on handwritten digit recognition

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web framework for the user interface
- **TensorFlow**: Machine learning framework for model inference
- **NumPy**: Numerical computing for image processing
- **Pillow**: Image processing library
- **streamlit-drawable-canvas**: Interactive drawing component

### Image Processing Pipeline
1. Capture drawing from canvas
2. Convert to grayscale
3. Invert colors (black background, white digit)
4. Resize to 28x28 pixels
5. Normalize pixel values (0-1 range)
6. Add batch dimension for model input

## 🚀 Deployment Options

This app can be easily deployed on various platforms:

- **Streamlit Cloud**: Connect your GitHub repo for free hosting
- **Heroku**: Deploy with a simple `Procfile`
- **Railway**: One-click deployment from GitHub
- **Local Network**: Run locally and share IP address

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- Report bugs or issues
- Suggest new features
- Improve documentation
- Optimize model performance
- Enhance user interface

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/handwritten-digit-recognition/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your environment and the issue

## ⭐ Acknowledgments

- MNIST dataset for training data
- TensorFlow team for the machine learning framework
- Streamlit team for the amazing web framework
- Open source community for various tools and libraries

---

**Happy digit recognition! 🎉**
