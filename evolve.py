from PIL import Image, ImageChops
import numpy as np
import random
import functools, operator
from screen import Screen

#some standard colors     
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#A chromosome object is the basic unit of the population made up of genes
class Chromosome():
    def __init__(self,color=BLACK,pos=(0,0),alpha=255,rad=0):
        #genes
        self.RGBA=tuple(list(color)+[alpha])
        self.pos=pos
        self.rad=rad

    def __str__(self):
        lst=[self.RGBA,self.pos,self,rad]
        return lst.__str__()


class Population():
    def __init__(self, pop, parent,fitVal):
        self.pop=pop
        self.fitVal=fitVal
        
    def __str__(self):
        lst=[self.pop,self.gen,self.fitVal]
        return lst.__str__()
    
        
    
class Evolve():
    def __init__(self, filename,n):
        #the image you want to approximate
        self.imgName=filename
        self.img=Image.open(filename)
        #stores size of the image
        width,height= self.img.size
        self.size=(width,height)
        #pygame screen 
        self.Screen=Screen(self.size)
        #the generation count
        self.genCount=0
        #population of the current generation, would be a list of chromosomes
        self.pops=[]
        #current population image
        self.genImg=None
        #no. of circles
        self.nCircle=n
        #offsprings
        self.offsprings=[]

    def addFitter(self,lst,p):
        """ makes sure that the fitter population is always at 0th index
            arguments:
                    1- lst: the list which needs to be operated on
                    2- p: the object that needs to be added
        """
        if len(lst)<1 or lst[0].fitVal>p.fitVal:
            lst.append(p)
        else:
            lst.insert(0,p)
            
    def generatePopulation(self):
        """generates random population"""
        
        if len(self.pops)>=2 :   #function should not work if there is no screen
            return False
        #computing radius for the circles
        ScreenArea=self.size[0]*self.size[1]
        CircleArea=ScreenArea/self.nCircle
        radius=int(np.sqrt(CircleArea/np.pi))
        #flags for colors
        black,white=0,1

        pop=[]
        for i in range(self.nCircle):
            #randomly choosing color for each circle/chromosome
            color=random.randint(black,white)
            #default color is black
            rgb=BLACK
            if color==white:
                rgb=WHITE
            #random selection of genes
            alpha=random.randint(0,255)
            posX=random.randint(0,self.size[0])
            posY=random.randint(0,self.size[1])
            #creating a new chromosome
            newChromo=Chromosome(rgb,(posX,posY),alpha,radius)
            pop.append(newChromo)
        self.Screen.setScreen()
        if self.Screen.DrawPop(pop,self.genCount):
            fitVal=self.fitness()
            if fitVal==-1:
                raise ValueError("No final image exists!")
            else:
                tempPop=Population(pop,fitVal)
                self.addFitter(self.pops,tempPop)
        else:
            raise ValueError("Population not drawn!")
        return True

    def fitness(self):
        """calculates fitness of a population"""
        
        im1=self.img
        im2=Image.open("gen" +str(self.genCount)+".jpg")
##        im2=self.genImg
        #if any of the images do not exis, the function doesn't work
        if im1==None or im2==None:
            return -1
        #computing the absolute pixel difference in both images and storing its ,histogram
        hist = ImageChops.difference(im1, im2).histogram()
        #calculating rms
        meanSquare=map(lambda h, i: h*(i**2), hist, range(len(hist)))
        rms= np.sqrt(functools.reduce(operator.add,meanSquare) / (float(self.size[0]) * self.size[1]))
        return rms

    def select(self):
        """ selects the fittest populations"""
        
        i=j=0
        selectedPop=[]
        while len(selectedPop)<2:
            if self.pops[i].fitVal>self.offsprings[j].fitVal:
                addFitter(selectedPop,self.pops[i])
                i+=1
            else:
                addFitter(selectedPop,self.offsprings[j])
                j+=1
        self.pops=selectPop
        self.offsprings=[]

    def select(self):
        """ single parent vs daughter"""
        self.pops.pop()     #removes the less fitter population
    
    def crossover(self,r):
        """ creates new offsprings using crossover at point r"""
        
        crossover_point=(self.nCircle)/r
        child1=self.pops[0][:crossover_point]+self.pops[1][crossover_point:]
        child2=self.pops[1][:crossover_point]+self.pops[0][crossover_point:]
        self.offsprings=[child1,child2]


    def mutate(self):
        """ after mutation,
            1- temporary store the offsprings in another list,
            2- calculate fitness of each population
                (you will need to draw the population first, its an issue which we can deal with later)
            3- re-add them in self.offsprings using addFitter()
            """
        
        pass
    
    def evolve(self):
        pass
    


test=Evolve('test.jpg',100)
test.generatePopulation()
##test.DrawPop()
##fitVal=test.fitness()
##print(fitVal)

