# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/6


from transformers import CLIPProcessor, CLIPModel, AutoTokenizer, AutoModelForSeq2SeqLM
from PIL import Image
import requests
from config import api_log_file
import logging

# 配置logging模块
logging.basicConfig(
    filename=api_log_file,  # 日志文件名
    filemode='a',             # 追加模式
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    level=logging.INFO        # 日志级别
)


processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")

tokenizer = AutoTokenizer.from_pretrained("t5-small")
text_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

# IMAGE_URL = "/Users/walkerz/AI/single_test/cat1111.jpeg"

IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpHYuBRGaCfY4fKwgc3RIRETcy7Y9Bq0XEpA&s"

# 加载图像
image = Image.open(requests.get(IMAGE_URL, stream=True).raw)

# 处理图像
inputs = processor(images=image, return_tensors="pt")

# # 生成描述
# out = model.generate(**inputs)
# description = processor.decode(out[0], skip_special_tokens=True)
# 获取图像嵌入
outputs = model.get_image_features(**inputs)
description_tensor = outputs.cpu().detach()
# description = outputs.cpu().detach().numpy()

# 生成描述的输入提示
prompt = "Describe this image:"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

# input_ids = description_tensor.unsqueeze(0).long()
generated_ids = text_model.generate(input_ids)
description = tokenizer.decode(generated_ids[0], skip_special_tokens=True)


print(description)











