# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/6

from config import api_log_file
import logging
from flask import Flask, request, render_template
from transformers import CLIPProcessor, CLIPModel, AutoTokenizer, AutoModelForSeq2SeqLM
from PIL import Image
import torch


# 配置logging模块
logging.basicConfig(
    filename=api_log_file,  # 日志文件名
    filemode='a',             # 追加模式
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    level=logging.INFO        # 日志级别
)


app = Flask(__name__)

# 加载模型和处理器
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")

# 加载文本生成模型
tokenizer = AutoTokenizer.from_pretrained("t5-small")
text_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded.", 400

    file = request.files['file']
    image = Image.open(file.stream)

    # 处理图像
    inputs = processor(images=image, return_tensors="pt")

    # 获取图像特征
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    # 假设我们可以用图像特征生成描述性文本
    # 将图像特征转化为适合文本生成的输入
    # 使用一个简单的文本提示加图像特征（例如，获取最大值并拼接）
    image_embedding = image_features.cpu().numpy().flatten()
    image_description = "Image feature vector: " + str(image_embedding)  # 将图像特征转为字符串

    # 更新提示文本
    prompt = f"Describe the content of this image based on the following features: {image_description}"
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    # 使用 T5 生成描述
    generated_ids = text_model.generate(input_ids)
    description = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    return {"description": description}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)



