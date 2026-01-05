# Facial Emotion Recognition using CNN & Transfer Learning (ResNet18)

## Install dependencies



## Project Overview

This project focuses on facial emotion recognition using the FER2013 dataset.

We compare two deep learning approaches:
 
- A custom Convolutional Neural Network (CNN) trained from scratch

- Transfer learning using ResNet18, pretrained on ImageNet

The goal is to analyze performance differences, especially under class imbalance conditions.

## Dataset: FER-2013
The **FER2013** dataset contains grayscale facial images of size 48×48 pixels, categorized into 7 emotion classes:

| Label | Emotion |
| ----------- | ----------- |
| 0 | Angry |
| 1 | Disgust |
| 2 | Fear |
| 3 | Happy |
| 4 | Sad |
| 5 | Surprise |
| 6 | Neutral |

Dataset Split
- Training set: ~28,700 images
- Validation (PublicTest): 3,589 images

Link to the dataset:
- [Image](https://www.kaggle.com/datasets/msambare/fer2013)
- [CSV]([Image](https://www.kaggle.com/datasets/msambare/fer2013))


## Model Architecture
### Custom CNN:
| Block | Layers | Output Shape | Parameters |
|  :----:  |  :----:  |  :----:  |  :----:  |
| Input | - | 1 x 48 x 48​ |  |
| Block 1 | 2 × Conv + BN + ReLU + MaxPool​ | 32 × 24 × 24​ | 9.7K​ |
| Block 2 | 2 × Conv + BN + ReLU + MaxPool​ | 64 x 12 x 12​ | 55.7K |
| Block 3 | 2 × Conv + BN + ReLU + MaxPool​ | 128 x 6 x 6 | 221.7K |
| Block 4 | Conv + BN + ReLU + Dropout​ | 256 x 6 x 6​ | 295.7K​ |
| GAP + FC | Global Avg Pool + Linear​ | 7​ | 1.8K​ |
| Total |  |  | 584.807K​ |

### Transfer Learning – ResNet18
- Pretrained on ImageNet
- Input resized to 112×112 or 224×224
- Grayscale images converted to 3 channels
- Early layers frozen, deeper layers fine-tuned
- Final fully connected layer adapted to 7 emotion classes

## Training Strategy

### Data Augmentation

- Random horizontal flip
- Random rotation
- Color jitter
- Random erasing

### Optimization

- Optimizer: AdamW
- Learning rate scheduling
- Class-weighted cross-entropy loss

### Metrics

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

## Result summary
### Overall metrics
| Model | Accuracy | Macro F1 | Weighted F1 |
| ----------- | :----: | :----: | :----: |
| Group's CNN | 68.24% | 67.23% | 67.93% |
| ResNet18 | 71.41% | 70.96% | 71.11% |

### Per-class accuracy
| Model | Angry | Disgust | Fear | Happy | Sad | Surprise | Neutral |
| ----------- | :----: | :----: | :----: | ----------- | :----: | :----: | :----: |
| Group's CNN | 59.47% | 65.45% | 42.61% | 88.74% | 59.40% | 80.77% | 71.09 | 
| ResNet18 | 55.60% | 72.73% | 51.33% | 91.58% | 62.63% | 82.69% | 73.16% | 
