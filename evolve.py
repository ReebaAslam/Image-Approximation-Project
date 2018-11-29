from PIL import Image, ImageChops
import numpy as np
import random
import functools, operator
from DrawImage import drawImage

# some standard colors
WHITE = (255, 255, 255,255)
BLACK = (0, 0, 0,255)
RED = (255, 0, 0,255)
GREEN = (0, 255, 0,255)
BLUE = (0, 0, 255,255)

MUTATE_CHANCE = 0.1


# A chromosome object is the basic unit of the population made up of genes
class Chromosome:
    def __init__(self,rad,pos=(0,0),color=BLACK):
        # genes
        self.RGBA = color
        self.pos = pos
        self.rad=rad

    def __str__(self):
        lst = [self.RGBA, self.pos1, self.rad]
        return lst.__str__()

    def gene_mutate(self, size):
        mutate = False
        if MUTATE_CHANCE >= np.random.random():
            mutate = True
        if mutate:
            mutation_size = max(1, int(round(random.gauss(15, 4)))) / 100
            prop = np.random.randint(0, 3)
            if prop == 0:
                color_r = min(max(0, random.randint(int(self.RGBA[0] * (1 - mutation_size)),
                                              int(self.RGBA[0] * (1 + mutation_size)))), 255)
                color_g = min(max(0, random.randint(int(self.RGBA[1] * (1 - mutation_size)),
                                          int(self.RGBA[1] * (1 + mutation_size)))), 255)
                color_b = min(max(0, random.randint(int(self.RGBA[2] * (1 - mutation_size)),
                                          int(self.RGBA[2] * (1 + mutation_size)))), 255)
                alpha = min(max(0, random.randint(int(self.RGBA[3] * (1 - mutation_size)),
                                          int(self.RGBA[3] * (1 + mutation_size)))), 255)

                self.RGBA = (color_r, color_g, color_b, alpha)
            elif prop == 1:
                # mutate position
                x = max(0, random.randint(int(self.pos[0] * (1 - mutation_size)), int(self.pos[0] * (1 + mutation_size))))
                y = max(0, random.randint(int(self.pos[1] * (1 - mutation_size)), int(self.pos[1] * (1 + mutation_size))))
                self.pos = (x, y)
            else:
                self.rad = max(self.rad,
                               random.randint(int(self.rad * (1 - mutation_size)), int(self.rad * (1 + mutation_size))))

class Population:
    def __init__(self, img, fitVal):
        self.image = img
        self.fitVal = fitVal
        self.pop=img.pop

    def __str__(self):
        # lst = [self.pop, self.gen, self.fitVal]
        lst = [self.pop, self.fitVal]
        return lst.__str__()


class Evolve:
    def __init__(self, filename, n):
        # the image you want to approximate
        self.imgName = filename
        self.img = Image.open(filename).convert('RGB')
        # stores size of the image
        width, height = self.img.size
        self.size = (width, height)
        # the generation count
        self.genCount = 0
        # population of the current generation, would be a list of chromosomes
        self.pops = []
        # current population image
        self.genImg = None
        # no. of circles
        self.nCircle = n
        # offsprings
        self.offsprings = []
        self.fit = []


    def addFitter(self, lst, p):
        """ makes sure that the fitter population is always at 0th index
            arguments:
                    1- lst: the list which needs to be operated on
                    2- p: the object that needs to be added
        """
        if len(lst) < 1 or lst[0].fitVal < p.fitVal:
            lst.append(p)
        else:
            lst.insert(0, p)

    def generatePopulation(self):
        """generates random population"""

        if len(self.pops) >= 2:  # function should not work if there is no screen
            return False
        population = []
        for k in range(2):
            p = []
            for i in range(self.nCircle):
                # random selection of genes
                posX = random.randint(0, self.size[0])
                posY = random.randint(0, self.size[1])
                rad = random.randint(0, self.size[0] // 5)
                rgba=(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
                # creating a new chromosome
                newChromo = Chromosome( rad ,(posX,posY),rgba)
                p.append(newChromo)
            population.append(p)
        for pop in population:
            drawPop=drawImage(pop,self.size)
            image=drawPop.generateImage()
            fitVal=self.fitness(image)
            if fitVal == -1:
                raise ValueError("No final image exists!")
            else:
                tempPop = Population(drawPop, fitVal)
                self.addFitter(self.pops, tempPop)
        self.fit = (self.pops[0].fitVal, self.pops[1].fitVal)
        self.pops[0].image.saveImage(0)
        return True

    def fitness(self,img):
        """calculates fitness of a population"""

        im1 = self.img
        im2 = img
        ##        im2=self.genImg
        # if any of the images do not exis, the function doesn't work
        if im1 == None or im2 == None:
            return -1
        # computing the absolute pixel difference in both images and storing its ,histogram
        hist = ImageChops.difference(im1, im2).histogram()
        # calculating rms
        sqr = (val*(i**2) for i, val in enumerate(hist))
        sum_of_squares = sum(sqr)
        rms = np.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
        return rms
##        i1 = np.array(im1,np.int16)
##        i2 = np.array(im2,np.int16)
##        dif = np.sum(np.abs(i1-i2))
##        return (dif / 255.0 * 100) / i1.size
    

    def select(self):
        """ selects the fittest populations"""

        i = j = 0
        selectedPop = self.pops+self.offsprings
        winners=sorted(selectedPop, key=lambda x: x.fitVal)
        self.pops = winners[0:2]
        self.offsprings = []
        self.fit = (self.pops[0].fitVal, self.pops[1].fitVal)
        if self.genCount in [0,100,500] or self.genCount%1000==0:
            image=self.pops[0].image
            image.saveImage(self.genCount)
            print("image # " +str(self.genCount))

    #    def select(self):
    #        """ single parent vs daughter"""
    #        self.pops.pop()     #removes the less fitter population

    def crossover(self, r):
     """ creates new offsprings using crossover at point r"""
##     crossover_point = min(self.nCircle - 1, int((self.nCircle) / r))
     if r<0.5:
         r=1-r
     crossover_point=int(self.nCircle*r)
     # crossover_point=(self.nCircle)/r
     child1 = self.pops[0].pop[:crossover_point] + self.pops[1].pop[crossover_point:]
     child2 = self.pops[1].pop[:crossover_point] + self.pops[0].pop[crossover_point:]
     self.offsprings = [child1, child2]

    def mutate(self):
        """ after mutation,
            1- temporary store the offsprings in another list,
            2- calculate fitness of each population
                (you will need to draw the population first, its an issue which we can deal with later)
            3- re-add them in self.offsprings using addFitter()
            """

        for p in self.offsprings:
            # each offspring has a random choice of mutating
            if MUTATE_CHANCE >= np.random.random():
                sample=random.sample(p,int(self.nCircle*0.5))
                for g in sample:
                    g.gene_mutate(self.size)
        children = self.offsprings[:]
        self.offsprings = []
        for pop in children:
            drawPop=drawImage(pop,self.size)
            image=drawPop.generateImage()
            fitVal=self.fitness(image)
            if fitVal == -1:
                raise ValueError("No final image exists!")
            else:
                tempPop = Population(drawPop, fitVal)
                self.addFitter(self.offsprings, tempPop)

    def evolve(self):
        while True:
            self.crossover(random.randrange(0,1))
##            self.crossover(0.7)
            self.mutate()
            self.genCount += 1
            self.select()
            print('gen #: {} fitness: {}'.format(str(self.genCount), str(self.fit)))


test = Evolve('download.png', 50)
test.generatePopulation()
test.evolve()
##test.DrawPop()
##fitVal=test.fitness()
##print(fitVal)
