import requests
response = requests.get('https://www.danke.com/room/sz/d%E5%8D%97%E5%B1%B1%E5%8C%BA-b%E5%A4%A7%E6%96%B0.html?page=15', timeout=10)
html = response.content
page_text = response.text
print('您查找的房源已售罄' in page_text)