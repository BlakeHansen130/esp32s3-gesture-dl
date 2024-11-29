# 手势识别数据集

[![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-blue.svg)](https://www.kaggle.com/datasets/gti-upm/leapgestrecog)

基于 Kaggle 的 [LeapGestRecog 数据集](https://www.kaggle.com/datasets/gti-upm/leapgestrecog) 进行手势识别的预处理数据集。

## 数据集结构

- `train.pkl`：训练数据集（12,800 个样本）
- `cal.pkl`：校准数据集（1,600 个样本）
- `test.pkl`：测试数据集（1,600 个样本）
- `dataset.ipynb`：数据预处理和生成笔记本

每个 pickle 文件包含一个 (X, y) 元组，其中：
- X：形状为 (n_samples, 96, 96) 的图像数据数组，标准化为 [0,1]
- y：形状为 (n_samples,) 的标签数组

## 手势类别

数据集包括 8 种手势类型：
- 0：手掌
- 1：l
- 2：拳头
- 3：拇指
- 4：食指
- 5：ok
- 6：c
- 7：向下

## 数据特征

- 图像大小：96x96 像素
- 颜色格式：灰度
- 值范围：0-1（float32）
- 总样本数：16,000
- 分割比例：80% 训练，10% 校准，10% 测试

## 用法

```python
import pickle

# 加载数据集
with open('train.pkl', 'rb') as f:
X_train, y_train = pickle.load(f)

with open('cal.pkl', 'rb') as f:
X_cal, y_cal = pickle.load(f)

with open('test.pkl', 'rb') as f:
X_test, y_test = pickle.load(f)

# 如果需要，添加通道维度
X_train = X_train[..., np.newaxis] # 形状变为 (n_samples, 96, 96, 1)
```

## 预处理步骤
1. 转换为灰度
2. 调整大小为 96x96
3. 将像素值标准化为 [0,1]
4. 分成训练/校准/测试集
