# Gesture recognition system based on ESP32-S3 [中文](./README_cn.md)

A complete deep learning gesture recognition project, from model training to ESP32-S3 embedded deployment.

## Project structure

- training: Model training related files, including training code and various generated model files

- quantization: Model quantization optimization, implementing multiple quantization strategies to adapt to embedded devices

- deployment: ESP32-S3 deployment code, complete implementation based on ESP-IDF framework

- dataset: Contains gesture image datasets for training and testing

- environment: Environmental requirements (different steps require different environments).

## Main features

- Deep learning model for real-time gesture recognition
- Support multiple quantization strategies to adapt to resource-constrained devices
- Complete ESP32-S3 implementation based on ESP-IDF framework
- Provide pre-trained models in multiple formats