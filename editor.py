import pygame as pg
import os
from os.path import isfile, join
import tkinter as tk
from tkinter import simpledialog, messagebox
from portal import Portal
from random import randint
import sys

sys.dont_write_bytecode = True

class Square(pg.Rect):
    def __init__(self, x, y, width, height, texture=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture = texture
        self.texturePath = "textures/1.png"

class TreeButton(pg.Rect):
    def __init__(self, name, obj, position, size):
        self.name = name
        self.object = obj
        self.selected = False
        self.color = (255, 0, 0)
        self.position = position
        self.size = size

        self.x = self.position[0]
        self.y = self.position[1]

        self.font = pg.font.SysFont("Arial", 8)

    def select(self):
        self.selected = not self.selected
        self.color = (150, 150, 150)

    def onClick(self):
        self.select()
        print("Selected: " + str(self.name))
        root = tk.Tk()
        root.title("Object Settings")
        root.geometry("400x600")

        titleLbl = tk.Label(root, text="Object Settings", font=("Arial", 20))
        titleLbl.pack()

        xLbl = tk.Label(root, text="X", font=("Arial", 10))
        xLbl.pack()
        xEntry = tk.Entry(root)
        xEntry.insert(0, str(self.object.x - 300))
        xEntry.pack()

        yLbl = tk.Label(root, text="Y", font=("Arial", 10))
        yLbl.pack()
        yEntry = tk.Entry(root)
        yEntry.insert(0, str(self.object.y))
        yEntry.pack()

        widthLbl = tk.Label(root, text="Width", font=("Arial", 10))
        widthLbl.pack()
        widthEntry = tk.Entry(root)
        widthEntry.insert(0, str(self.object.width))
        widthEntry.pack()

        heightLbl = tk.Label(root, text="Height", font=("Arial", 10))
        heightLbl.pack()
        heightEntry = tk.Entry(root)
        heightEntry.insert(0, str(self.object.height))
        heightEntry.pack()

        try:
            textureLbl = tk.Label(root, text="Texture", font=("Arial", 10))
            textureLbl.pack()
            textureEntry = tk.Entry(root)
            textureEntry.insert(0, str(self.object.texture))
            textureEntry.pack()
        except AttributeError:
            textureLbl = tk.Label(root, text="Texture (N/A): Portal", font=("Arial", 10), foreground="grey")
            textureLbl.pack()
            textureEntry = tk.Entry(root, state="disabled")
            textureEntry.insert(0, "N/A")
            textureEntry.pack()

        saveBtn = tk.Button(root, text="Save", command=lambda: self.saveSettings(xEntry.get(), yEntry.get(), widthEntry.get(), heightEntry.get(), textureEntry.get(), root))
        saveBtn.pack()

        root.mainloop()

    def saveSettings(self, x, y, width, height, texture, root):
        self.object.x = int(x) + 300
        self.object.y = int(y)
        self.object.width = int(width)
        self.object.height = int(height)

        if texture != "N/A" and texture != "":
            self.object.texture = int(texture)
            self.object.texturePath = "textures/" + str(texture) + ".png"

        print("Saved: " + str(self.name))
        root.destroy()
        del root

class Window:
    def __init__(self, title):
        self.screen = pg.display.set_mode((1500, 800), pg.DOUBLEBUF, pg.OPENGL)
        pg.display.set_caption("Game Engine: 0 FPS")
        pg.font.init()

        self.BUTTON_SIZE = 145, 13

        self.gameTitle = title

        self.clock = pg.time.Clock()
        self.running = True
        self.fps = 165

        self.objects = []
        self.objectColors = []
        self.treeButtons = []

        self.currentTreePosition = 0

        self.objectsTree = pg.Rect(0, 0, 300, 900)
        self.objectsTreeColor = (30, 30, 30)
        self.objectsTreeBorder = 2
        self.objectsTreeBorderColor = (255, 255, 255)

        self.addObjButton = pg.Rect(0, 700, 300, 100)
        self.addObjButtonColor = (0, 200, 0)
        self.addObjButtonBorder = 2
        self.addObjButtonBorderColor = (255, 0, 0)
        self.addObjButtonText = "Add Object"
        self.addObjButtonFont = pg.font.SysFont("Arial", 50)

        self.viewport = pg.Rect(300, 0, 1200, 800)
        self.viewportColor = (0, 0, 0)
        self.viewportBorder = 2
        self.viewportBorderColor = (255, 255, 255)

        self.portals = []
        self.portalLocations = []

        self.chosenNums = []

        #self.texture1 = pg.image.load("textures/1.png").convert_alpha()
        #self.texture2 = pg.image.load("textures/2.png").convert_alpha()
        #self.texture3 = pg.image.load("textures/3.png").convert_alpha()

        self.textures = {}
        self.onlyfiles = [f for f in os.listdir("textures") if isfile(join("textures", f))]
        self.texturesLen = len(self.onlyfiles)

        for i in range(len(self.onlyfiles)):
            self.textures[i] = pg.image.load("textures/" + self.onlyfiles[i]).convert_alpha()

        self.treeX = 0
        self.currentTexture = 1

    def run(self):
        while self.running:
            self.clock.tick(self.fps)

            self.events()
            if not self.running:
                break
            self.update()
            self.draw()

    def showHelp(self):
        root = tk.Tk()

        root.title("Plazma Engine: Help")
        root.geometry("500x600")

        titleLbl = tk.Label(root, text="Help", font=("Arial", 20))
        titleLbl.pack()

        brandLbl = tk.Label(root, text="Plazma Game Engine\n", font=("Arial", 10) , foreground="grey")
        brandLbl.pack()

        actions = [
            "   'L-Click': Select UI elements and add objects",
            "   'Shift + L-Click': Place an object with advanced config (options menu)",
            "   'R-Click': Remove an object or portal",
            "   'Shift + R-Click': Edit an object or portal with advanced config (options menu)",
            "   'Alt + L-Click': Place a portal",
            "   'Shift + Alt + L-Click': Place a portal with advanced config (options menu)",
            "   'H': Bring up this menu",
            "   'L': Load a map",
            "   '`': Pack your map",
            "   'Esc': Exit"
        ]

        for action in actions:
            actionLbl = tk.Label(root, text=action, font=("Arial", 10))
            actionLbl.pack(anchor="w")

        root.mainloop()

    def packGame(self, debug=False):
        root = tk.Tk()
        root.withdraw()
        fileName = messagebox.askquestion("Save", "Would you like to save your map?", icon="question")
        if fileName == "yes":
            fileName = simpledialog.askstring("Save", "What name would you like to save your game map as?")
            if fileName == None:
                return
            fileName = "maps/" + fileName + ".py"
        else:
            return
        with open(fileName, "w") as f:
            f.write("# Generated by Plazma Game Engine! We hope you've enjoyed using our engine!\n# Email: 'unstableplazma@gmail.com'\n\n")
            f.write("import pygame as pg\n\n")

            objects = []
            objectTypes = []
            portals = []
            portalLocations = []
            for obj in self.objects:
                objects.append(pg.Rect(obj.x-300, obj.y, obj.width, obj.height))
                objectTypes.append(obj.texture - 1)

            for i, portal in enumerate(self.portals):
                portals.append(pg.Rect(portal.x - 300, portal.y, portal.width, portal.height))
                portalLocations.append(self.portalLocations[i])

            objectsString = str(objects)
            objectsString = objectsString.replace("<", "")
            objectsString = objectsString.replace(">", "")
            objectsString = objectsString.replace("rect", "pg.Rect")

            portalsString = str(portals)
            portalsString = portalsString.replace("<", "")
            portalsString = portalsString.replace(">", "")
            portalsString = portalsString.replace("rect", "pg.Rect")

            f.write("objects = " + objectsString + "\n")
            f.write("objectTypes = " + str(objectTypes) + "\n\n")

            f.write("portals = " + portalsString + "\n")
            f.write("portalLocations = " + str(portalLocations) + "\n\n")

            f.write("def loadMap():\n")
            f.write("    return objects, objectTypes, portals, portalLocations\n")

            f.write("# Thank you using our engine! We hope you've enjoyed using it!\n# - UnstablePlazma\n\n")

        f.close()

        messagebox.showinfo("Saved", f"Your map has been saved! Location: {os.getcwd()}/{fileName}", icon="info")

        root.destroy()
        del root

    def loadMap(self):
        root = tk.Tk()
        root.withdraw()
        filePath = simpledialog.askstring("Load", "What map would you like to load?")
        if filePath == None:
            return
        filePathAll = "maps/" + filePath + ".py"
        try:
            with open(filePathAll, "r") as f:
                data = f.read()
                f.close()
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found! Location: {os.getcwd()}/{filePath}", icon="error")
            return

        self.objects = []
        self.objectColors = []
        self.treeButtons = []
        self.portals = []
        self.portalLocations = []

        self.currentTreePosition = 0
        num = randint(0, 100000)
        while num in self.chosenNums:
            num = randint(0, 100000)

        with open(f"temp{num}.py", "w") as f:
            f.write(data)
            f.close()

        temp = __import__(f"temp{num}")

        self.treeX = 0
        self.currentTexture = 1
        
        objects, objectTypes, portals, portalLocations = temp.loadMap()

        for i, portal in enumerate(portals):
            self.portals.append(Portal(portal.x + 300, portal.y, portal.width, portal.height))
            self.portalLocations.append(portalLocations[i])
            if self.currentTreePosition == 690 and self.treeX != 150:
                self.treeX = 150
                self.currentTreePosition = 0

            self.treeButtons.append(TreeButton("Portal", self.portals[-1], (self.treeX, self.currentTreePosition), self.BUTTON_SIZE))
            self.currentTreePosition += 15

        for i, obj in enumerate(objects):
            self.objects.append(Square(obj.x + 300, obj.y, obj.width, obj.height, objectTypes[i]+1))
            self.objectColors.append((255, 255, 255))
            if self.currentTreePosition == 690 and self.treeX != 150:
                self.treeX = 150
                self.currentTreePosition = 0

            self.treeButtons.append(TreeButton("Square", self.objects[-1], (self.treeX, self.currentTreePosition), self.BUTTON_SIZE))
            self.currentTreePosition += 15

        os.remove(f"temp{num}.py")

        messagebox.showinfo("Loaded", f"Loaded: {os.getcwd()}/{filePath}", icon="info")

        root.destroy()
        del root

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            keys = pg.key.get_pressed()

            if keys[pg.K_ESCAPE]:
                self.running = False
                pg.quit()
                break

            elif keys[pg.K_BACKQUOTE]:
                self.packGame(debug=True)

            elif keys[pg.K_l]:
                self.loadMap()

            elif keys[pg.K_h]:
                self.showHelp()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if pg.mouse.get_pos()[0] < 300 and pg.mouse.get_pos()[1] > 700:
                    objAlreadyExists = False
                    for obj in self.objects + self.portals:
                        if obj.x == 300 and obj.y == 0:
                            objAlreadyExists = True
                            break

                    if not objAlreadyExists:
                        newObj = Square(300, 0, 100, 100)

                        self.objects.append(newObj)
                        self.objectColors.append((255, 255, 255))
                        if self.currentTreePosition == 690 and self.treeX != 150:
                            self.treeX = 150
                            self.currentTreePosition = 0

                        self.treeButtons.append(TreeButton("Square", newObj, (self.treeX, self.currentTreePosition), self.BUTTON_SIZE))
                        self.currentTreePosition += 15
                
                elif pg.mouse.get_pos()[0] > 300:
                    gx = int((pg.mouse.get_pos()[0] - 300) / 100) * 100
                    gy = int(pg.mouse.get_pos()[1] / 100) * 100

                    objAlreadyExists = False
                    for obj in self.objects + self.portals:
                        if obj.x == gx + 300 and obj.y == gy:
                            objAlreadyExists = True
                            break

                    if not objAlreadyExists:
                        altPressed = False
                        if keys[pg.K_LALT]:
                            altPressed = True
                            newObj = Portal(gx+300, gy, 100, 100)
                        else: newObj = Square(gx+300, gy, 100, 100, self.currentTexture)

                        if self.currentTreePosition == 690 and self.treeX != 150:
                            self.treeX = 150
                            self.currentTreePosition = 0

                        if altPressed:
                            self.treeButtons.append(TreeButton("Portal", newObj, (0, self.currentTreePosition), self.BUTTON_SIZE))
                            self.portals.append(newObj)
                            root = tk.Tk()
                            root.withdraw()
                            self.portalLocations.append(simpledialog.askstring("Load", "What map would you like to assign?"))
                            root.destroy()
                            del root
                        else:
                            self.treeButtons.append(TreeButton("Square", newObj, (0, self.currentTreePosition), self.BUTTON_SIZE))
                            self.objects.append(newObj)
                            self.objectColors.append((255, 255, 255))

                        self.currentTreePosition += 15

                        if keys[pg.K_LSHIFT]: self.treeButtons[-1].onClick()

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                if pg.mouse.get_pos()[0] > 300:
                    gx = int((pg.mouse.get_pos()[0] - 300) / 100) * 100
                    gy = int(pg.mouse.get_pos()[1] / 100) * 100

                    for obj in self.objects:
                        if gx + 300 == obj.x and gy == obj.y:
                            if keys[pg.K_LSHIFT]:
                                self.treeButtons[self.objects.index(obj)].onClick()
                                break
                            self.treeButtons.remove(self.treeButtons[self.objects.index(obj)])
                            self.objectColors.remove(self.objectColors[self.objects.index(obj)])
                            self.objects.remove(obj)
                            break

                    for portal in self.portals:
                        if gx + 300 == portal.x and gy == portal.y:
                            if keys[pg.K_LSHIFT]:
                                self.treeButtons[self.portals.index(portal)].onClick()
                                break
                            self.treeButtons.remove(self.treeButtons[self.portals.index(portal)])
                            self.portalLocations.remove(self.portalLocations[self.portals.index(portal)])
                            self.portals.remove(portal)
                            break

            # scroll change texture
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
                if self.currentTexture == self.texturesLen - 1:
                    self.currentTexture = 1
                else:
                    self.currentTexture += 1

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
                if self.currentTexture == 1:
                    self.currentTexture = self.texturesLen - 1
                else:
                    self.currentTexture -= 1

                for button in self.treeButtons:
                    if pg.mouse.get_pos()[0] > button.position[0] and pg.mouse.get_pos()[0] < button.position[0] + button.size[0] and pg.mouse.get_pos()[1] > button.position[1] and pg.mouse.get_pos()[1] < button.position[1] + button.size[1]:
                        button.onClick()

            if event.type == pg.MOUSEBUTTONUP:
                for button in self.treeButtons:
                    button.select()
                    button.color = (255, 0, 0)

    def update(self):
        pg.display.set_caption(f"Game Engine: {self.clock.get_fps():.2f} FPS    'H' For Help Menu    Objects: {len(self.objects)}    Portals: {len(self.portals)}    Current Texture: {self.currentTexture} (textures/{self.currentTexture}.png)")

    def drawViewportGrid(self):
        for y in range(0, 800, 100):
            pg.draw.line(self.screen, (100, 100, 100), (300, y), (1500, y))
            
        for x in range(300, 1500, 100):
            pg.draw.line(self.screen, (100, 100, 100), (x, 0), (x, 800))

    def draw(self):
        self.screen.fill((0, 0, 30))
        pg.draw.rect(self.screen, self.objectsTreeColor, self.objectsTree)
        pg.draw.rect(self.screen, self.objectsTreeBorderColor, self.objectsTree, self.objectsTreeBorder)
        pg.draw.rect(self.screen, self.viewportColor, self.viewport)
        pg.draw.rect(self.screen, self.viewportBorderColor, self.viewport, self.viewportBorder)
        pg.draw.rect(self.screen, self.addObjButtonColor, self.addObjButton)

        for button in self.treeButtons:
            pg.draw.rect(self.screen, button.color, button)
            self.screen.blit(button.font.render(button.name, True, (255, 255, 255)), (button.x + 20, button.y + 2))

        self.screen.blit(self.addObjButtonFont.render(self.addObjButtonText, True, (255, 255, 255)), (self.addObjButton.x + 20, self.addObjButton.y + 20))

        self.drawViewportGrid()

        for obj in self.objects:
            #pg.draw.rect(self.screen, self.objectColors[self.objects.index(obj)], obj)
            #if obj.texture == 1:
            #    objTexture = pg.transform.scale(self.texture1, (obj.width, obj.height))
            #elif obj.texture == 2:
            #    objTexture = pg.transform.scale(self.texture2, (obj.width, obj.height))
            #elif obj.texture == 3:
            #    objTexture = pg.transform.scale(self.texture3, (obj.width, obj.height))

            #self.screen.blit(objTexture, (obj.x, obj.y))

            self.screen.blit(pg.transform.scale(self.textures[obj.texture], (obj.width, obj.height)), (obj.x, obj.y))

        for portal in self.portals:
            self.screen.blit(pg.transform.scale(portal.texturePath, (portal.width, portal.height)), (portal.x, portal.y))

        pg.display.flip()

class GameEngine:
    def __init__(self):
        self.running = False
        self.title = "My Game"

        self.window = Window(self.title)
        self.window.run()

if __name__ == "__main__":
    game = GameEngine()
    pg.quit()