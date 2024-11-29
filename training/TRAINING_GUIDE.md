# Hand Gesture Recognition Model Training [中文](./TRAINING_GUIDE_cn.md)

This folder contains the model training code and exported models for a deep learning-based hand gesture recognition system. The project aims to classify 8 different hand gestures using a lightweight neural network architecture.

## Project Structure

```
.
├── model.ipynb                    # Model architecture definition
├── train.ipynb                    # Training script and procedures
├── data_label_verification.ipynb  # Dataset validation and analysis
├── best_model.pth                 # Best checkpoint during training
├── gesture_model.pth             # Final PyTorch model
├── gesture_model.onnx            # ONNX format model
├── gesture_model.tflite          # TensorFlow Lite model
└── tf_gesture_model/             # TensorFlow SavedModel directory
```

## Model Architecture

### LightGestureNet
- Based on MobileNetV2's inverted residual blocks
- Optimized for mobile and edge deployment
- Input: 96x96 grayscale images
- Output: 8 gesture classes
- Key features:
  - Depthwise separable convolutions
  - Residual connections
  - Batch normalization
  - ReLU6 activation functions

### Model Parameters
```python
# Network structure
first_layer = Conv2d(1, 16, 3, stride=2)  # Initial convolution
inverted_residual_blocks = [
    (16, 24, stride=2, expand_ratio=6),
    (24, 24, stride=1, expand_ratio=6),
    (24, 32, stride=2, expand_ratio=6),
    (32, 32, stride=1, expand_ratio=6)
]
classifier = Linear(32, num_classes=8)
```

## Training Details

### Data Preprocessing
- Image resizing to 96x96
- Grayscale conversion
- Normalization to [0,1] range
- Data augmentation:
  - Random rotation (±30°)
  - Random scaling (0.8-1.2x)
  - Random translation (±20%)

### Training Configuration
- Optimizer: Adam
- Learning rate: 0.001 with cosine annealing
- Batch size: 32
- Loss function: Cross-entropy
- Early stopping patience: 5 epochs
- Target accuracy threshold: 99.27%

### Performance Monitoring
- Training metrics tracked:
  - Loss (training and validation)
  - Accuracy (training and validation)
  - Learning rate changes
  - Early stopping conditions

## Data Verification Tools

The `data_label_verification.ipynb` notebook provides tools for:
- Dataset integrity validation
- Class distribution visualization
- Error analysis using a simple CNN
- Sample visualization and inspection
- Class balance checking

## Exported Model Formats

### PyTorch Models
- `best_model.pth`: Best performing checkpoint during training
- `gesture_model.pth`: Final trained model
```python
import torch
from model import LightGestureNet

# Load model
model = LightGestureNet()
model.load_state_dict(torch.load('gesture_model.pth'))
model.eval()

# Inference
input_tensor = torch.randn(1, 1, 96, 96)
output = model(input_tensor)
```

### ONNX Format
- `gesture_model.onnx`: Cross-platform inference
```python
import onnxruntime

# Initialize session
session = onnxruntime.InferenceSession('gesture_model.onnx')

# Inference
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: input_array})
```

### TensorFlow Formats
*When using tensorflow and tensorflow lite, remember to use English documents instead of Chinese documents.*
- `gesture_model.tflite`: Mobile deployment ready
```python
import tensorflow as tf

# Load interpreter
interpreter = tf.lite.Interpreter('gesture_model.tflite')
interpreter.allocate_tensors()

# Get input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Inference
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])
```

- `tf_gesture_model/`: TensorFlow SavedModel
```python
import tensorflow as tf

# Load model
model = tf.saved_model.load('tf_gesture_model')

# Inference
predictions = model(input_tensor)
```

## Class Mapping
```python
CLASS_NAMES = {
    0: 'palm',
    1: 'l',
    2: 'fist',
    3: 'thumb',
    4: 'index',
    5: 'ok',
    6: 'c',
    7: 'down'
}
```

## Training Results

The model achieves:
- Training accuracy: >99%
- Validation accuracy: >98%
- Average inference time: ~5ms on CPU
- Model size: 
  - PyTorch: ~2MB
  - TFLite: ~1.5MB
  - ONNX: ~2.2MB

## Future Improvements

1. Data augmentation enhancements:
   - Brightness variation
   - Gaussian noise
   - Random erasing

2. Model optimization:
   - Quantization
   - Pruning
   - Knowledge distillation

3. Training improvements:
   - Mixed precision training
   - Gradient clipping
   - Label smoothing

## Requirements

```python
torch>=1.8.0
torchvision>=0.9.0
onnx>=1.9.0
onnxruntime>=1.8.0
tensorflow>=2.5.0
numpy>=1.19.5
matplotlib>=3.3.4
tqdm>=4.60.0
```