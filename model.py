# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/7

from config import model_file
from config import api_log_file
from transformers import BlipProcessor, BlipForConditionalGeneration
import logging
from youdao_translator import youda_trans

# 配置logging模块
logging.basicConfig(
    filename=api_log_file,  # 日志文件名
    filemode='a',             # 追加模式
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    level=logging.INFO        # 日志级别
)

processor = BlipProcessor.from_pretrained(model_file)
# model = BlipForConditionalGeneration.from_pretrained(model_file)
model = BlipForConditionalGeneration.from_pretrained(model_file).to("cuda")

# img_url = 'https://www.greenpeace.org/static/planet4-taiwan-stateless/2021/04/17b12b72-shutterstock_77217466-scaled-e1622618684654.jpg'
# raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

def describe_image(raw_image):
    # conditional image captioning
    # text = "a photography of"
    # inputs = processor(raw_image, text, return_tensors="pt")

    # out = model.generate(**inputs)
    # conditional_detail = processor.decode(out[0], skip_special_tokens=True)
    # # 使用googletrans库进行翻译
    # translator = GoogleTranslator(source='auto', target='zh-CN')
    # # conditional_detail = translator.translate(conditional_detail, dest='zh-cn')
    # conditional_detail = translator.translate(conditional_detail)
    # logging.info(conditional_detail)

    # unconditional image captioning
    # inputs = processor(raw_image, return_tensors="pt")
    inputs = processor(raw_image, return_tensors="pt").to("cuda")

    out = model.generate(**inputs)
    unconditional_detail = processor.decode(out[0], skip_special_tokens=True)
    # 使用googletrans库进行翻译
    # translator2 = GoogleTranslator(source='auto', target='zh-CN')
    # unconditional_detail = translator2.translate(unconditional_detail, dest='zh-cn')
    # unconditional_detail = translator2.translate(unconditional_detail)
    logging.info(unconditional_detail)
    unconditional_detail = youda_trans(unconditional_detail)
    logging.info(unconditional_detail)
    return unconditional_detail

