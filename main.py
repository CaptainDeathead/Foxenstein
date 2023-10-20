import tkinter as tk
import game as main
import settings
import time

with open("settings.txt", "r") as f:
    data = f.read().split()
    f.close()

width = data[0]
height = data[1]
resolutionScale = data[2]
colorScale = data[3]

root = tk.Tk()
root.title("Plazma 3D Menu")
root.geometry("400x600")

titleLbl = tk.Label(root, text="Plazma 3D Menu", font=("Arial", 20))
titleLbl.pack()

startBtn = tk.Button(root, text="Start Game", command=lambda: startGame())
startBtn.pack()

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
    setScreenDimensions()
    setResolutionScale()
    #setFOV()
    setColorDarkenScale()
    print("\033[94m" + "Writing preferences to 'settings.txt'" + "\033[0m")
    with open("settings.txt", "w") as f:
        f.write(str(width) + " " + str(height) + " " + str(resolutionScale) + " " + str(colorScale))
        f.close()
    print("Starting Game...")
    # hide menu
    root.withdraw()
    try:
        main.main(settings.WIDTH, settings.HEIGHT, settings.RESOLUTION_SCALE, settings.FOV, settings.COLOR_DARKEN_SCALE)
    except Exception as e:
        print("\033[91m" + "Error: " + str(e) + "\033[0m")
        main.pg.quit()
        main.running = False
    # show menu
    print("\033[94m" + "Game Closed Successfully!" + "\033[0m")
    time.sleep(0.5)
    root.deiconify()

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