# coding: utf-8
# @Author: WalkerZ
# @Time: 2024/10/6

from config import api_log_file
import logging
from flask import Flask, request, render_template, jsonify
from PIL import Image
from model import describe_image

# 配置logging模块
logging.basicConfig(
    filename=api_log_file,  # 日志文件名
    filemode='a',             # 追加模式
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    level=logging.INFO        # 日志级别
)

app = Flask(__name__)

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# 检查文件格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # if 'file' not in request.files:
    #     return "No file uploaded.", 400
    #
    # file = request.files['file']
    # # image = Image.open(file.stream)
    # raw_image = Image.open(file.stream).convert('RGB')
    # detail = describe_image(raw_image)
    # return detail
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        raw_image = Image.open(file.stream).convert('RGB')
        detail = describe_image(raw_image)

        return jsonify({'success': True, 'message': f"分析结果为：{detail}"})

    return jsonify({'success': False, 'message': 'File type not allowed'})





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)