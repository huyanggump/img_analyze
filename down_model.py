# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/8

from config import model_file
from transformers import BlipProcessor, BlipForConditionalGeneration

from huggingface_hub import login

# 登录 Hugging Face 账户
login(token="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", add_to_git_credential=True)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


# 将模型保存到指定目录
save_directory = model_file
model.save_pretrained(save_directory)



