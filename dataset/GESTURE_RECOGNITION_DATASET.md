# Hand Gesture Recognition Dataset [中文](./GESTURE_RECOGNITION_DATASET_cn.md)

[![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-blue.svg)](https://www.kaggle.com/datasets/gti-upm/leapgestrecog)

A preprocessed dataset for hand gesture recognition based on the [LeapGestRecog dataset](https://www.kaggle.com/datasets/gti-upm/leapgestrecog) from Kaggle.

## Dataset Structure

- `train.pkl`: Training dataset (12,800 samples)
- `cal.pkl`: Calibration dataset (1,600 samples)
- `test.pkl`: Test dataset (1,600 samples)
- `dataset.ipynb`: Data preprocessing and generation notebook

Each pickle file contains a tuple of (X, y) where:
- X: Image data array of shape (n_samples, 96, 96), normalized to [0,1]
- y: Labels array of shape (n_samples,)

## Gesture Classes

The dataset includes 8 gesture types:
- 0: palm
- 1: l
- 2: fist
- 3: thumb
- 4: index
- 5: ok
- 6: c
- 7: down

## Data Characteristics

- Image size: 96x96 pixels
- Color format: Grayscale
- Value range: 0-1 (float32)
- Total samples: 16,000
- Split ratio: 80% train, 10% calibration, 10% test

## Usage

```python
import pickle

# Load datasets
with open('train.pkl', 'rb') as f:
    X_train, y_train = pickle.load(f)

with open('cal.pkl', 'rb') as f:
    X_cal, y_cal = pickle.load(f)

with open('test.pkl', 'rb') as f:
    X_test, y_test = pickle.load(f)

# Add channel dimension if needed
X_train = X_train[..., np.newaxis]  # Shape becomes (n_samples, 96, 96, 1)
```

## Preprocessing Steps
1. Convert to grayscale
2. Resize to 96x96
3. Normalize pixel values to [0,1]
4. Split into train/cal/test sets