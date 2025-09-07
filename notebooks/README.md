# Notebooks

This folder contains Jupyter notebooks used for model development and training.

## Contents

- **Model Training Notebook**: The main notebook used to train the CNN model
- **Data Exploration**: Analysis and visualization of the MNIST dataset  
- **Model Evaluation**: Performance metrics and testing results
- **Experiments**: Various model architectures and hyperparameter tuning

## Dataset Setup

The notebooks automatically download the MNIST dataset using:
```python
import tensorflow as tf
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
```

No manual dataset setup required! 🎉

## Usage

1. Install Jupyter in your virtual environment:
   ```bash
   pip install jupyter matplotlib seaborn
   ```

2. Start Jupyter Lab/Notebook:
   ```bash
   jupyter lab
   # or
   jupyter notebook
   ```

3. Open the notebooks to see the training process and experiments

## Requirements

The notebooks use the same dependencies as the main application, plus:
- `jupyter` - Notebook environment
- `matplotlib` - Data visualization  
- `seaborn` - Advanced plotting
- `pandas` - Data manipulation (if used)

Install with:
```bash
pip install jupyter matplotlib seaborn pandas
```
