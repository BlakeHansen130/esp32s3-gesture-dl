# Model Quantization for ESP32-S3 [中文](./QUANTIZATION_cn.md)

This folder contains quantized models optimized for ESP32-S3 deployment, exploring three different quantization strategies to achieve the optimal balance between model size, accuracy, and inference speed.

## Directory Structure

```
.
├── gesture_model_int8/
│   ├── gesture_model_int8.espdl    # INT8 quantized model
│   ├── gesture_model_int8.info     # Performance metrics
│   └── gesture_model_int8.json     # Model configuration
├── gesture_model_mixed/
│   ├── gesture_model_mixed.espdl   # Mixed precision model
│   ├── gesture_model_mixed.info    # Performance metrics
│   └── gesture_model_mixed.json    # Model configuration
├── gesture_model_balanced/
│   ├── gesture_model_balanced.espdl # Equalized model
│   ├── gesture_model_balanced.info  # Performance metrics
│   └── gesture_model_balanced.json  # Model configuration
└── notebooks/
    ├── quantize_8bit.ipynb         # INT8 quantization script
    ├── quantize_mixed.ipynb        # Mixed precision script
    └── quantize_equalization.ipynb  # Equalization script
```

## Quantization Methods

### 1. INT8 Quantization
Implementation: `quantize_8bit.ipynb`

Baseline quantization approach:
- Uniform 8-bit quantization across all layers
- Symmetric quantization scheme
- Per-channel quantization for weights
- Per-tensor quantization for activations

### 2. Mixed Precision Quantization
Implementation: `quantize_mixed.ipynb`

Uses combination of 8-bit and 16-bit quantization:
- Default: 8-bit precision
- Critical layers: 16-bit precision
- Layer-specific optimization based on error sensitivity

### 3. Equalization-Aware Quantization
Implementation: `quantize_equalization.ipynb`

Layer-wise scaling optimization:
- Iterations: 4
- Value threshold: 0.4
- Optimization level: 2
- ReLU6 to ReLU conversion for compatibility

## Model Requirements

### Input Format
- Size: 96x96 pixels
- Channels: Grayscale (1 channel)
- Type: float32
- Range: [0,1]
- Shape: [1, 1, 96, 96]

### Dependencies
- PPQ (PyTorch Post-training Quantization toolkit)
- PyTorch >= 1.8.0
- ONNX >= 1.9.0
- OpenCV >= 4.5.0
- NumPy >= 1.19.0
- ESP-IDF >= 4.4.0
- ESP-DL >= 1.0.0

## Future Optimizations

1. Dynamic quantization
   - Runtime activation quantization
   - Adaptive input handling

2. Hardware-aware optimization
   - ESP32-S3 specific features
   - Hardware acceleration

3. Advanced calibration
   - Entropy-based methods
   - Per-layer strategies

4. Post-training optimization
   - Weight pruning
   - Channel reduction
   - Knowledge distillation

## References

### ESP-DL Framework Documentation
ESP-DL is Espressif's deep learning framework for ESP32 series chips:
- [ESP-DL Main Repository](https://github.com/espressif/esp-dl) - Core framework with Chinese documentation
- [Model Quantization Guide](https://github.com/espressif/esp-dl/blob/master/tutorial/how_to_quantize_model_cn.md)

### ESP-PPQ Documentation
ESP-PPQ is the post-training quantization toolkit for ESP32 chips:

1. API Interface
   - [ESP-DL Interface](https://github.com/espressif/esp-ppq/blob/master/ppq/api/espdl_interface.py)
   - [Core API](https://github.com/espressif/esp-ppq/blob/master/ppq/api/interface.py)
   - [Usage Guide](https://github.com/espressif/esp-ppq/blob/master/md_doc/how_to_use.md)

2. Quantization Engine
   - [Quantizer Documentation](https://github.com/espressif/esp-ppq/blob/master/ppq/quantization/quantizer/README.md)
   - [Executor Implementation](https://github.com/espressif/esp-ppq/blob/master/ppq/executor/README.md)
   - [Base Executor](https://github.com/espressif/esp-ppq/blob/master/ppq/executor/base.py)
   - [PyTorch Executor](https://github.com/espressif/esp-ppq/blob/master/ppq/executor/torch.py)