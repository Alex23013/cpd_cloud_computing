import sys
import math
import heapq
from time import time

class Cell:
  def __init__(self, pos):
    self.pos = pos
    self.is_obs = False
    self.neighbours = {}
    self.visited = False  
    self.weight = 1000#sys.maxint
    self.father = {}
    self.dir = -1
  
  def printCell2d(self):
    print "(",self.pos[0],",",self.pos[1],")",
#   for i in xrange(len(self.pos)):
#     print self.pos[i]
  def printCell3d(self):
    print "(",self.pos[0],",",self.pos[1],",",self.pos[2],")"

  def setAsObstacle(self):
    self.is_obs = True
  
  def setAsVisited(self):
    self.visited = True
  
  def setNeighbours(self, neighbours):
    self.neighbours = neighbours

  def isObstacle(self):
    return self.is_obs
  
  def Edistance(self, other):
#    self.printCell2d()
#    other.printCell2d()
    return round(math.sqrt((float(self.pos[0])-float(other.pos[0]))**2 + (float(self.pos[1])-float(other.pos[1]))**2),1)
  
class Rectangle:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.tiles = 0
    self.homogeneus = False
    self.dir = -1
  
  def print_rdims(self):
    print " s:",
    self.start.printCell2d()
    print " e:",
    self.end.printCell2d()
  
  def set_features(self, tiles, homogeneus, dir):
    self.tiles = tiles
    self.homogeneus = homogeneus
    self.dir = dir

  def print_comp(self):
    print "\n",
    self.print_rdims()
    print "tiles:",self.tiles, "h:",self.homogeneus, "dir:",self.dir,


class Grid:
  def __init__(self, dims):
    self.dims = dims
    self.mGrid =[[Cell([row,column]) for column in xrange(dims[0])]  
                      for row in xrange(dims[1])] 
    self.cpd = dict()

  def initial_rectangles(self, start):
    rects = []  
    if start.pos[1]+1 < self.dims[1]:
      rects.append(Rectangle(self.mGrid[start.pos[0]][start.pos[1]+1], self.mGrid[start.pos[0]][self.dims[1]-1])) # right
      if start.pos[0]+1 < self.dims[0]:    
        rects.append(Rectangle(self.mGrid[start.pos[0]+1][start.pos[1]+1], self.mGrid[self.dims[0]-1][self.dims[1]-1])) # right-down  
      if start.pos[0]-1 >= 0:
        rects.append(Rectangle(self.mGrid[0][start.pos[1]+1], self.mGrid[start.pos[0]-1][self.dims[1]-1])) # right-up
    if start.pos[0]+1 < self.dims[0]:
      rects.append(Rectangle(self.mGrid[start.pos[0]+1][start.pos[1]], self.mGrid[self.dims[0]-1][start.pos[1]])) # down
      if start.pos[1]-1 >= 0:
        rects.append(Rectangle(self.mGrid[start.pos[0]+1][0], self.mGrid[self.dims[0]-1][start.pos[1]-1])) # left-down  
    if start.pos[1]-1 >= 0:
      rects.append(Rectangle(self.mGrid[start.pos[0]][0], self.mGrid[start.pos[0]][start.pos[1]-1])) # left
    if start.pos[0]-1 >= 0:    
      rects.append(Rectangle(self.mGrid[0][start.pos[1]], self.mGrid[start.pos[0]-1][start.pos[1]])) # up
      if start.pos[1]-1 >= 0:
       rects.append(Rectangle(self.mGrid[0][0], self.mGrid[start.pos[0]-1][start.pos[1]-1])) # left-up
    return rects

  def process_rect(self, rect):
    homogeneus = True
    dir = rect.start.dir
    tiles = 0
#    rect.print_rdims()
    for i in xrange(rect.start.pos[0], rect.end.pos[0]+1):
      for j in xrange(rect.start.pos[1], rect.end.pos[1]+1):
        current = self.mGrid[i][j]
#        print "current",current.pos
        if current.dir != dir and not current.isObstacle():
          homogeneus = False
          dir = -1
        if not current.isObstacle():
          tiles = tiles+1
    return tiles, homogeneus, dir
  
  def left_homogenize(self, rect):
    homogeneus = True
    split = rect.start.pos[1]
    while homogeneus and split+1 <= rect.end.pos[1]:
      split = split +1
      n_split = self.mGrid[rect.end.pos[0]][split]
      p_rect = Rectangle(rect.start,n_split)
      t,h,dir = self.process_rect(p_rect)
    r1 = Rectangle(rect.start,self.mGrid[rect.end.pos[0]][split-1])
    t,h,d = self.process_rect(r1)
    if h == True:
      r1.set_features(t,h,d)
      return r1, 1, split
    else:
      return -1, -1, -1

  def right_homogenize(self, rect):
    homogeneus = True
    split = rect.end.pos[1]
    while homogeneus and split-1 >= rect.start.pos[1]:
      split = split -1
      n_split = self.mGrid[rect.start.pos[0]][split]
      p_rect = Rectangle(n_split,rect.end)
      t,h,dir = self.process_rect(p_rect)
    r1 = Rectangle(self.mGrid[rect.start.pos[0]][split+1],rect.end)
    t,h,d = self.process_rect(r1)
    if h == True:
      r1.set_features(t,h,d)
      return r1, 2, split 
    else:
      return -1, -1, -1

  def top_homogenize(self,rect):
    homogeneus = True
    split = rect.start.pos[0]
    while homogeneus and split+1 <= rect.end.pos[1]:
      split = split +1
      n_split = self.mGrid[split][rect.end.pos[1]]
      p_rect = Rectangle(rect.start,n_split)
      t,h,dir = self.process_rect(p_rect)
    r1 = Rectangle(rect.start,self.mGrid[split-1][rect.end.pos[1]])
    t,h,d = self.process_rect(r1)
    if h == True:
      r1.set_features(t,h,d)
      return r1, 3, split
    else:
      return -1, -1, -1

  def bottom_homogenize(self, rect):
    homogeneus = True
    split = rect.end.pos[0]
    while homogeneus and split-1 >= rect.start.pos[0]:
      split = split -1
      n_split = self.mGrid[split][rect.start.pos[1]]
      p_rect = Rectangle(n_split,rect.end)
      t,h,dir = self.process_rect(p_rect)

    r1 = Rectangle(self.mGrid[split+1][rect.start.pos[0]],rect.end)
    t,h,d = self.process_rect(r1)
    if h == True:
      r1.set_features(t,h,d)
      return r1, 4, split
    else:
      return -1, -1, -1

  def compRect(self, rect, opt, split):
    if opt == 1: #left
      return Rectangle(self.mGrid[rect.start.pos[0]][split],rect.end)
    if opt == 2: #right
      return Rectangle(rect.start, self.mGrid[rect.end.pos[0]][split])
    if opt == 3: #top
      return Rectangle(self.mGrid[split][rect.start.pos[0]],rect.end)
    if opt == 4: #bottom
      return Rectangle(rect.start, self.mGrid[split][rect.end.pos[1]])

  def homogenize(self, rect,result):
#    print "rect before homogenize",
#    rect.print_comp()
    t,h,d = self.process_rect(rect)
    if h == True :
      result.append(rect)
      return
    
    maxTiles = 0
    optSplit = 0
    split = 0
    hRect = ""
    r1, opt1, split1 = self.left_homogenize(rect)
    if r1 != -1:
      #print "left_h:", r1.tiles, "opt:",opt
      if r1.tiles > max_tiles:
        maxTiles = r1.tiles
        optSplit = opt1
        split = split1
        hRect = r1
    r2, opt2, split2 = self.top_homogenize(rect)
    if r2 != -1:
      #print "top_h:", r2.tiles, "opt:",opt2
      if r2.tiles > maxTiles:
        maxTiles = r2.tiles
        optSplit = opt2
        split = split2
        hRect = r2

    r3, opt3, split3 = self.right_homogenize(rect)
    if r3 != -1:
      #print "right_h:", r3.tiles, "opt:",opt3
      if r3.tiles > maxTiles:
        maxTiles = r3.tiles
        optSplit = opt3
        split = split3
        hRect = r3

    r4, opt4, split4 = self.bottom_homogenize(rect)
    if r4 != -1:
      #print "bottom_h:", r4.tiles, "opt:",opt4
      if r4.tiles > maxTiles:
        maxTiles = r4.tiles
        optSplit = opt4
        split = split4   
        hRect = r4

    #print "maxTile:", maxTiles, "optSplit", optSplit
    compRect = self.compRect(rect, optSplit, split)
    t,h,d = self.process_rect(compRect)
    compRect.set_features(t,h,d)
    #print "compRect: ",
    #compRect.print_comp()
    result.append(hRect)

    self.homogenize(compRect, result)
    #hRect.print_comp()

  def printGrid(self):
    for  i in xrange (len(self.mGrid)):
      for  j in xrange (len(self.mGrid[i])):
        print self.mGrid[i][j].dir,
      print "\n",
  
  def get_neightbours(self,start):
    n = []   
    if start.pos[1]+1 < self.dims[1]: # right
      var1 = self.mGrid[start.pos[0]][start.pos[1]+1]      
      if not var1.isObstacle():
        n.append(var1)
      if start.pos[0]+1 < self.dims[0]: #abajo y derecha
        var2 = self.mGrid[start.pos[0]+1][start.pos[1]+1]
        if not var2.isObstacle():
          n.append(var2)
      if start.pos[0]-1 >= 0: #arriba y derecha
        var3 = self.mGrid[start.pos[0]-1][start.pos[1]+1]
        if not var3.isObstacle():
          n.append(var3)
    if start.pos[0]+1 < self.dims[0]: #abajo
      var4 = self.mGrid[start.pos[0]+1][start.pos[1]]
      if not var4.isObstacle():
        n.append(var4)
      if start.pos[1]-1 >= 0: #abajo y izquierda
        var5 = self.mGrid[start.pos[0]+1][start.pos[1]-1]
        if not var5.isObstacle():
          n.append(var5)
    if start.pos[0]-1 >= 0: #arriba
      var6 = self.mGrid[start.pos[0]-1][start.pos[1]]
      if not var6.isObstacle():
        n.append(var6)
      if start.pos[1]-1 >= 0: #arriba y izquierda
        var7 = self.mGrid[start.pos[0]-1][start.pos[1]-1]
        if not var7.isObstacle():
          n.append(var7)
    if start.pos[1]-1 >= 0: # izquierda
          var8 = self.mGrid[start.pos[0]][start.pos[1]-1]
          if not var8.isObstacle():
            n.append(var8)
#    print "neightbours of "+str(start.pos[0])+","+str(start.pos[1])
#    for i in xrange(len(n)):
#      print n[i].pos
    return n

  def initial_directions(self,start):
    if start.pos[1]+1 < self.dims[1]: # derecha
      var1 = self.mGrid[start.pos[0]][start.pos[1]+1]      
      if not var1.isObstacle():
        var1.dir = 0
      if start.pos[0]+1 < self.dims[0]: #abajo y derecha
        var2 = self.mGrid[start.pos[0]+1][start.pos[1]+1]
        if not var2.isObstacle():
          var2.dir = 1
      if start.pos[0]-1 >= 0: #arriba y derecha
        var3 = self.mGrid[start.pos[0]-1][start.pos[1]+1]
        if not var3.isObstacle():
          var3.dir = 7
    if start.pos[0]+1 < self.dims[0]: #abajo
      var4 = self.mGrid[start.pos[0]+1][start.pos[1]]
      if not var4.isObstacle():      
        var4.dir = 2
      if start.pos[1]-1 >= 0: #abajo y izquierda
        var5 = self.mGrid[start.pos[0]+1][start.pos[1]-1]
        if not var5.isObstacle():        
          var5.dir = 3
    if start.pos[0]-1 >= 0: #arriba
      var6 = self.mGrid[start.pos[0]-1][start.pos[1]]
      if not var6.isObstacle():
        var6.dir = 6
      if start.pos[1]-1 >= 0: #arriba y izquierda
        var7 = self.mGrid[start.pos[0]-1][start.pos[1]-1]
        if not var7.isObstacle():        
          var7.dir = 5
    if start.pos[1]-1 >= 0: # izquierda
      var8 = self.mGrid[start.pos[0]][start.pos[1]-1]
      if not var8.isObstacle():
        var8.dir = 4

  def dijkstra(self,start):
    print "init Dijkstra"
    self.initial_directions(start)
    start.weight = 0
    self.printGrid()
    heap = []
    heapq.heappush(heap,(start.weight,start))
    while len(heap):
      current = heap[0][1]
#      print "current",current
      heapq.heappop(heap)
      current.setAsVisited()
      n = self.get_neightbours(current)
#      print "type(n)",type(n)
      for i in xrange( len(n)):
        if n[i].visited == False:
          newd = current.weight + current.Edistance(n[i])
#          print n[i].pos," newd ",newd, "n[i].weight ", n[i].weight
          if newd <= n[i].weight:
            n[i].weight = newd
            if current != start:
              n[i].dir = current.dir
            heapq.heappush(heap,(newd,n[i]))
  
  def compress(self, start):  
    frects = []
    irects = self.initial_rectangles(start)
    print "initial rects:",len(irects)
    for r in xrange(len(irects)):
      t,h,d = self.process_rect(irects[r])
      irects[r].set_features(t,h,d)
#      irects[r].print_comp()
#    print"\n"
    for r in xrange(len(irects)):
      if irects[r].homogeneus == True:
        frects.append(irects[r])
      else:
        self.homogenize(irects[r],frects)
    id = start.pos[0]*self.dims[1]+start.pos[1]    
    self.cpd[id]=frects
    return frects


def readMap():
  f = open("map.map", "r")
  list_of_lines = f.readlines()
  gridFromMap = Grid([len(list_of_lines), len(list_of_lines[0]) - 1])
  print(len(gridFromMap.mGrid[0]))
  row = 0
  for line in list_of_lines:
    col = 0
    for letter in line:
      #print "\nr:",row,"c:",col,
      if letter != '\n':
        if letter == 'T':
          gridFromMap.mGrid[row][col].setAsObstacle()
        col = col + 1
    row = row + 1
  f.close()
  return gridFromMap


cel = Cell([1,2,0])
#cel.printCell2d()
#cel.printCell3d()
#print cel.pos

grid = Grid([10,10])
grid.mGrid[1][1].setAsObstacle()
grid.mGrid[2][1].setAsObstacle()
print "grid"

start_cell = grid.mGrid[3][3]
start_time = time()
grid.dijkstra(start_cell)
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)
grid.printGrid()
cpd =  grid.compress(start_cell)
print "\nfinal CPD's:",
for c in cpd :
  print c.print_comp(), 

'''
print"Final Result"  
for key, value in grid.cpd.iteritems() :
    print key, value
'''

#print grid.mGrid[1][1].Edistance(grid.mGrid[0][0])
'''
gridFromMap = readMap()
gridFromMap.printGrid()
start_cell = gridFromMap.mGrid[5][5]
start_time = time()
gridFromMap.dijkstra(start_cell)
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)
gridFromMap.printGrid() '''

