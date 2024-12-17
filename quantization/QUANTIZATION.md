# Model Quantization for ESP32-S3 [中文](./QUANTIZATION_cn.md)

This folder contains quantized models optimized for ESP32-S3 deployment, exploring three different quantization strategies to achieve the optimal balance between model size, accuracy, and inference speed.

## Updates

[2024-12-16] CHANGELOG:

perf(8bit_evaluate_quantized_model): Optimize the evaluation logic of the quantized model
- Fix the `bool` type error: When calculating the accuracy, the `.sum()` method is not available because `y_test` may not be a Tensor type (such as a Python list). Ensure its compatibility by explicitly converting `y_test` to `torch.Tensor`.
- Forced type conversion: Boolean comparison results (`predicted == y_test[...]`) are converted to integer Tensor, and the correctness of the summation operation is ensured by `.int()`.
- Shape matching check: Add assertions to check the shapes of `predicted` and `y_test` slices to prevent potential errors caused by mismatches.
- Enhanced debuggability: Add `print` debugging information output to quickly locate the problem of inconsistent shapes of `predicted` and `y_test` slices.

Test results:
On multiple batches of test data, the accuracy calculation results are consistent with expectations. The dimension mismatch and Boolean calculation anomalies that may occur during the evaluation process have been fixed, and the evaluation process is stable and reliable.

perf(8bit_predict): Optimize prediction batch processing logic
- Change single prediction to 32 batches: Simulate batch reasoning in actual deployment scenarios, because the quantized model may perform differently from single reasoning in batch processing
- Adjust softmax dim: Since the batch output shape changes from [1, num_classes] to [32, num_classes] and then takes the first result, the softmax dimension needs to be adjusted accordingly to maintain the correctness of the prediction probability calculation

Test results: The difference in accuracy before and after quantization on the test set is within the normal fluctuation range, indicating that this change has no effect on the quantization accuracy.

perf(mixed-Copy2-dispatch): Optimize high-precision quantization strategy
- Modify the first layer strategy to 32bit to completely avoid quantization effects
- Remove multiple layers of high-precision configuration and focus on the key bottleneck layer
- Supplement scale coefficient shift calculation

Test results: By focusing on the quantization effect of the first layer, the subsequent layers maintain 8bit and still achieve the target accuracy.

[2024-12-04] CHANGELOG:

perf(equalization): Optimize inter-layer equalization quantization parameter configuration

1. bias/activation equalization (multiplier=0.5): Control the equalization strength of bias and activation value by setting the multiplier to avoid excessive modification leading to decreased network expression ability

2. value_threshold(0.4→0.5)/iterations(4→10): Relax the threshold and increase the number of iterations to make the equalization process smoother and more gradual, and reduce quantization noise

3. kl calibration algorithm: Use the KL divergence algorithm to determine the optimal quantization range, which more accurately preserves the activation value distribution than the default method

Test results: The accuracy of the quantization model remains stable, and the parameter adjustment effectively reduces the accuracy loss caused by excessive equalization.

perf(mixed-Copy1-policy): Optimize mixed precision quantization configuration
- Streamline high-precision quantization layers, only keep the first layer of convolution and its activation function as 16bit
- Adjust GetTargetPlatform configuration to make the code more standardized
- Add power of 2 and other quantization attribute configurations to improve quantization efficiency

Test results: This optimization significantly reduces the model size while maintaining accuracy.

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