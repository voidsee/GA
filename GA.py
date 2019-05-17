# -*- coding: utf-8 -*-
from random import random,sample,uniform,shuffle,randint
class GA(object):
      def __init__(self, aCrossRate, aMutationRate, aLifeNum, aGeneLen, aSsess = lambda life : 1):
            self.crsRate = aCrossRate
            self.mutRate = aMutationRate
            self.lifeNum = aLifeNum
            self.geneLen = aGeneLen
            self.assess = aSsess  
            self.lives = []    
            self.best = None   
            self.generation = 0
            self.crossCount = 0
            self.mutaCount = 0
            self.bounds = 0.0 #轮盘
            self.initPopulation()

      def initPopulation(self):
            self.lives = []
            for i in range(self.lifeNum):
                  gene = [x for x in range(self.geneLen)] 
                  shuffle(gene)
                  life = Life(gene)
                  life.score = self.assess(life)
                  self.lives.append(life)

      def getbest(self):
            self.bounds = 0.0
            self.best = self.lives[0]
            for life in self.lives:
                  self.bounds += life.score
                  if self.best.score < life.score:
                        self.best = life


      def cross(self, p1, p2):
            x1 = randint(0, self.geneLen - 1)
            x2 = randint(x1, self.geneLen - 1)
            tempGene = p2.gene[x1:x2]
            newGene = []
            p1len = 0
            for g in p1.gene:
                  if p1len == x1:
                        newGene.extend(tempGene) 
                        p1len += 1
                  if g not in tempGene:
                        newGene.append(g)
                        p1len += 1
            self.crossCount += 1
            return newGene

      def  mutation(self, gene):
            x1 = randint(0, self.geneLen - 1)
            x2 = randint(0, self.geneLen - 1)
            newGene = gene[:]     
            newGene[x1], newGene[x2] = newGene[x2], newGene[x1]
            self.mutaCount += 1
            return newGene

      # def chicken(self):#轮盘赌
      #       r = uniform(0, self.bounds)
      #       for life in self.lives:
      #             r -= life.score
      #             if r <= 0:
      #                   return life
      def chicken(self):#锦标赛
            smp = sample(self.lives, self.lifeNum//5 + 1)
            best = smp[0]
            for life in smp:
                  if best.score < life.score:
                        best = life
            return best


      def newChild(self):
            for i in range(50):
                  p1, p2 = self.chicken(), self.chicken()
                  rate = random()
                  if rate < self.crsRate:
                        gene = self.cross(p1, p2)
                  else:
                        gene = p1.gene
                  rate = random()
                  if rate < self.mutRate:
                        gene = self.mutation(gene)

                  life = Life(gene)
                  life.score = self.assess(life)
                  if life.score > self.best.score:
                        break

            return life

      def born(self):
            self.getbest()
            newLives = []
            newLives.append(self.best)
            while len(newLives) < self.lifeNum:
                  newLives.append(self.newChild())
            self.lives = newLives
            self.generation += 1

class Life(object):
      def __init__(self, aGene = None):
            self.gene = aGene
            self.score = 0.0
