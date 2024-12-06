import requests

url = 'https://api.bigread.ai/client/v2/api/topic/fun'
params = {'num': '6'}

headers = {
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.1.1237860590.1733133915; _ga_N94S9M1QW7=GS1.1.1733144334.2.0.1733144334.0.0.0; token=bf34ec0143b6478990009d39d9df3de6',
    'Origin': 'https://app.bigread.ai',
    'Referer': 'https://app.bigread.ai/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'accept': '*/*',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'authorization': 'bf34ec0143b6478990009d39d9df3de6',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

response = requests.get(url, params=params, headers=headers)

print(f"Status Code: {response.status_code}")
print("Response Content:")
print(response.text)