import requests
import fake_useragent, requests
from bs4 import BeautifulSoup


__user = fake_useragent.UserAgent().random
__headers = {"user-agent": __user}
req= requests.get('https://rur.hitmotop.com/get/music/20170831/Linkin_Park_-_What_Ive_Done_47894351.mp3',headers=__headers,allow_redirects=True)
print(req.url)