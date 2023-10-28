import requests
from bs4 import BeautifulSoup

print("Checking for updates...")

# https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/version.txt

with open("version.txt", "r") as f:
    __version__ = f.read()
    f.close()

r = requests.get("https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/version.txt")
version = r.text
print("Current version: " + version)
print("This version: " + __version__)

if version != __version__:
    print("Update available!")
    print("Getting update...")
    r = requests.get("https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/changelog.txt")
    changelog = r.text
    print(f"Changelog:\n{changelog}")