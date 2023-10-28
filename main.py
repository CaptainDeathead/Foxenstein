import tkinter as tk
import game as main
import settings
import time
import importlib
import sys
from editor import GameEngine
import os

sys.dont_write_bytecode = True

with open("settings.txt", "r") as f:
    data = f.read().split()
    f.close()

network = ""
width = data[0]
height = data[1]
fps = data[2]
resolutionScale = data[3]
colorScale = data[4]
name = data[5]

root = tk.Tk()
root.title("Plazma 3D Menu")
root.geometry("400x800")

titleLbl = tk.Label(root, text="Plazma 3D Menu", font=("Arial", 20))
titleLbl.pack()

startBtn = tk.Button(root, text="Start Game", command=lambda: startGame())
startBtn.pack()

editorBtn = tk.Button(root, text="Open Editor", command=lambda: startEditor())
editorBtn.pack()

mapLbl = tk.Label(root, text="\nMap", font=("Arial", 15))
mapLbl.pack()
mapEntry = tk.Entry(root)
mapEntry.pack()
mapEntry.insert(0, "perimeterPortals")

nameLbl = tk.Label(root, text="\nName", font=("Arial", 15))
nameLbl.pack()
nameEntry = tk.Entry(root)
nameEntry.pack()
nameEntry.insert(0, name)

serverIpLbl = tk.Label(root, text="\nServer IP", font=("Arial", 15))
serverIpLbl.pack()
serverIpEntry = tk.Entry(root)
serverIpEntry.pack()

screenDimensionsLbl = tk.Label(root, text="\nScreen Dimensions", font=("Arial", 15))
screenDimensionsLbl.pack()

widthLbl = tk.Label(root, text="Width", font=("Arial", 10))
widthLbl.pack()
widthEntry = tk.Entry(root)
widthEntry.pack()
widthEntry.insert(0, str(width))

heightLbl = tk.Label(root, text="Height", font=("Arial", 10))
heightLbl.pack()
heightEntry = tk.Entry(root)
heightEntry.pack()
heightEntry.insert(0, str(height))

fpsLbl = tk.Label(root, text="\nFPS", font=("Arial", 15))
fpsLbl.pack()

fpsEntry = tk.Entry(root)
fpsEntry.pack()
fpsEntry.insert(0, str(fps))

resolutionScaleLbl = tk.Label(root, text="\nResolution Scale", font=("Arial", 15))
resolutionScaleLbl.pack()

resolutionScaleEntry = tk.Entry(root)
resolutionScaleEntry.pack()
resolutionScaleEntry.insert(0, str(resolutionScale))

colorDarkenScaleLbl = tk.Label(root, text="\nColor Darken Scale", font=("Arial", 15))
colorDarkenScaleLbl.pack()

colorDarkenScaleEntry = tk.Entry(root)
colorDarkenScaleEntry.pack()
colorDarkenScaleEntry.insert(0, str(colorScale))

def startGame():
    print("\033[95m" + "Setting Up Variables..." + "\033[0m")
    setName()
    setNetwork()
    setScreenDimensions()
    setFPS()
    setResolutionScale()
    #setFOV()
    setColorDarkenScale()
    print("\033[94m" + "Writing preferences to 'settings.txt'" + "\033[0m")
    with open("settings.txt", "w") as f:
        f.write(str(width) + " " + str(height) + " " + str(fps) + " " + str(resolutionScale) + " " + str(colorScale) + " " + str(name))
        f.close()
    print("Starting Game...")
    # reimport main.py to reset variables
    importlib.reload(main)
    # hide menu
    root.withdraw()
    print(str(mapEntry.get()))
    if settings.NETWORK == "": settings.NETWORK = None
    main.main(settings.WIDTH, settings.HEIGHT, settings.RESOLUTION_SCALE, settings.FOV, settings.COLOR_DARKEN_SCALE, str(mapEntry.get()), settings.FPS, settings.NETWORK, settings.NAME)
    main.pg.quit()
    main.running = False
    # show menu
    print("\033[94m" + "Game Closed Successfully!" + "\033[0m")
    exit()

def startEditor():
    print("\033[95m" + "Withdrawing Menu..." + "\033[0m")
    root.withdraw()
    print("Starting Editor...")
    os.system("python editor.py")
    exit()
    #game = GameEngine()
    time.sleep(0.5)
    print("\033[94m" + "Editor Closed Successfully!" + "\033[0m")
    root.deiconify()

def setName():
    global name
    settings.NAME = str(nameEntry.get())
    name = str(nameEntry.get())
    print("\033[93mName set to " + str(name) + "\033[0m")

def setNetwork():
    global network
    settings.NETWORK = str(serverIpEntry.get())
    network = str(serverIpEntry.get())
    print("\033[93mNetwork set to " + str(settings.NETWORK) + "\033[0m")

def setWidth():
    global width
    settings.WIDTH = int(widthEntry.get())
    width = int(widthEntry.get())
    print("\033[93mWidth set to " + str(settings.WIDTH) + "\033[0m")

def setHeight():
    global height
    settings.HEIGHT = int(heightEntry.get())
    height = int(heightEntry.get())
    print("\033[93mHeight set to " + str(settings.HEIGHT) + "\033[0m")

def setScreenDimensions():
    setWidth()
    setHeight()

def setFPS():
    global fps
    settings.FPS = int(fpsEntry.get())
    fps = int(fpsEntry.get())
    print("\033[93mFPS set to " + str(settings.FPS) + "\033[0m")

def setResolutionScale():
    global resolutionScale
    settings.RESOLUTION_SCALE = int(resolutionScaleEntry.get())
    resolutionScale = int(resolutionScaleEntry.get())
    print("\033[93mResolution Scale set to " + str(settings.RESOLUTION_SCALE) + "\033[0m")

def setFOV():
    settings.FOV = float(fovEntry.get()) * 0.0174533
    print("\033[93mFOV set to " + str(settings.FOV) + "\033[0m")

def setColorDarkenScale():
    global colorScale
    settings.COLOR_DARKEN_SCALE = int(colorDarkenScaleEntry.get())
    colorScale = int(colorDarkenScaleEntry.get())
    print("\033[93mColor Darken Scale set to " + str(settings.COLOR_DARKEN_SCALE) + "\033[0m")

root.mainloop()