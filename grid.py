import sys, os
import math
import heapq

from cell import Cell

class Grid:
  def __init__(self, dims):
    self.dims = dims
    self.mGrid=[[Cell([row,column]) for column in range(dims[0])]  
                      for row in range(dims[1])] 
    
  def printGrid(self):
    for  i in range (len(self.mGrid)):
      for  j in range (len(self.mGrid[i])):
        print self.mGrid[i][j].dir,
      print "\n",
  
  def get_neightbours(self,start):
    n = []   
    if start.pos[1]+1 < self.dims[1]: # derecha
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
    self.mGrid[start.pos[0]][start.pos[1]].weight = 0
    heap = []
    heapq.heappush(heap,(start.weight,start))
    self.mGrid[start.pos[0]][start.pos[1]].inHeap = True
    while len(heap):
      current = heap[0][1]
      heapq.heappop(heap)
      self.mGrid[current.pos[0]][current.pos[1]].visited = True
      n = self.get_neightbours(current)
      for i in xrange( len(n)):
        if self.mGrid[n[i].pos[0]][n[i].pos[1]].visited == False:
          newd = current.weight + current.Edistance(n[i])
          if newd <= n[i].weight:
            self.mGrid[n[i].pos[0]][n[i].pos[1]].weight = newd
            if current != start:
              self.mGrid[n[i].pos[0]][n[i].pos[1]].dir = current.dir
            if self.mGrid[n[i].pos[0]][n[i].pos[1]].inHeap == False:
              heapq.heappush(heap,(newd,n[i]))
              self.mGrid[n[i].pos[0]][n[i].pos[1]].inHeap = True


