import requests
from bs4 import BeautifulSoup

# 因为没有token，所以无法获取用户主页的详细信息，需要优化
def get_user_info(user_url):
    # 发送HTTP请求，获取用户主页的HTML内容
    response = requests.get(user_url)
    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # 提取用户信息
    name = soup.find('span', class_='ProfileHeader-name').text
    gender = soup.find('span', class_='ProfileHeader-infoValue').text
    bio = soup.find('span', class_='RichText ProfileHeader-headline').text

    return name, gender, bio

user_url = 'https://www.zhihu.com/people/jia-jia-27-58/answers'
name, gender, bio = get_user_info(user_url)
print(f'姓名：{name}')
print(f'性别：{gender}')
print(f'个人简介：{bio}')