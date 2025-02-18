# 升级方舟 SDK 到最新版本 pip install -U 'volcengine-python-sdk[ark]'
from volcenginesdkarkruntime import Ark

client = Ark(
    # 从环境变量中读取您的方舟API Key
    api_key="f6a53c6e-b98d-493b-9989-badbaf1b152e",
    # 深度推理模型耗费时间会较长，请您设置较大的超时时间，避免超时，推荐30分钟以上
    timeout=1800,
    )

response = client.chat.completions.create(
    # 替换 <YOUR_ENDPOINT_ID> 为您的方舟推理接入点 ID
    model="ep-20250208115257-gmc4g",
    messages=[
        {"role": "user", "content": "根据提供以逗号分隔的单词, 给出常用定义, 常用例句, 输入示例: 'climbers,thought'. 输出示例: [{'climbers': {'definition': 'A person who climbs (especially mountains) or an animal that climbs, a climbing plant', 'example':'Climbers and hill walkers'}}, {'thought': {...}] 原始单词为: weight,volleyball"}
    ]
)
# 当触发深度推理时，打印思维链内容
# if hasattr(response.choices[0].message, 'reasoning_content'):
#     print(response.choices[0].message.reasoning_content)
print(response.choices[0].message.content)