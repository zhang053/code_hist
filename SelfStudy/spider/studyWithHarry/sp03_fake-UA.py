import requests
from fake_useragent import UserAgent
import random

url = "https://www.google.com/"

ua = UserAgent()
ua_output = ua.random
print(ua_output)
