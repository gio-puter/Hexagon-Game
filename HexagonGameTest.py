from tkinter import *
import math
from math import sin, cos, sqrt, radians
import random

class Hex():
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "black"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, centerX, centerY, radius, tags): 
        self.master = master # canvas control
        self.centerX = centerX # hexagon x-coord
        self.centerY = centerY # hexagon y-coord
        self.radius = radius # hexagon radius
        self.tags = tags

        self.selected = False
    
    def _switch(self):
        self.selected = not self.selected

    def draw(self):
        if self.master == None:
            return
        
        angle = 60
        coords = []
        fill = self.FILLED_COLOR_BG if self.selected else self.EMPTY_COLOR_BG
        outline = self.FILLED_COLOR_BORDER if self.selected else self.EMPTY_COLOR_BORDER

        for i in range(6):
            vertX = self.centerX + self.radius * cos(radians(angle * i))
            vertY = self.centerY - self.radius * sin(radians(angle * i))
            coords.append((vertX, vertY))
        
        self.master.create_polygon(coords[0][0], coords[0][1],
                                   coords[1][0], coords[1][1],
                                   coords[2][0], coords[2][1],
                                   coords[3][0], coords[3][1],
                                   coords[4][0], coords[4][1],
                                   coords[5][0], coords[5][1],
                                   fill = fill, outline = outline,
                                   activefill = "yellow", tags = self.tags)

    def inRadius(self, x, y):
        return math.hypot(self.centerX - x, self.centerY - y) < self.radius

class HexGrid(Canvas):
    WIDTH = 1250
    HEIGHT = 650
    BACKGROUND = 'black'
    def __init__(self, master, rowNumber, columnNumber, hexRadius, *args, **kwargs):
        Canvas.__init__(self, master, width = self.WIDTH, height = self.HEIGHT, background = self.BACKGROUND, *args, **kwargs)

        self.master = master
        self.rows = rowNumber
        self.cols = columnNumber

        centerX = self.WIDTH/2
        centerY = self.HEIGHT/2
        self.startX = centerX - 1.5 * (columnNumber//2) * hexRadius
        self.startY = centerY - (rowNumber - 1)*(sqrt(3)/2 * hexRadius)

        self.hexRadius = hexRadius
        self.grid = []
        self.hexDict = {}
        self.switched = []

        self.initGrid(rowNumber, columnNumber, hexRadius)
        self.printColumnLabels(columnNumber)
        self.printRightDiagLabels(columnNumber)
        self.printLeftDiagLabels(2*rowNumber-1, columnNumber)

        self.bind("<Button-1>", self.handleLeftMouseClick)
        self.bind("<B1-Motion>", self.handleLeftMouseMotion)
        self.bind("<Button-2>", self.handleRightMouseClick)
        self.bind("<B2-Motion>", self.handleRightMouseMotion)
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        self.bind("<ButtonRelease-2>", lambda event: self.switched.clear())

    def initGrid(self, rows, cols, rad):
        xOffset = 1.5 * rad
        yOffset = sqrt(3)*rad/2
        for row in range(2*rows-1):
            for col in range(cols):
                if (row + col) % 2 == 0: # when row and col both even or odd
                    continue
                h = Hex(self, self.startX + col * xOffset, self.startY + row * yOffset, rad, '{}.{}'.format(row, col))
                colored = random.randint(0, 4) < 2 # EXPECT 40% OF HEXAGONS TO BE COLORED
                self.hexDict[h.tags] = {
                    'cell' : h, 
                    'row' : row, 
                    'col' : col, 
                    'sum' : row + col,
                    'colored' : colored
                }
                # if colored:
                #     h.selected = True
                h.draw()
                self.grid.append(h)

    """
    If selected hexagon is white, then it should now be green (user believes this is part of the solution)
    If selected hexagon is gray, then do nothing
    """
    def handleLeftMouseClick(self, event):
        self.switched.clear()
        x, y = event.x, event.y
        
        try:
            hex = self.grid[self.find_closest(x, y)[0]-1] # better more smart way of doing this is checking the dictionary
            if not hex.inRadius(x,y):
                return
        except:
            return 
        
        color = self.itemconfig(hex.tags)['fill'][-1]
        if color == 'gray': return
        
        hex._switch()
        if hex.selected:
            self.itemconfig(hex.tags, fill='green', activefill='')
        else:
            self.itemconfig(hex.tags, fill='white', activefill='yellow')

        self.switched.append(hex)
        # print(hex.tags)
        self.checkForComplete(2*self.rows-1, self.cols)

    def handleLeftMouseMotion(self, event):
        x, y = event.x, event.y
        
        try:
            hex = self.grid[self.find_closest(x, y)[0]-1] # better more smart way of doing this is checking the dictionary
            if not hex.inRadius(x,y):
                return
            if hex in self.switched:
                return
        except:
            return 
        
        color = self.itemconfig(hex.tags)['fill'][-1]
        if color == 'gray': return

        hex._switch()
        if hex.selected:
            self.itemconfig(hex.tags, fill='green', activefill='')
        else:
            self.itemconfig(hex.tags, fill='white', activefill='yellow')
        
        self.switched.append(hex)
        # print(hex.tags)
        self.checkForComplete(2*self.rows-1, self.cols)

    """
    If selected hexagon is white, then it should now be gray (user believes this is not part of the solution)
    If selected hexagon is green, then do nothing
    """
    def handleRightMouseClick(self, event):
        self.switched.clear()
        x, y = event.x, event.y

        try:
            hex = self.grid[self.find_closest(x, y)[0]-1] # better more smart way of doing this is checking the dictionary
            if not hex.inRadius(x,y):
                return
        except:
            return 

        color = self.itemconfig(hex.tags)['fill'][-1]
        # hex._switch()
        if color == 'green': return
        
        if color == 'white':
            self.itemconfig(hex.tags, fill='gray', activefill = '')
        else:
            self.itemconfig(hex.tags, fill='white', activefill = 'yellow')

        self.switched.append(hex)
        # print(hex.tags)
        # self.checkForComplete(2*self.rows-1, self.cols)

    def handleRightMouseMotion(self, event):
        x, y = event.x, event.y
        
        try:
            hex = self.grid[self.find_closest(x, y)[0]-1] # better more smart way of doing this is checking the dictionary
            if not hex.inRadius(x,y):
                return
            if hex in self.switched:
                return
        except:
            return 
        
        color = self.itemconfig(hex.tags)['fill'][-1]
        if color == 'green': return

        if color == 'white':
            self.itemconfig(hex.tags, fill='gray', activefill = '')
        else:
            self.itemconfig(hex.tags, fill='white', activefill = 'yellow')
        
        self.switched.append(hex)
        # print(hex.tags)
        # self.checkForComplete(2*self.rows-1, self.cols)

    def printColumnLabels(self, cols):
        for i in range(cols):
            result = list(filter(lambda x: x[1]['col'] == i, self.hexDict.items()))
            count = 0
            for tag, hex in result:
                if hex['colored']:
                    count += 1 
            label_hex = result[-1][1]['cell']
            self.create_text(label_hex.centerX, label_hex.centerY + sqrt(3)*self.hexRadius/2 + 25, text = count, fill = 'CadetBlue2')

    def printRightDiagLabels(self, cols):
        topRow = list(filter(lambda x: x[1]['row'] == 0, self.hexDict.items()))
        rightCol = list(filter(lambda x: x[1]['col'] == cols - 1, self.hexDict.items()))
        rightDiagStart = topRow + rightCol
        sums = []
        for tag, hex in rightDiagStart:
            sums.append(hex['sum'])

        for i in range(len(sums)):
            result = list(filter(lambda x: x[1]['sum'] == sums[i], self.hexDict.items()))
            count = 0
            for tag, hex in result:
                if hex['colored']:
                    count += 1
            label_hex = result[0][1]['cell']
            self.create_text(label_hex.centerX + self.hexRadius, label_hex.centerY - sqrt(3)*self.hexRadius/4, text = count, fill = 'red')

    def printLeftDiagLabels(self, rows, cols):
        botRow = list(filter(lambda x: x[1]['row'] == rows - 1, self.hexDict.items()))
        botRow.reverse()
        rightCol = list(filter(lambda x: x[1]['col'] == cols - 1, self.hexDict.items()))
        leftDiagStart = rightCol + botRow
        i = 0
        for tag, hex in leftDiagStart:
            done = False
            temp = self.hexDict[tag]
            count = 0
            while not done:
                if temp['colored']:
                    count += 1
                if temp['row'] == 0 or temp['col'] == 0:
                    done = True
                else:
                    temp = self.hexDict['{}.{}'.format(temp['row']-1, temp['col'] - 1)]
            label_hex = temp['cell']
            self.create_text(label_hex.centerX - self.hexRadius, label_hex.centerY - sqrt(3)*self.hexRadius/4, text = count, fill = 'yellow')
            i += 1 

    def checkForComplete(self, rows, cols):
        result = self.checkCols(cols) and self.checkRightDiag(cols) and self.checkLeftDiag(rows, cols)
        if result:
            print('YAYYYY')
        # return self.checkCols(cols) and self.checkRightDiag(cols) and self.checkLeftDiag(rows, cols)

    def checkCols(self, cols):
        for i in range(cols):
            result = list(filter(lambda x: x[1]['col'] == i, self.hexDict.items()))
            cor_count = 0
            sel_count = 0
            for tag, hex in result:
                if hex['colored']:
                    cor_count += 1 
                if hex['cell'].selected:
                    sel_count += 1
            if sel_count != cor_count: return False
        return True
    
    def checkRightDiag(self, cols):
        topRow = list(filter(lambda x: x[1]['row'] == 0, self.hexDict.items()))
        rightCol = list(filter(lambda x: x[1]['col'] == cols - 1, self.hexDict.items()))
        rightDiagStart = topRow + rightCol

        for tag, hex in rightDiagStart:
            result = list(filter(lambda x: x[1]['sum'] == hex['sum'], self.hexDict.items()))
            cor_count = 0
            sel_count = 0
            for tag, hex in result:
                if hex['colored']:
                    cor_count += 1
                if hex['cell'].selected:
                    sel_count += 1
            if cor_count != sel_count: return False
        return True
    
    def checkLeftDiag(self, rows, cols):
        botRow = list(filter(lambda x: x[1]['row'] == rows - 1, self.hexDict.items()))
        botRow.reverse()
        rightCol = list(filter(lambda x: x[1]['col'] == cols - 1, self.hexDict.items()))
        leftDiagStart = rightCol + botRow

        i = 0
        for tag, hex in leftDiagStart:
            done = False
            temp = self.hexDict[tag]
            cor_count = 0
            sel_count = 0
            while not done:
                if temp['colored']:
                    cor_count += 1
                if temp['cell'].selected:
                    sel_count += 1
                if temp['row'] == 0 or temp['col'] == 0:
                    done = True
                else:
                    temp = self.hexDict['{}.{}'.format(temp['row']-1, temp['col'] - 1)]
            if cor_count != sel_count: return False
            i += 1 
        return True

from math import comb
if __name__ == "__main__":
    app = Tk()

    grid = HexGrid(app, 4, 5, 75) # (4,5) (5,7) (6,9) (7, 11) <-- other options for first two arguments
    grid.pack()

    app.mainloop()

