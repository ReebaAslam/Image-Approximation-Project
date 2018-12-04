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
POPULATION_SIZE=10


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
            mutation_size = max(1, int(round(random.gauss(40, 4)))) / 100
            prop = np.random.randint(0, 3)
            if prop == 0:
                color_r = min(max(0, random.randint(int(self.RGBA[0] * (1 - mutation_size)),
                                              int(self.RGBA[0] * (1 + mutation_size)))), 255)
                color_g = min(max(0, random.randint(int(self.RGBA[1] * (1 - mutation_size)),
                                          int(self.RGBA[1] * (1 + mutation_size)))), 255)
                color_b = min(max(0, random.randint(int(self.RGBA[2] * (1 - mutation_size)),
                                          int(self.RGBA[2] * (1 + mutation_size)))), 255)
                alpha = min(max(50, random.randint(int(self.RGBA[3] * (1 - mutation_size)),
                                          int(self.RGBA[3] * (1 + mutation_size)))), 255)

                self.RGBA = (color_r, color_g, color_b, alpha)
            elif prop == 1:
                # mutate position
##                x = max(0, random.randint(int(self.pos[0] * (1 - mutation_size)), int(self.pos[0] * (1 + mutation_size))))
##                y = max(0, random.randint(int(self.pos[1] * (1 - mutation_size)), int(self.pos[1] * (1 + mutation_size))))
                x=random.randint(min(0,self.pos[0]),size[0])
                y=random.randint(min(0,self.pos[1]),size[1])
                self.pos = (x, y)
            else:
                self.rad = max(self.rad,
                               random.randint(int(self.rad * (1 - mutation_size)), min(int(self.rad * (1 + mutation_size)),size[0] // 5)))

class Population:
    def __init__(self, img, fitVal):
        self.image = img
        self.fitVal = fitVal
        self.pop=img.pop

    def __str__(self):
        # lst = [self.pop, self.gen, self.fitVal]
        lst = [self.pop, self.fitVal]
        return lst.__str__()


def sort(lst):
    return sorted(lst,key=lambda x: x.fitVal)


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
        self.maxFitness=0
        self.avgFitness=0


    def howFit(self):
        self.maxFitness=self.pops[0].fitVal
        self.avgFitness=sum(pop.fitVal for pop in self.pops)/POPULATION_SIZE
        
    def generatePopulation(self):
        """generates random population"""

        if len(self.pops) >= POPULATION_SIZE:  # function should not work if there is no screen
            return False
        population = []
        for k in range(POPULATION_SIZE):
            p = []
            for i in range(self.nCircle):
                # random selection of genes
                posX = random.randint(0, self.size[0])
                posY = random.randint(0, self.size[1])
                rad = random.randint(10, self.size[0] // 5)
                rgba=(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
                # creating a new chromosome
                newChromo = Chromosome( rad ,(posX,posY),rgba)
                p.append(newChromo)
            drawPop=drawImage(p,self.size)
            image=drawPop.generateImage()
            fitVal=self.fitness(image)
            if fitVal == -1:
                raise ValueError("No final image exists!")
            else:
                p = Population(drawPop, fitVal)
            population.append(p)
        self.pops=sort(population)
        self.howFit()
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
        pix=np.sqrt(functools.reduce(operator.add,
                         list(map(lambda h, i: h*(i**2),
                             hist, list(range(256))*3))) /
                            (float(self.size[0]) * self.size[1]))
##        # calculating rms
##        sqr = (val*(i**2) for i, val in enumerate(hist))
##        sum_of_squares = sum(sqr)
##        rms = np.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
##        return rms
        i1 = np.array(im1,np.int16)
        i2 = np.array(im2,np.int16)
        dif = np.sum(np.abs(i1-i2))
        pos=(dif / 255.0 * 100) / i1.size
        return pix+pos
    

    def select(self):
        """ selects the fittest populations"""
        selectedPop = self.pops+self.offsprings
        winners=sort(selectedPop)
        self.pops = winners[0:POPULATION_SIZE//2]
        left=winners[POPULATION_SIZE//2:]
        for i in range(POPULATION_SIZE-POPULATION_SIZE//2):
            ind=random.choice(left)
            left.remove(ind)
            self.pops.append(ind)
        self.howFit()
        self.offsprings = []
        if self.genCount in [0,100,500] or self.genCount%1000==0:
            image=self.pops[0].image
            image.saveImage(self.genCount)


    def crossover1(self, r):
     """ creates new offsprings using crossover at point r"""
##     crossover_point = min(self.nCircle - 1, int((self.nCircle) / r))
     crossover_point=int(self.nCircle*r)
     # crossover_point=(self.nCircle)/r
     i=0
     j=0
     parents=self.pops[:]
     childCount=0
     while childCount<POPULATION_SIZE and len(parents)>1:
         father=random.choice(parents)
         parents.remove(father)
         mother=random.choice(parents)
         parents.remove(mother)
         child1=father.pop[:crossover_point] + mother.pop[crossover_point:]
         child2 = mother.pop[:crossover_point] + father.pop[crossover_point:]
         self.offsprings.append(child1)
         self.offsprings.append(child2)
         childCount+=2

    def crossover2(self, r1,r2):
     """ creates new offsprings using crossover at point r"""
##     crossover_point = min(self.nCircle - 1, int((self.nCircle) / r))
     if r2<r1:
         crossover_point1=int(self.size[0]*r2)
         crossover_point2=int(self.size[0]*r1)
     else:
         crossover_point1=int(self.size[0]*r1)
         crossover_point2=int(self.size[0]*r2)
     # crossover_point=(self.nCircle)/r
     parents=self.pops[:]
     childCount=0
     while childCount<POPULATION_SIZE and len(parents)>1:
         father=random.choice(parents)
         parents.remove(father)
##         father.pop=sorted(father.pop,key=lambda x: x.pos[1])
         mother=random.choice(parents)
         parents.remove(mother)
##         mother.pop=sorted(mother.pop,key=lambda x: x.pos[1])
         child1=[chromo for chromo in father.pop if chromo.pos[0]<crossover_point1 or chromo.pos[0]>crossover_point2 ]+[
                chromo for chromo in mother.pop if chromo.pos[0]>=crossover_point1 and chromo.pos[0]<=crossover_point2 ]

         child2=[chromo for chromo in mother.pop if chromo.pos[0]<crossover_point1 or chromo.pos[0]>crossover_point2 ]+[
                chromo for chromo in father.pop if chromo.pos[0]>=crossover_point1 and chromo.pos[0]<=crossover_point2 ]
         self.offsprings.append(child1[:self.nCircle])
         self.offsprings.append(child2[:self.nCircle])
         childCount+=2

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
                sample=random.sample(p,int(len(p)*0.5))
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
                self.offsprings.append(tempPop)

    def evolve(self):
        global MUTATE_CHANCE
        print('gen #: {} fitness: {}, {}'.format(str(self.genCount), str(self.maxFitness), str(self.avgFitness)))
        while True:
##            for i in range(500):
            self.crossover2(random.uniform(0,1),random.uniform(0,1))
##            self.crossover1(random.uniform(0,1))
            self.mutate()
            self.genCount += 1
            self.select()
            if self.genCount%20==0:
                print('gen #: {} fitness: {}, {}'.format(str(self.genCount), str(self.maxFitness), str(self.avgFitness)))
##            MUTATE_CHANCE*=0.8

test = Evolve('firefox.png', 50)
test.generatePopulation()
test.evolve()
##test.DrawPop()
##fitVal=test.fitness()
##print(fitVal)
