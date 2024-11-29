# ESP32-S3 Model Deployment Guide [中文](./DEPLOYMENT_cn.md)

## Project Overview

This deployment project demonstrates running a quantized gesture recognition model on ESP32-S3. The implementation focuses on efficient memory usage, fast inference, and reliable model execution.

## Project Structure

```
.
├── model/                      # Model and header files directory
│   ├── test_image.hpp         # Generated image header
│   └── gesture_model.espdl    # Quantized model
├── CMakeLists.txt             # Project CMake configuration
├── app_main.cpp               # Main application code
├── generate_image_header.py   # Image preprocessing utility
├── pack_model.py              # Model packaging tool
└── partitions.csv            # Custom partition configuration
```

## Environment Setup

### Driver Installation
For new ESP32-S3 devices, you may need to install USB drivers:

1. CH340/CH341 Driver (Silicon Labs):
   - Required for USB communication
   - Detailed guide: [CH340/CH341 Installation Tutorial](https://blog.csdn.net/qq_52102933/article/details/126839474)

2. Alternative Driver Method:
   - Using Zadig tool
   - Guide: [USB Driver Installation](https://blog.csdn.net/k1e2n3n4y5/article/details/132684803)

### ESP-IDF Configuration 
Use `idf.py menuconfig` to configure:

1. Memory Configuration
   ```
   Component Config
   └── ESP32S3-Specific
       ├── Flash Size: 8MB
       └── Support for external RAM
           └── SPIRAM: Enabled
           └── Mode: Allow .bss segment placed in PSRAM
   ```

2. Partition Configuration
   ```
   Partition Table
   ├── Partition Table: Custom partition table CSV
   └── Custom partition CSV file: partitions.csv
   ```

3. Serial Communication
   ```
   Serial Flasher Config
   ├── Default serial port: [YOUR_PORT]
   └── Flash baud rate: 115200
   ```

4. Flash Size
   ```
   Serial Flasher Config
   └── Flash Size: 8MB
   ```

## Build Configuration

### Project CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.5)

# ESP-DL library path
set(EXTRA_COMPONENT_DIRS 
    "$ENV{HOME}/esp/esp-dl/esp-dl"     # Adjust path as needed
)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(gesture_recognition)
```

### Component CMakeLists.txt
```cmake
idf_component_register(
    SRCS 
        "app_main.cpp"
    INCLUDE_DIRS 
        "."
        "model"
    REQUIRES 
        esp-dl
)
```

## Memory Management

### PSRAM Utilization
- Model weights stored in PSRAM
- Input/output tensors allocated in PSRAM
- Runtime buffers use internal RAM when possible

### Memory Monitoring
The application includes memory monitoring:
```cpp
size_t free_mem = heap_caps_get_free_size(MALLOC_CAP_SPIRAM);
ESP_LOGI(TAG, "Free PSRAM: %u bytes", free_mem);
```

## Image Preprocessing

`generate_image_header.py` handles image preprocessing:
1. Grayscale conversion
2. Resize to 96x96
3. Normalization to [0,1]
4. INT8 quantization

Key parameters:
- Input size: 96x96
- Pixel format: Grayscale
- Quantization: INT8 (-128 to 127)
- Scale factor: 128 (for quantization)

## Model Loading and Inference

### Model Loading
- Models are loaded from a dedicated flash partition
- Partition defined in `partitions.csv`
- Uses ESP-DL's model loader interface

### Inference Pipeline
1. Input preparation
2. Model execution
3. Output processing
4. Confidence calculation

### Performance Monitoring
- Inference time measurement
- Memory usage tracking
- Model loading time monitoring

## Common Issues and Solutions

### Memory Errors
1. PSRAM Allocation Failure
   - Ensure PSRAM is enabled
   - Check partition table configuration
   - Monitor memory fragmentation

2. Stack Overflow
   - Increase stack size in menuconfig
   - Optimize recursive functions
   - Move large buffers to heap

### USB Communication Issues
1. Port Detection
   - Install correct drivers
   - Check USB cable
   - Verify port permissions

2. Flash Errors
   - Reduce flash speed in menuconfig
   - Check power supply stability
   - Verify flash size configuration

## References

### ESP-DL Documentation
- [Model Loading Tutorial](https://github.com/espressif/esp-dl/blob/master/tutorial/how_to_load_model_cn.md)
- [MobileNet V2 Deployment Guide](https://github.com/espressif/esp-dl/blob/master/tutorial/how_to_deploy_mobilenet_v2_cn.md)

### Community Resources
- [USB Driver Installation Guide](https://blog.csdn.net/qq_52102933/article/details/126839474)
- [Alternative Driver Setup](https://blog.csdn.net/k1e2n3n4y5/article/details/132684803)

### Official Documentation
- [ESP32-S3 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)
- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)