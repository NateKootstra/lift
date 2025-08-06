import threading
import time
import math
import sys
import os
import random
import socket
import requests

import numpy as np
import PIL.Image as Image

import adafruit_blinka_raspberry_pi5_piomatter as piomatter

class Matrix():
    width = None
    height = None
    geometry = None
    canvas = None
    framebuffer = None
    matrix = None
    def __init__(self, chain=1, inverted=False):
        self.width = 64 * chain
        self.height = 64
        self.geometry = piomatter.Geometry(width=self.width, height=self.height, n_addr_lines=5, rotation=piomatter.Orientation.Normal, n_planes=9)
        self.canvas = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        self.framebuffer = np.asarray(self.canvas) + 0
        self.matrix = piomatter.PioMatter(
                                    colorspace=piomatter.Colorspace.RGB888Packed,
                                    pinout=piomatter.Pinout.AdafruitMatrixBonnetBGR, 
                                    framebuffer=self.framebuffer,
                                    geometry=self.geometry
                                    ) if inverted else piomatter.PioMatter(
                                    colorspace=piomatter.Colorspace.RGB888Packed,
                                    pinout=piomatter.Pinout.AdafruitMatrixBonnet,
                                    framebuffer=self.framebuffer,
                                    geometry=self.geometry
                                    )
    def displayImage(self, image):
        self.canvas.paste(image, (0,0))
        self.framebuffer[:] = np.asarray(self.canvas)
        self.matrix.show()
class Game:
    matrix = None
    screen = None
    
    fps = None
    frames = None
    xScale = 64
    yScale = 64
    sprites = None
    class BasicColours:
        Black = [0, 0, 0]
    class Borders:
        Left = 0
        Top = 1
        Right = 2
        Bottom = 3
    class Sprite:
        gameRef = None
        currentSprite = 0
        spriteSheet = None
        currentAnimation = None
        animationFrame = 0
        animationTick = 0
        animations = None
        x = 0
        y = 0
        rotation = None
        layer = None
        visible = True
        storage = None
        def __init__(self, sprite, interval=0, layer=0, rotation=0, visible=True):
            self.layer = layer
            self.rotation = rotation
            self.visible = visible
            self.spriteSheet = []
            self.animations = {}
            self.storage = {}
            sprite = np.asarray(Image.open("sprites/" + sprite + ".png")).tolist()
            sprite = np.asarray(sprite)
            if interval < 1:
                self.spriteSheet.append(sprite)
            else:
                currentSlice = []
                for i,row in enumerate(sprite):
                    currentSlice.append(row)
                    if (i+1) % interval == 0:
                        self.spriteSheet.append(currentSlice)
                        currentSlice = []
        def render(self, screen):
            image = self.getImage().copy()
            if not self.currentAnimation == None:
                self.animationTick += 1
                if self.animationTick >= self.animations[self.currentAnimation][1]:
                    self.animationTick = 0
                    self.animationFrame += 1
                    if self.animationFrame >= len(self.animations[self.currentAnimation][0]):
                        self.animationFrame = 0
            screen = np.asarray(screen, np.uint8)
            xOffset = int(self.x)
            yOffset = len(screen) - len(image) - int(self.y)
            minX = 0
            maxX = image.shape[1]
            minY = 0
            maxY = image.shape[0]
            if xOffset < 0:
                minX = -xOffset
            if yOffset < 0:
                minY = -yOffset
            if xOffset > 64 - maxX:
                maxX = 64 - xOffset
            if yOffset > 64 - maxY:
                maxY = 64 - yOffset
            if abs(minX) < image.shape[1] and abs(minY) < image.shape[0] and maxX > 0 and maxY > 0:
                screen[yOffset + minY:yOffset + maxY, xOffset + minX:xOffset + maxX] = np.where(image[minY:maxY, minX:maxX, 0:3] != [300, 300, 300], image[minY:maxY, minX:maxX, 0:3], screen[yOffset + minY:yOffset + maxY, xOffset + minX:xOffset + maxX])
            return screen
        def setSprite(self, sprite):
            self.currentSprite = sprite
            return self
        def moveTo(self, x, y):
            self.x = x
            self.y = y
            return self
        def move(self, x, y):
            self.x += x
            self.y += y
            return self
        def rotateTo(self, rotation):
            self.rotation = rotation
            return self
        def rotate(self, amount):
            self.rotation += amount
            return self
        def clamp(self):
            old = [self.x, self.y]
            self.x = sorted([0, self.x, 64 - len(self.getImage())])[1]
            self.y = sorted([0, self.y, 64 - len(self.getImage()[0])])[1]
            return not (old == [self.x, self.y])
        def visible(self, visibility):
            self.visible = visibility
            return self
        def storeData(self, name, data):
            self.storage[name] = data
            return self
        def getData(self, name):
            return self.storage[name]
        def getRectCollisions(self, onlyLayer=True):
            collisions = []
            for sprite in self.gameRef.sprites:
                if self.layer == sprite.layer or not onlyLayer:
                    if not (self == sprite):
                        if self.x <= sprite.x and sprite.x <= self.x + len(self.getImage()[0]) - 1 or sprite.x <= self.x and self.x <= sprite.x + len(sprite.getImage()[0]) - 1:
                            if self.y <= sprite.y and sprite.y <= self.y + len(self.getImage()) - 1 or sprite.y <= self.y and self.y <= sprite.y + len(sprite.getImage()) - 1:
                                collisions.append(sprite)
            return collisions
        def addAnimation(self, name, animation, interval, speed):
            animation = np.asarray(Image.open("animations/" + animation + ".png"), np.uint8).tolist()
            for i, line in enumerate(animation):
                for i2, pixel in enumerate(line):
                    if len(pixel) > 3:
                        if pixel[3] == 0:
                            animation[i][i2] = [300, 300, 300]
                        else:
                            animation[i][i2] = [pixel[0], pixel[1], pixel[2]]
            animation = np.asarray(animation)
            animationSplit = []
            currentSlice = []
            for i,row in enumerate(animation):
                currentSlice.append(row)
                if (i+1) % interval == 0:
                    animationSplit.append(currentSlice)
                    currentSlice = []
            self.animations[name] = [animationSplit, speed]
            return self
        def startAnimation(self, name):
            self.currentAnimation = name
            self.animationTick = 0
            return self
        def stopAnimation(self):
            self.currentAnimation = None
            return self
        def getImage(self):
            image = self.spriteSheet[self.currentSprite].copy()
            if not self.currentAnimation == None:
                image = self.animations[self.currentAnimation][0][self.animationFrame]
            for i in range(4 - self.rotation % 4):
                image = np.rot90(image)
            return image
        def touchingBorder(self, border):
            if border == Game.Borders.Left:
                if self.x <= 0:
                    return True
                return False
            if border == Game.Borders.Top:
                if self.y >= 64 - len(self.getImage()[0]):
                    return True
                return False
            if border == Game.Borders.Right:
                if self.x >= 64 - len(self.getImage()):
                    return True
                return False
            if border == Game.Borders.Bottom:
                if self.y <= 0:
                    return True
                return False
    def __init__(self, fps=24, chain=1, inverted=False):
        self.sprites = []
        self.frames = []
        
        self.fps = fps
        self.xScale = 64 * chain
        
        self.matrix = Matrix(chain, inverted)
        self.screen = self.blankScreen()
    def blankScreen(self):
        screen = []
        for i in range(self.yScale):
            row = []
            for i2 in range(self.xScale):
                row.append(self.BasicColours.Black)
            screen.append(row)
        self.screen = screen
    def addSprite(self, sprite, interval=0, layer=0, rotation=0, visible=True):
        self.sprites.append(self.Sprite(sprite, interval=interval, layer=layer, rotation=rotation, visible=visible))
        self.sprites[-1].gameRef = self
        return self.sprites[-1]
    def render(self):
        self.blankScreen()
        sprites = sorted(self.sprites, key = lambda x: x.layer)
        for sprite in sprites:
            if sprite.visible:
                self.screen = sprite.render(self.screen)
        self.matrix.displayImage(Image.fromarray(np.asarray(self.screen)))
    def pause(self):
        fps = 1./self.fps
        self.frames.append(time.perf_counter())
        
        debt = 0
        for i in range(len(self.frames)):
            if not i == 0:
                debt += self.frames[i] - self.frames[i - 1]
        debt -= fps * len(self.frames)
        debt *= -1
        if len(self.frames) > 60:
            self.frames.pop(0)
        time.sleep(debt if debt > 0 else 0)
        try:
            currentFPS = self.fps / ((self.frames[-1] - self.frames[0]) / len(self.frames) * self.fps)
        except:
            currentFPS = 60
        return currentFPS
    def kill(self):
        del self.matrix
        del self


title = "LIFT WEBSITE"
localhost = "127.0.0.1"
privateIP = "0.0.0.0"
publicIP = "0.0.0.0"
game = Game(fps=1, inverted=True)

privateIPDisplay = []
numbers = "0123456789."

while True:    
    game.sprites = []
    game.addSprite("title").moveTo(0, 49)


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        privateIP = s.getsockname()[0]
        s.close()
    except:
        pass

    try:
        publicIP = requests.get('https://api.ipify.org').content.decode('utf8')
    except:
        pass
    
    
    i = 9
    for char in localhost:
        game.addSprite("numbers", interval=5, layer=0).moveTo(i, 40).setSprite(numbers.index(char))
        i += 2 if char == "." else 4
    try:
        response = requests.get("http://" + localhost + "/status", timeout=3)
        live = True
    except:
        live = False
    game.addSprite("status", interval=5, layer=0).moveTo(2, 40).setSprite(1 if live else 0)

    i = 9
    for char in privateIP:
        game.addSprite("numbers", interval=5, layer=0).moveTo(i, 33).setSprite(numbers.index(char))
        i += 2 if char == "." else 4
        
    try:
        response = requests.get("http://" + privateIP + "/status", timeout=3)
        live = True
    except:
        live = False
    game.addSprite("status", interval=5, layer=0).moveTo(2, 33).setSprite(0 if privateIP == "0.0.0.0" else 1 if live else 0)

    i = 9
    for char in publicIP:
        game.addSprite("numbers", interval=5, layer=0).moveTo(i, 26).setSprite(numbers.index(char))
        i += 2 if char == "." else 4
        
    try:
        response = requests.get("http://" + publicIP + "/status", timeout=3)
        live = True
    except:
        live = False
    game.addSprite("status", interval=5, layer=0).moveTo(2, 26).setSprite(0 if publicIP == "0.0.0.0" else 1 if live else 0)
    
    
    game.render()
    game.pause()