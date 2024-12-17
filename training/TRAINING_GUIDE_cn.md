# 手势识别模型训练

## 更新内容

[2024-12-01] CHANGELOG:

feat(data): 优化`train-Copy1.ipynb`数据增强策略
- 扩展图像旋转增强参数范围
- 新增水平/垂直翻转增强

perf(training): 引入差异化评估指标
- 为训练集/测试集分别设置独立准确率阈值
- 实现动态过拟合监控机制

此文件夹包含基于深度学习的手势识别系统的模型训练代码和导出模型。该项目旨在使用轻量级神经网络架构对 8 种不同的手势进行分类。

## 项目结构

```
.
├── best_model.pth
├── data_label_verification.ipynb
├── gesture_model.onnx
├── gesture_model.pth
├── gesture_model.tflite
├── model.ipynb
├── Onnx Inference.py
├── tf_gesture_model
│   ├── assets
│   ├── fingerprint.pb
│   ├── saved_model.pb
│   └── variables
│       ├── variables.data-00000-of-00001
│       └── variables.index
├── train-Copy1.ipynb
├── TRAINING_GUIDE_cn.md
├── TRAINING_GUIDE.md
└── train.ipynb
```

## 模型架构

### LightGestureNet
- 基于 MobileNetV2 的倒置残差块
- 针对移动和边缘部署进行了优化
- 输入：96x96 灰度图像
- 输出：8 个手势类
- 主要特点：
- 深度可分离卷积
- 残差连接
- 批量归一化
- ReLU6 激活函数

### 模型参数
```python
# 网络结构
first_layer = Conv2d(1, 16, 3, stride=2) # 初始卷积
inverted_residual_blocks = [
(16, 24, stride=2, expand_ratio=6),
(24, 24, stride=1, expand_ratio=6),
(24, 32, stride=2, expand_ratio=6),
(32, 32, stride=1, expand_ratio=6)
]
classifier = Linear(32, num_classes=8)
```

## 训练细节

### 数据预处理
- 图像调整为 96x96
- 灰度转换
- 归一化到 [0,1] 范围
- 数据增强：
- 随机旋转（±30°）
- 随机缩放（0.8-1.2x）
- 随机平移（±20%）

### 训练配置
- 优化器：Adam
- 学习率： 0.001，采用余弦退火
- 批次大小：32
- 损失函数：交叉熵
- 提前停止耐心：5 个时期
- 目标准确率阈值：99.27%

### 性能监控
- 跟踪的训练指标：
- 损失（训练和验证）
- 准确率（训练和验证）
- 学习率变化
- 提前停止条件

## 数据验证工具

`data_label_verification.ipynb` 笔记本提供以下工具：
- 数据集完整性验证
- 类分布可视化
- 使用简单 CNN 进行错误分析
- 样本可视化和检查
- 类平衡检查

## 导出的模型格式

### PyTorch 模型
- `best_model.pth`：训练期间表现最佳的检查点
- `gesture_model.pth`：最终训练模型
```python
import torch
from model import LightGestureNet

# 加载模型
model = LightGestureNet()
model.load_state_dict(torch.load('gesture_model.pth'))
model.eval()

# 推理
input_tensor = torch.randn(1, 1, 96, 96)
output = model(input_tensor)
```

### ONNX 格式
- `gesture_model.onnx`: 跨平台推理
```python
import onnxruntime

# 初始化会话
session = onnxruntime.InferenceSession('gesture_model.onnx')

# 推理
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: input_array})
```

### TensorFlow 格式
*使用 tensorflow 和 tensorflow lite 时，记得使用英文文档，不要使用中文文档。*
- `gesture_model.tflite`：移动部署就绪
```python
import tensorflow as tf

# 加载解释器
interpreter = tf.lite.Interpreter('gesture_model.tflite')
interpreter.allocate_tensors()

# 获取输入/输出详细信息
input_details = interpretationer.get_input_details()
output_details = interpretationer.get_output_details()

# 推理
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output = interpretationer.get_tensor(output_details[0]['index'])
```

- `tf_gesture_model/`：TensorFlow SavedModel
```python
import tensorflow as tf

# 加载模型
model = tf.saved_model.load('tf_gesture_model')

# 推理
predictions = model(input_tensor)
```

## 类映射
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

## 训练结果

模型实现：
- 训练准确率：>99%
- 验证准确率：>98%
- 平均推理时间：CPU 上约 5 毫秒
- 模型大小：
- PyTorch：约 2MB
- TFLite：约 1.5MB
- ONNX：约 2.2MB

## 未来改进

1. 数据增强增强：
-亮度变化
- 高斯噪声
- 随机擦除

2. 模型优化：
- 量化
- 修剪
- 知识蒸馏

3. 训练改进：
- 混合精度训练
- 梯度裁剪
- 标签平滑

## 要求

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
