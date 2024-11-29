import torch
import torch.nn as nn
import cv2
import numpy as np
import argparse

# 手势类别映射
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

class InvertedResidual(nn.Module):
    def __init__(self, in_c, out_c, stride, expand_ratio):
        super().__init__()
        hidden_dim = in_c * expand_ratio
        self.use_res = stride == 1 and in_c == out_c
        
        layers = []
        if expand_ratio != 1:
            layers.extend([
                nn.Conv2d(in_c, hidden_dim, 1, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True)
            ])
        layers.extend([
            nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True),
            nn.Conv2d(hidden_dim, out_c, 1, bias=False),
            nn.BatchNorm2d(out_c)
        ])
        self.conv = nn.Sequential(*layers)

    def forward(self, x):
        if self.use_res:
            return x + self.conv(x)
        return self.conv(x)

class LightGestureNet(nn.Module):
    def __init__(self, num_classes=8):
        super().__init__()
        
        self.first = nn.Sequential(
            nn.Conv2d(1, 16, 3, 2, 1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU6(inplace=True)
        )
        
        self.layers = nn.Sequential(
            InvertedResidual(16, 24, 2, 6),
            InvertedResidual(24, 24, 1, 6),
            InvertedResidual(24, 32, 2, 6),
            InvertedResidual(32, 32, 1, 6)
        )
        
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(32, num_classes)
        )
        
    def forward(self, x):
        x = self.first(x)
        x = self.layers(x)
        x = self.classifier(x)
        return x

def preprocess_image(image_path):
    """图片预处理函数"""
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"无法读取图片: {image_path}")
        
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调整大小到96x96
    resized = cv2.resize(gray, (96, 96))
    # 归一化到0-1
    normalized = resized.astype('float32') / 255.0
    # 添加batch和channel维度
    tensor = torch.FloatTensor(normalized).unsqueeze(0).unsqueeze(0)
    
    return tensor

def main():
    parser = argparse.ArgumentParser(description='手势识别推理脚本')
    parser.add_argument('image_path', type=str, help='输入图片的路径')
    parser.add_argument('--model_path', type=str, default='gesture_model.pth', help='模型路径')
    args = parser.parse_args()

    try:
        # 加载并预处理图片
        input_tensor = preprocess_image(args.image_path)
        
        # 加载模型
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = LightGestureNet().to(device)
        model.load_state_dict(torch.load(args.model_path, map_location=device))
        model.eval()
        
        # 执行推理
        with torch.no_grad():
            input_tensor = input_tensor.to(device)
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            prediction = output.argmax(1).item()
            
        # 输出结果
        print(f"\n预测结果:")
        print(f"类别编号: {prediction}")
        print(f"手势名称: {CLASS_NAMES[prediction]}")
        print("\n各类别置信度:")
        for i, prob in enumerate(probabilities):
            print(f"{CLASS_NAMES[i]}: {prob.item()*100:.2f}%")
            
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == '__main__':
    main()
