# 环境设置指南

## Conda 环境

### 训练环境 (dl_env)
用于：
- 数据集预处理
- 模型训练
- 基本评估

### 量化环境 (esp-dl)
用于：
- 模型量化
- 准确度评估
- ESP-DL 格式转换

## ESP-IDF 设置

### 版本要求
- ESP-IDF：v5.x（使用 v5.3.1 测试）
```bash
git clone -b v5.3.1 https://github.com/espressif/esp-idf.git
```

- ESP-DL：主分支（必需）
```bash
git clone https://github.com/espressif/esp-dl.git
```

重要说明：
- 请勿使用 ESP-DL 发布版本（idfv4.4 或 v1.1），因为它们会产生较差的量化结果
- 始终参考GitHub 文档而不是 PDF 手册，因为 GitHub 包含最新的教程和示例：
- ESP-IDF：https://github.com/espressif/esp-idf
- ESP-DL：https://github.com/espressif/esp-dl

### 环境激活

1. 如果处于活动状态，则退出 Conda 环境：
```bash
conda deactivate
```

2. 激活 ESP-IDF：
```bash
。 $IDF_PATH/export.sh
```

## 安装顺序

1. 使用提供的 YAML 文件安装 Conda 环境
2. 安装 ESP-IDF v5.x
3. 从 master 分支安装 ESP-DL
4. 配置系统路径和环境变量

## 依赖项管理

- 创建环境：`conda env create -f [environment].yml`
- 更新环境：`conda env update -f [environment].yml`
- 列出环境：`conda env list`
- 切换环境：`conda activate [env_name]`
