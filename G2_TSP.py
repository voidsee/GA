# -*- encoding: utf-8 -*-
import tkinter as Tk
from tkinter import simpledialog
from time import sleep
from GA import GA

class TSP_WIN(object):
      def __init__(self, aRoot, aLifeNum=99, aWidth=1080, aHeight=720):
            self.colors = ["red", "green", "blue", "purple", "orange", "black",]
            self.root = aRoot
            self.lifeNum = aLifeNum
            self.width = aWidth
            self.height = aHeight
            self.canvas = Tk.Canvas(
                        self.root,
                        bg = "#F5F5F5",
                        width = self.width,
                        height = self.height,)
            self.canvas.pack(expand = Tk.YES, fill = Tk.BOTH)
            self.button = Tk.Button(
                        self.root,
                        bg = "#E6E6FA",
                        text = "Plans",
                        command=self.plans,
            ).place(x=1,y=1)
            self.bindEvents()
            self.initCitys()
            self.reset()
            self.title("TSP")
            self.least_sub_citys=3
            self.canvas.bind('<Button-1>', self.display_sub_sum)

      def initCitys(self,):
            self.citys = []
            with open('citys.txt', "r") as fd:
                  line = fd.readline()
                  while line:
                        tmp = line.strip().split(',')
                        self.citys.append((tmp[0],float(tmp[1]),float(tmp[2])))
                        line = fd.readline()

            minX, minY = self.citys[0][1], self.citys[0][2]
            maxX, maxY = minX, minY
            for city in self.citys[1:]:
                  #minX = city[1] if minX > city[1] else minX
                  if minX > city[1]:
                        minX = city[1]
                  if minY > city[2]:
                        minY = city[2]
                  if maxX < city[1]:
                        maxX = city[1]
                  if maxY < city[2]:
                        maxY = city[2]

            map_w, map_h = maxX - minX, maxY - minY
            x_offset, y_offset = 20, 18
            inner_w, inner_h = self.width-2*x_offset, self.height-2*y_offset
            x_unit, y_unit = inner_w/map_w, inner_h/map_h

            r = 5; self.coordinate=[]
            for city in self.citys:
                  x = (city[1] - minX) * x_unit + x_offset
                  y = inner_h - (city[2] - minY) * y_unit + y_offset
                  self.coordinate.append((x, y))
                  node = self.canvas.create_oval(x-r, y-r, x+r, y+r,
                        fill = "#2FFF4F",
                        activefill = "red",
                        outline = "#000000",
                        tags = city[0],)
                  self.canvas.tag_bind(city[0], '<Button-1>', self.handler_adaptor(self.clickCity, city[0]))
                  self.canvas.create_text(x+r,y-2*r,
                        text=city[0],
                        fill = "#2F2F4F",
                        tags = "city_name",)

      def handler_adaptor(self, fun, *argv):
            return lambda event,fun=fun,argv=argv: fun(event, *argv)
      def clickCity(self, evt, city_name):
            for city in self.citys:
                  if city[0] == city_name :
                        tmp_city = list(city) 
                        tmp_city.append(self.citys.index(city))
                        if tmp_city not in self.sub_citys:
                              self.sub_citys.append(tmp_city)
      def display_sub_sum(self, evt):
            self.canvas.delete("sum")
            self.canvas.create_text(8,715,text=len(self.sub_citys), tags="sum")

      def plans(self,evt=None):
            n=1;
            while not 1<n<len(self.colors)+1:
                  n = simpledialog.askinteger("plans number","Input a Integer(2-%d):"%len(self.colors))
                  if n==None:
                        return None
            for i in range(len(self.colors)):
                  self.canvas.delete("line_%d"%i)
            for i in range(n):
                  if len(self.sub_citys)>self.least_sub_citys:
                        self.sub_start(color = self.colors[i], code=i)
                  else:
                        self.restart()
                        self.start(color = self.colors[i], code =i)
                        sleep(3)

      def distance(self, gene, citys,):
            distance = 0.0
            for i in range(-1, len(citys) - 1):
                  g1, g2 = gene[i], gene[i+1]
                  city1, city2 = citys[g1], citys[g2]
                  distance += ((city1[1]-city2[1])**2 + (city1[2]-city2[2])**2)**0.5
            return distance

      def assess(self):
            return lambda life: 9/self.distance(life.gene,self.citys) 
      def sub_assess(self):
            return lambda life: 9/self.distance(life.gene,self.sub_citys)


      def line(self, gene, color="black", code=0):
            self.canvas.delete("line_%d"%code) 
            self.canvas.delete("city_num") 
            for i in range(-1, len(gene) -1):
                  p1,p2 = self.coordinate[gene[i]], self.coordinate[gene[i+1]]
                  self.canvas.create_line(p1, p2, fill=color, width=2, arrow="last",tags = "line_%d"%code)

      def sub_line(self, gene, color="black", code=0):
            self.canvas.delete("line_%d"%code) 
            self.canvas.delete("city_num") 
            for i in range(-1, len(gene) -1):
                  p1,p2 = self.coordinate[self.sub_citys[gene[i]][3]], self.coordinate[self.sub_citys[gene[i+1]][3]]; x,y = p1
                  #self.canvas.create_line(p1, p2, tags = "line", fill=self.colors[i%(len(self.colors)-1)])
                  self.canvas.create_line(p1, p2, tags = "line_%d"%code, width=2, arrow="last", fill=color)
                  self.canvas.create_text(x+5, y+9, fill=color, text=(i-gene.index(0))%len(gene) +1, tags = "city_num",) #i-循环左移，sub_citys[0]移至0

      def bindEvents(self):
            self.root.bind("r", self.reset)
            self.root.bind("<Return>", self.start)
            self.root.bind("<space>", self.stop)
            self.root.bind("g", self.sub_start)
            self.root.bind("q", self.plans)

      def reset(self, evt = None):
            self.sub_citys=[]
            self.isRunning = False
            self.restart()
            for i in range(len(self.colors)):
                  self.canvas.delete("line_%d"%i)
            self.canvas.delete("city_num") 

      def restart(self):
            self.ga = GA(aCrossRate = 0.8, 
                  aMutationRate = 0.2, 
                  aLifeNum = self.lifeNum, 
                  aGeneLen = len(self.citys), 
                  aSsess = self.assess())

      def sub_start(self, evt = None, color = "black", code=0):
            lenth = len(self.sub_citys)
            if lenth>self.least_sub_citys:
                  self.sub_ga = GA(aCrossRate = 0.5, 
                        aMutationRate = 0.2, 
                        aLifeNum = self.lifeNum, 
                        aGeneLen = len(self.sub_citys),
                        aSsess = self.sub_assess())
                  self.sub_isRunning = True 
                  while self.sub_isRunning:
                        self.sub_ga.born()
                        distance = self.distance(self.sub_ga.best.gene,self.sub_citys)
                        self.sub_line(self.sub_ga.best.gene, color=color,code=code)
                        self.title("代数:%d代    距离:%f" % (self.sub_ga.generation,distance))
                        self.canvas.update()
                        if lenth < 15:
                              if self.sub_ga.generation > 7:
                                    break
                        else:
                              if self.sub_ga.generation > 19:
                                    break
    
      def start(self, evt = None, color="black", code=0):
            self.isRunning = True 
            while self.isRunning:
                  self.ga.born()
                  distance = self.distance(self.ga.best.gene,self.citys)
                  self.line(self.ga.best.gene, color=color, code=code)
                  self.title("代数:%d代    距离:%f" % (self.ga.generation,distance))
                  self.canvas.update()
                  if self.ga.generation > 29:
                        break
      def stop(self, evt = None):
            self.isRunning = False
            self.sub_isRunning = False

      def title(self, text):
            self.root.title(text)
      def mainloop(self):
            self.root.mainloop()


if __name__ == '__main__':
      tsp = TSP_WIN(Tk.Tk())
      tsp.mainloop()