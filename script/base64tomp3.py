import json
import base64

def save_mp3_from_json(json_file_path, output_mp3_path):
    # 读取 JSON 文件
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # 获取 base64 编码的数据
    base64_data = data['data']  # 假设 JSON 中的字段名为 'data'

    # 解码 base64 数据
    mp3_data = base64.b64decode(base64_data)

    # 将解码后的数据写入 MP3 文件
    with open(output_mp3_path, 'wb') as mp3_file:
        mp3_file.write(mp3_data)

# 使用示例
try:
    json_file_path = r"C:\Users\ZJ\Desktop\resp.json"
    output_mp3_path = r"C:\Users\ZJ\Desktop\output.mp3"
    save_mp3_from_json(json_file_path, output_mp3_path)
    print(f"MP3 文件已保存到: {output_mp3_path}")
except Exception as e:
    print(f"发生错误: {str(e)}")