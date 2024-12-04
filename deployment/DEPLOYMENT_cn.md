# ESP32-S3 模型部署指南

## 更新内容

[2024-12-01] CHANGELOG:

feat(preprocessing): 新增肤色检测与图像预处理模块
- 实现基于YCrCb色彩空间的智能肤色分割
- 引入形态学优化(OPEN/CLOSE)提升边缘检测质量
- 集成自适应对比度增强(α=1.5)与动态二值化
- 新增健壮的异常处理机制
- 支持命令行调用及批处理功能
- 标准化输出路径管理，自动创建目标文件夹

build(env): 配置依赖
- 引入OpenCV核心模块
- 集成NumPy数值计算支持

## 项目概述

此部署项目演示了如何在 ESP32-S3 上运行量化手势识别模型。实现侧重于高效的内存使用、快速推理和可靠的模型执行。

## 项目结构

```
.
═── model/ # 模型和头文件目录
│ ═── test_image.hpp # 生成的图像头文件
│ └──gesture_model.espdl # 量化模型
═── CMakeLists.txt # 项目 CMake 配置
═── app_main.cpp # 主应用程序代码
═──generate_image_header.py # 图像预处理实用程序
═──pack_model.py # 模型打包工具
└──partitions.csv # 自定义分区配置
```

## 环境设置

### 驱动程序安装
对于新的 ESP32-S3 设备，您可能需要安装 USB 驱动程序：

1. CH340/CH341 驱动程序（Silicon Labs）：
- USB 通信所需
- 详细指南：[CH340/CH341 安装教程](https://blog.csdn.net/qq_52102933/article/details/126839474)

2. 替代驱动方法：
- 使用 Zadig 工具
- 指南：[USB 驱动安装](https://blog.csdn.net/k1e2n3n4y5/article/details/132684803)

### ESP-IDF 配置
使用 `idf.py menuconfig` 进行配置：

1. 内存配置
```
组件配置
└── ESP32S3-Specific
└── Flash 大小：8MB
└── 支持外部 RAM
└── SPIRAM：已启用
└── 模式：允许 .bss 段放置在 PSRAM 中
```

2. 分区配置
```
分区表
└── 分区表：自定义分区表 CSV
└── 自定义分区CSV 文件：partitions.csv
```

3. 串行通信
```
串行 Flasher 配置
═── 默认串行端口：[YOUR_PORT]
└── Flash 波特率：115200
```

4. Flash 大小
```
串行 Flasher 配置
└── Flash 大小：8MB
```

## 构建配置

### 项目 CMakeLists.txt
```cmake
cmake_minimum_required(VERSION 3.5)

# ESP-DL 库路径
set(EXTRA_COMPONENT_DIRS
"$ENV{HOME}/esp/esp-dl/esp-dl" # 根据需要调整路径
)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(gesture_recognition)
```

### 组件CMakeLists.txt
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

## 内存管理

### PSRAM 利用率
- 模型权重存储在 PSRAM 中
- 输入/输出张量分配在 PSRAM 中
- 运行时缓冲区尽可能使用内部 RAM

### 内存监控
应用程序包括内存监控：
```cpp
size_t free_mem = heap_caps_get_free_size(MALLOC_CAP_SPIRAM);
ESP_LOGI(TAG, "可用 PSRAM：%u 字节", free_mem);
```

## 图像预处理

`generate_image_header.py` 处理图像预处理：
1. 灰度转换
2. 调整大小为 96x96
3. 归一化为 [0,1]
4. INT8 量化

关键参数：
- 输入大小：96x96
- 像素格式：灰度
- 量化：INT8（-128 至 127）
- 比例因子：128（用于量化）

## 模型加载和推理

### 模型加载
- 模型从专用闪存分区加载
- 在 `partitions.csv` 中定义的分区
- 使用 ESP-DL 的模型加载器接口

### 推理管道
1. 输入准备
2. 模型执行
3. 输出处理
4. 置信度计算

### 性能监控
- 推理时间测量
- 内存使用情况跟踪
- 模型加载时间监控

## 常见问题和解决方案

### 内存错误
1. PSRAM 分配失败
- 确保 PSRAM 已启用
- 检查分区表配置
- 监控内存碎片

2. 堆栈溢出
- 在 menuconfig 中增加堆栈大小
- 优化递归函数
- 将大缓冲区移至堆

### USB 通信问题
1. 端口检测
- 安装正确的驱动程序
- 检查 USB 电缆
- 验证端口权限

2. 闪存错误
- 在 menuconfig 中降低闪存速度
- 检查电源稳定性
- 验证闪存大小配置

## 参考资料

### ESP-DL 文档
- [模型加载教程](https://github.com/espressif/esp-dl/blob/master/tutorial/how_to_load_model_cn.md)
- [MobileNet V2 部署指南](https://github.com/espressif/esp-dl/blob/master/tutorial/how_to_deploy_mobilenet_v2_cn.md)

### 社区资源
- [USB 驱动程序安装指南](https://blog.csdn.net/qq_52102933/article/details/126839474)
- [替代驱动程序设置](https://blog.csdn.net/k1e2n3n4y5/article/details/132684803)

### 官方文档
- [ESP32-S3 技术参考](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)
- [ESP-IDF 编程指南](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
