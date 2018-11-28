from PIL import Image, ImageChops
import numpy as np
import random
import functools, operator
from screen import Screen

# some standard colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MUTATE_CHANCE = 0.1


# A chromosome object is the basic unit of the population made up of genes
class Chromosome:
    def __init__(self, color=BLACK, pos=(0, 0), alpha=255, rad=0):
        # genes
        self.RGBA = tuple(list(color) + [alpha])
        self.pos = pos
        self.rad = rad

    def __str__(self):
        lst = [self.RGBA, self.pos, self.rad]
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
                self.rad = max(1,
                               random.randint(int(self.rad * (1 - mutation_size)), int(self.rad * (1 + mutation_size))))


class Population:
    def __init__(self, pop, fitVal):
        self.pop = pop
        self.fitVal = fitVal

    def __str__(self):
        # lst = [self.pop, self.gen, self.fitVal]
        lst = [self.pop, self.fitVal]
        return lst.__str__()


class Evolve:
    def __init__(self, filename, n):
        # the image you want to approximate
        self.imgName = filename
        self.img = Image.open(filename)
        # stores size of the image
        width, height = self.img.size
        self.size = (width, height)
        # pygame screen
        self.Screen = Screen(self.size)
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
            # #computing radius for the circles
            # ScreenArea=self.size[0]*self.size[1]
            # CircleArea=ScreenArea/self.nCircle
            # radius=int(np.sqrt(CircleArea/np.pi))
            # #flags for colors
        population = []
        for k in range(2):
            p = []
            for i in range(self.nCircle):
                # randomly choosing color for each circle/chromosome
                ##                color = random.randint(black, white)
                # default color is black
                ##                rgb = BLACK
                ##                if color == white:
                ##                    rgb = WHITE
                # random selection of genes
                alpha = random.randint(0, 255)
                posX = random.randint(0, self.size[0])
                posY = random.randint(0, self.size[1])
                radius = random.randint(0, self.size[0] // 8)
                rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                # creating a new chromosome
                newChromo = Chromosome(rgb, (posX, posY), alpha, radius)
                p.append(newChromo)
            population.append(p)
        for pop in population:
            self.Screen.setScreen()
            if self.Screen.DrawPop(pop, self.genCount):
                fitVal = self.fitness()
                if fitVal == -1:
                    raise ValueError("No final image exists!")
                else:
                    tempPop = Population(pop, fitVal)
                    self.addFitter(self.pops, tempPop)
            else:
                raise ValueError("Population not drawn!")
        self.fit = (self.pops[0].fitVal, self.pops[1].fitVal)
        return True

    def fitness(self):
        """calculates fitness of a population"""

        im1 = self.img
        im2 = Image.open("gen#" + str(self.genCount) + ".jpg")
        ##        im2=self.genImg
        # if any of the images do not exis, the function doesn't work
        if im1 == None or im2 == None:
            return -1
        # computing the absolute pixel difference in both images and storing its ,histogram
        hist = ImageChops.difference(im1, im2).histogram()
        # calculating rms
        meanSquare = map(lambda h, i: h * (i ** 2), hist, range(len(hist)))
        rms = np.sqrt(functools.reduce(operator.add, meanSquare) / (float(self.size[0]) * self.size[1]))
        return rms

    def select(self):
        """ selects the fittest populations"""

        i = j = 0
        selectedPop = []
        while len(selectedPop) < 2:
            if self.pops[i].fitVal < self.offsprings[j].fitVal:
                self.addFitter(selectedPop, self.pops[i])
                i += 1
            else:
                self.addFitter(selectedPop, self.offsprings[j])
                j += 1
        self.pops = selectedPop
        self.offsprings = []
        self.fit = (self.pops[0].fitVal, self.pops[1].fitVal)
        self.Screen.setScreen()
        self.Screen.DrawPop(self.pops[0].pop, self.genCount + 1)

    #    def select(self):
    #        """ single parent vs daughter"""
    #        self.pops.pop()     #removes the less fitter population

    def crossover(self, r):
        """ creates new offsprings using crossover at point r"""

        crossover_point = min(self.nCircle - 1, int((self.nCircle) / r))
        # crossover_point=(self.nCircle)/r
        child1 = self.pops[0].pop[:crossover_point] + self.pops[1].pop[crossover_point:]
        child2 = self.pops[1].pop[:crossover_point] + self.pops[0].pop[crossover_point:]
        # child1=self.pops[0][:crossover_point]+self.pops[1][crossover_point:]
        # child2=self.pops[1][:crossover_point]+self.pops[0][crossover_point:]
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
                for g in p:
                    g.gene_mutate(self.size)
        children = self.offsprings[:]
        self.offsprings = []
        for pop in children:
            self.Screen.setScreen()
            if self.Screen.DrawPop(pop, self.genCount + 1):
                fitVal = self.fitness()
                if fitVal == -1:
                    raise ValueError("No final image exists!")
                else:
                    tempPop = Population(pop, fitVal)
                    self.addFitter(self.offsprings, tempPop)
            else:
                raise ValueError("Population not drawn!")

    def evolve(self):
        while True:
            self.crossover(np.random.randint(1, max(2, len(self.pops))))
            self.mutate()
            self.select()
            self.genCount += 1
            print('gen #: {} fitness: {}'.format(str(self.genCount), str(self.fit)))


test = Evolve('test.jpg', 100)
test.generatePopulation()
test.evolve()
##test.DrawPop()
##fitVal=test.fitness()
##print(fitVal)
