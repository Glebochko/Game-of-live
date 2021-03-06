from graphics import *
from random import randint, randrange
import time



class cellObj:
    def __init__(self, x, y, celltype, bgColor):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.type = celltype
        self.oldtype = celltype
        self.setColor(bgColor)

        p = Point(0, 0)
        self.ghost = Polygon([p, p, p, p])

    
    def setColor(self, bgColor):
        if self.type == 0 :     # free cell
            self.color = bgColor
        elif self.type == 1 :   # fish
            self.color = 'blue'
        elif self.type == 2 :   # rock
            self.color = 'gray'
        elif self.type == 3 :   # shrimp
            self.color = 'pink'



class GameOfLive:
    def __init__(self):
        self.cellsize = 10
        self.iteration = 0
        self.status = 0   # 0 - expectations; 1 - work; 2 - quit


    def createWindow(self, xmax, ymax, cellsize):
        self.bgColor = 'white'#color_rgb(230, 216, 181)
        self.cellsize = cellsize
        self.iterationWidth = 30
        self.xmax = xmax
        self.ymax = ymax

        self.field = []
        for i in range(self.xmax):
            self.field.append([])
            for j in range(self.ymax):
                celltype = randrange(0, 3 + 1)
                self.field[i].append(cellObj(i, j, celltype, self.bgColor))

        self.width = self.xmax * self.cellsize
        self.hight = self.ymax * self.cellsize
        self.iterationLabel = Text(Point(self.width - 1 + self.iterationWidth / 2, self.iterationWidth / 2), self.iteration)
        self.window = GraphWin('Game of live', self.width + 1 + self.iterationWidth, self.hight + 1)
        

    def pause(self):
        message = Text(Point(self.width / 2, self.cellsize / 2), 'Click anywhere to quit.')
        message.draw(self.window)
        self.window.getMouse()
        self.window.close()


    def windowClear(self):
        p1 = Point(0, 0)
        p2 = Point(self.width, 0)
        p3 = Point(self.width, self.hight)
        p4 = Point(0, self.hight)

        verticles = [p1, p2, p3, p4]
        bg = Polygon(verticles)
        bg.setFill(self.bgColor)
        bg.setOutline(self.bgColor)

        bg.draw(self.window)


    def drawline(self, x1, y1, x2, y2):
        if self.window.isOpen() :
            Line(Point(x1, y1), Point(x2, y2)).draw(self.window)
        else :
            self.quit()
 

    def drawCells(self):
        x, y = 0, 0
        
        while (x <= self.width):
            self.drawline(x, 0, x, self.hight)
            x += self.cellsize

        while (y <= self.hight):
            self.drawline(0, y, self.width, y)
            y += self.cellsize


    def showInfo(self):
        
        self.iterationLabel.setText(self.iteration)


    def drawCell(self, x, y, thisCell):
        dx = thisCell.x - thisCell.oldx
        dy = thisCell.y - thisCell.oldy
        thisCell.setColor(self.bgColor)
        thisCell.ghost.setFill(thisCell.color)
        thisCell.ghost.move(dx, dy)


    def firstDrawField(self):
        if self.window.isOpen() :
            self.iterationLabel.draw(self.window)
            for i in range(self.xmax):
                for j in range(self.ymax):
                    thisCell = self.field[i][j]
                    p1 = Point(i * self.cellsize, j * self.cellsize)
                    p2 = Point((i + 1) * self.cellsize, j * self.cellsize)
                    p3 = Point((i + 1) * self.cellsize, (j + 1) * self.cellsize)
                    p4 = Point(i * self.cellsize, (j + 1) * self.cellsize)

                    verticles = [p1, p2, p3, p4]
                    newCell = Polygon(verticles)
                    thisCell.ghost = newCell
                    thisCell.ghost.setFill(thisCell.color)

                    if self.window.isOpen() :
                        thisCell.ghost.draw(self.window) 
                    else :
                        self.quit()

        else :
            self.quit()


    def drawField(self):
        for i in range(self.xmax):
            for j in range(self.ymax):
                thisCell = self.field[i][j]
                if (thisCell.oldtype != thisCell.type) | (thisCell.oldx != thisCell.x) | (thisCell.oldy != thisCell.y) :
                    self.drawCell(i, j, thisCell)
                    thisCell.oldx = thisCell.x
                    thisCell.oldy = thisCell.y
                    thisCell.oldtype = thisCell.type

        self.showInfo()


    def countNumberObjects(self, x, y, objtype):
        objAmount = 0
        radius = 1

        for i in range(x - radius, x + radius + 1) :
            for j in range(y - radius, y + radius + 1) :
                try :
                    if (i, j) != (x, y): # don't take into account yourself
                        if self.field[i][j].type == objtype :
                            objAmount += 1
                except :
                    pass

        return objAmount


    def regulatePopulation(self):
        for i in range(self.xmax):
            for j in range(self.ymax):
                if self.field[i][j].type != 2 :
                    fishAmount = self.countNumberObjects(i, j, 1)
                    shrimpAmount = self.countNumberObjects(i, j, 3)
                    # birth of fish or shrimp
                    if self.field[i][j].type == 0 :
                        if fishAmount == 3 :
                            self.field[i][j].type = 1
                        elif shrimpAmount == 3 :
                            self.field[i][j].type = 3

                    # kill extra fish
                    elif self.field[i][j].type == 1 :
                        if (fishAmount <= 1) | (fishAmount >= 4) :
                            self.field[i][j].type = 0

                    # kill extra shrimp
                    elif self.field[i][j].type == 3 :
                        if (shrimpAmount <= 1) | (shrimpAmount >= 4) :
                            self.field[i][j].type = 0

        
    def worldLoop(self, sleeptime):
        while (True):  
            if self.window.isOpen() :
                self.iteration += 1
                self.regulatePopulation()
                self.drawField()
                time.sleep(sleeptime)
            else :
                self.quit()

        self.pause()


    def preStart(self):
        message = Text(Point(self.width / 2, self.cellsize), 'Click anywhere to start.')
        message.draw(self.window)
        self.window.getMouse()


    def start(self, sleeptime):
        self.preStart()
        self.windowClear()
        self.drawCells()
        self.firstDrawField()
        self.status = 1
        self.worldLoop(sleeptime)
    

    def quit(self):
        self.status = 2
        self.__del__()
        print('-- Exit! --')
        raise SystemExit(0)


    def __del__(self):
        if self.status == 2 :
            self.window.close()



def main():
    print('-- Tinkoff Fintech Task #9 --')
    print('-- Created by Skryabin Gleb --')

    gol = GameOfLive()
    rows = 15
    cols = 11
    cellsize = 20
    waitingTime  = 0.8

    print('-- Create window --') 
    gol.createWindow(rows, cols, cellsize)

    print('-- Start Game of live! --')
    gol.start(waitingTime)



main()