# Environment Setup Guide

## Conda Environments

### Training Environment (dl_env)
Used for:
- Dataset preprocessing
- Model training
- Basic evaluation

### Quantization Environment (esp-dl)
Used for:
- Model quantization
- Accuracy evaluation
- ESP-DL format conversion

## ESP-IDF Setup

### Version Requirements
- ESP-IDF: v5.x (tested with v5.3.1)
  ```bash
  git clone -b v5.3.1 https://github.com/espressif/esp-idf.git
  ```

- ESP-DL: master branch (required)
  ```bash
  git clone https://github.com/espressif/esp-dl.git
  ```

Important Notes:
- Do not use ESP-DL release versions (idfv4.4 or v1.1) as they produce inferior quantization results
- Always refer to GitHub documentation instead of PDF manuals, as GitHub contains the most up-to-date tutorials and examples:
  - ESP-IDF: https://github.com/espressif/esp-idf
  - ESP-DL: https://github.com/espressif/esp-dl

### Environment Activation

1. Exit Conda environment if active:
   ```bash
   conda deactivate
   ```

2. Activate ESP-IDF:
   ```bash
   . $IDF_PATH/export.sh
   ```

## Installation Order

1. Install Conda environments using provided YAML files
2. Install ESP-IDF v5.x
3. Install ESP-DL from master branch
4. Configure system paths and environment variables

## Dependencies Management

- Create environment: `conda env create -f [environment].yml`
- Update environment: `conda env update -f [environment].yml`
- List environments: `conda env list`
- Switch environment: `conda activate [env_name]`