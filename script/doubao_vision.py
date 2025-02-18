import base64
import os
# 通过 pip install volcengine-python-sdk[ark] 安装方舟SDK
from volcenginesdkarkruntime import Ark

# 初始化一个Client对象，从环境变量中获取API Key
client = Ark(
    api_key="f6a53c6e-b98d-493b-9989-badbaf1b152e",
    )

# 定义方法将指定路径图片转为Base64编码
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# 需要传给大模型的图片
image_path = r"D:\Container\Download\Google\（根据2022年版课程标准修订）义务教育教科书 英语 三年级 上册裁剪后\page_93.png"

# 将图片转为Base64编码
base64_image = encode_image(image_path)

response = client.chat.completions.create(
  # 替换为您的
  model="ep-20250212173055-nfsh7",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": '解析单词, 输出为json, 输出示例为:[{"word": "air", "pronunciation": "/eə(r)/", "translation": "空气"}]',
        },
        {
          "type": "image_url",
          "image_url": {
          # 需要注意：传入Base64编码前需要增加前缀 data:image/{图片格式};base64,{Base64编码}：
          # PNG图片："url":  f"data:image/png;base64,{base64_image}"
          # JEPG图片："url":  f"data:image/jpeg;base64,{base64_image}"
          # WEBP图片："url":  f"data:image/webp;base64,{base64_image}"
            "url":  f"data:image/png;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0].message.content)