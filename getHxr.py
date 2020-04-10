from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

server = Server(os.getcwd() + r'\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy.proxy}')
chrome_options.add_argument('--ignore-certificate-errors')  # 忽略不安全证书提示

driver = webdriver.Chrome(chrome_options=chrome_options)
# 要访问的地址
base_url = "http://www.weather.com.cn/forecast/"
proxy.new_har('http://www.weather.com.cn/forecast/', options={'captureHeaders': True, 'captureContent': True})
driver.get(base_url)
time.sleep(5)
result = proxy.har

for entry in result['log']['entries']:
    url = entry['request']['url']
    print(url)
    if "http://map.weather.com.cn/static_data/101.js" in url:
        response = entry['response']  # 相应对象
        content = response['content']  # 相应内容对象
        text = content['text']  # 响应内容
        print(response)
        break

server.stop()
driver.quit()
