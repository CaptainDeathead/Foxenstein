import requests
from bs4 import BeautifulSoup

print("Checking for updates...")
r = requests.get("https://github.com/CaptainDeathead/Plazma-Engine")

soup = BeautifulSoup(r.text, 'html.parser')
version = soup.find("span", {"class": "css-truncate-target"}).text
print(f"Latest version: {version}")