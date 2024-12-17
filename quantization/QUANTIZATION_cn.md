# ESP32-S3 的模型量化

此文件夹包含针对 ESP32-S3 部署优化的量化模型，探索三种不同的量化策略，以实现模型大小、准确率和推理速度之间的最佳平衡。

## 更新内容

[2024-12-16] CHANGELOG:

perf(8bit_evaluate_quantized_model)：优化量化模型评估逻辑  
- 修复 `bool` 类型报错问题：在计算准确率时，由于 `y_test` 可能非 Tensor 类型（如 Python 列表），导致 `.sum()` 方法不可用。通过显式将 `y_test` 转换为 `torch.Tensor`，确保其兼容性。
- 强制类型转换：布尔比较结果（`predicted == y_test[...]`）被转换为整数 Tensor，通过 `.int()` 确保求和操作的正确性。
- 形状匹配检查：增加断言，检查 `predicted` 与 `y_test` 切片的形状，防止不匹配导致潜在错误。
- 增强可调试性：增加 `print` 调试信息输出，快速定位 `predicted` 和 `y_test` 切片形状不一致问题。

测试结果：  
在多批次测试数据上，准确率计算结果与预期一致，修复了评估过程中可能导致的维度不匹配与布尔计算异常问题，评估流程稳定可靠。  

perf(8bit_predict): 优化预测批处理逻辑
- 将单张预测修改为32个batch: 模拟实际部署场景下的batch推理，因为量化后的模型在批处理时可能表现与单张推理有差异
- softmax的dim调整: 由于batch输出形状从[1,num_classes]变为[32,num_classes]后取第一个结果，需要相应调整softmax的维度以保持预测概率计算的正确性

测试结果：在测试集上量化前后准确率差异在正常波动范围内，表明该改动对量化精度无影响。

perf(mixed-Copy2-dispatch): 优化高精度量化策略
- 修改第一层策略为32bit，完全避免量化影响
- 移除多层高精度配置，聚焦关键瓶颈层
- 补充scale系数移位计算

测试结果：通过关注第一层的量化效果，后续层保持8bit依然达到目标精度。

[2024-12-04] CHANGELOG:

perf(equalization): 优化层间均衡量化参数配置
1. bias/activation均衡(multiplier=0.5): 通过设置乘数控制偏置项和激活值的均衡强度，避免过度修改导致网络表达能力下降

2. value_threshold(0.4→0.5)/iterations(4→10): 放宽阈值并增加迭代次数，使均衡过程更平滑渐进，减少量化噪声

3. kl校准算法: 使用KL散度算法确定最优量化范围，相比默认方法更准确地保留激活值分布

测试结果：量化模型准确率保持稳定，调参有效减少均衡过度带来的精度损失。

perf(mixed-Copy1-policy): 优化混合精度量化配置
- 精简高精度量化层，仅保留第一层卷积和其激活函数为16bit
- 调整GetTargetPlatform配置方式，使代码更规范
- 新增power of 2等量化属性配置，提高量化效率

测试结果：该优化在保持精度的同时，显著降低了模型大小。

## 目录结构

```
.
├── QUANTIZATION_cn.md
├── QUANTIZATION.md
├── quantize_8bit-Copy1.ipynb
├── quantize_8bit.ipynb
├── quantize_equalization-Copy1.ipynb
├── quantize_equalization.ipynb
├── quantize_mixed-Copy1.ipynb
├── quantize_mixed-Copy2.ipynb
└── quantize_mixed.ipynb
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
