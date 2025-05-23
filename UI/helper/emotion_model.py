import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# 标签列表
LABELS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

# 获取当前脚本文件的目录，并构建到模型文件的相对路径
model_path = os.path.join(os.path.dirname(__file__), "../../ml_model/cnn/cnn_model.pth")

# 加载模型并设置设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, len(LABELS))
model.load_state_dict(torch.load(model_path, map_location=device))
model = model.to(device)
model.eval()

# 预处理图像的转换
transform = transforms.Compose([
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

def predict_emotion(image):
    """对PIL图像进行情绪预测"""
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        return LABELS[predicted.item()]
