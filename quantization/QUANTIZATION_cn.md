# ESP32-S3 的模型量化

此文件夹包含针对 ESP32-S3 部署优化的量化模型，探索三种不同的量化策略，以实现模型大小、准确率和推理速度之间的最佳平衡。

## 目录结构

```
.
═──gesture_model_int8/
│ ═──gesture_model_int8.espdl # INT8 量化模型
│ ═──gesture_model_int8.info # 性能指标
│ └──gesture_model_int8.json # 模型配置
═──gesture_model_mixed/
│ ═──gesture_model_mixed.espdl # 混合精度模型
│ ═──gesture_model_mixed.info # 性能指标
│ └──gesture_model_mixed.json # 模型配置
═──gesture_model_balanced/
│ ═──gesture_model_balanced.espdl # 均衡模型
│ ═──gesture_model_balanced.info # 性能指标
│ └──gesture_model_balanced.json # 模型配置
└──notebooks/
═──quantize_8bit.ipynb # INT8 量化脚本
═──quantize_mixed.ipynb # 混合精度脚本
└── quantize_equalization.ipynb # 均衡脚本
```

## 量化方法

### 1. INT8 量化
实现：`quantize_8bit.ipynb`

基线量化方法：
- 所有层均采用统一的 8 位量化
- 对称量化方案
- 权重的每个通道量化
- 激活的每个张量量化

### 2. 混合精度量化
实现：`quantize_mixed.ipynb`

使用 8 位和 16 位量化的组合：
- 默认：8 位精度
- 关键层：16 位精度
- 根据误差敏感度进行层特定优化

### 3. 均衡感知量化
实现：`quantize_equalization.ipynb`

逐层缩放优化：
- 迭代次数：4
-值阈值：0.4
- 优化级别：2
- ReLU6 转换为 ReLU 以实现兼容性

## 模型要求

### 输入格式
- 大小：96x96 像素
- 通道：灰度（1 通道）
- 类型：float32
- 范围：[0,1]
- 形状：[1, 1, 96, 96]

### 依赖项
- PPQ（PyTorch 训练后量化工具包）
- PyTorch >= 1.8.0
- ONNX >= 1.9.0
- OpenCV >= 4.5.0
- NumPy >= 1.19.0
- ESP-IDF >= 4.4.0
- ESP-DL >= 1.0.0

## 未来优化

1. 动态量化
- 运行时激活量化
- 自适应输入处理

2. 硬件感知优化
- ESP32-S3 特定功能
- 硬件加速

3. 高级校准
- 基于熵的方法
- 每层策略

4. 训练后优化
- 权重修剪
- 通道减少
- 知识蒸馏

## 参考资料

### ESP-DL 框架文档
ESP-DL 是 Espressif 针对 ESP32 系列芯片的深度学习框架：
- [ESP-DL 主存储库](https://github.com/espressif/esp-dl) - 带中文文档的核心框架
- [模型量化指南](https://github.com/espressif/esp-dl/blob/master/tutorial/how_to_quantize_model_cn.md)

### ESP-PPQ 文档
ESP-PPQ 是针对 ESP32 芯片的训练后量化工具包：

1. API 接口
- [ESP-DL 接口](https://github.com/espressif/esp-ppq/blob/master/ppq/api/espdl_interface.py)
- [核心API](https://github.com/espressif/esp-ppq/blob/master/ppq/api/interface.py)
- [使用指南](https://github.com/espressif/esp-ppq/blob/master/md_doc/how_to_use.md)

2. 量化引擎
- [量化器文档](https://github.com/espressif/esp-ppq/blob/master/ppq/quantization/quantizer/README.md)
- [执行器实现](https://github.com/espressif/esp-ppq/blob/master/ppq/executor/README.md)
- [基本执行器](https://github.com/espressif/esp-ppq/blob/master/ppq/executor/base.py)
- [PyTorch执行器](https://github.com/espressif/esp-ppq/blob/master/ppq/executor/torch.py​​)
