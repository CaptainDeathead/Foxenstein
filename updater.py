import requests
import sys
import os

print("Checking for updates...")

# https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/version.txt

with open("version.txt", "r") as f:
    __version__ = f.read()
    f.close()

r = requests.get("https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/version.txt")
version = r.text
print("Current version: " + version)
print("This version: " + __version__)

if version == __version__:
    print("No update available")
    print("Done! Restarting...")

    #subprocess.Popen(["python", "main.py", "--no-update"])
    #sys.exit()

    os.system("python main.py --no-update")
    sys.exit()

print("Update available!")
print("Getting update...")
r = requests.get("https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/changelog.txt")
changelog = r.text
print(f"Changelog:\n{changelog}")
print("Updating...")

changelog = changelog.split("\n")

for line in changelog:
    if line == "":
        continue
    else:
        try:
            print(f"Getting {line}")
            r = requests.get(f"https://raw.githubusercontent.com/CaptainDeathead/Plazma-Engine/main/{line}")
            print(f"Writing to {line}")
            with open(line, "w") as f:
                f.write(r.text)
                f.close()
            print(f"Done writing to {line}")
        except:
            print(f"Error getting {line}")
            print("Continuing anyway...")
            continue

print("Done! Restarting...")

#subprocess.Popen(["python", "main.py", "--no-update"])
#sys.exit()
os.system("python main.py --no-update")
sys.exit()
