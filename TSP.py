# -*- encoding: utf-8 -*-
from GA import GA

class TSP(object):
      def __init__(self, city_file, aLifeNum = 99, aCrsRate=0.7, aMutaRate=0.7):
            self.initCitys(city_file)
            self.lifeNum = aLifeNum
            self.ga = GA(aCrossRate = aCrsRate, 
                  aMutationRate = aMutaRate, 
                  aLifeNum = self.lifeNum, 
                  aGeneLen = len(self.citys), 
                  aSsess = self.assess())

      def initCitys(self, city_file):
            self.citys = []
            with open(city_file, "r") as fd:
                  line = fd.readline()
                  while line:
                        tmp = line.strip().split(',')
                        self.citys.append((tmp[0],float(tmp[1]),float(tmp[2])))
                        line = fd.readline()
            
      def distance(self, gene):
            distance = 0.0
            for i in range(-1, len(self.citys)-1):
                  g1, g2 = gene[i], gene[i + 1]
                  city1, city2 = self.citys[g1], self.citys[g2]
                  distance += ((city1[1]-city2[1])**2 + (city1[2]-city2[2])**2)**0.5

            return distance


      def assess(self):
            return lambda life: 10/self.distance(life.gene)


      def run(self, n = 0):
            while n > 0:
                  self.ga.born()
                  distance = self.distance(self.ga.best.gene)
                  print (("%d代: %f") % (self.ga.generation, distance))
                  n -= 1


if __name__ == '__main__':
      tsp = TSP('citys.txt', aCrsRate=0.7, aMutaRate=0.2)
      tsp.run(25)