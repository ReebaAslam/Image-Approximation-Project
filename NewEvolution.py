from Chromosome import Chromosome
from PIL import Image, ImageChops
from DrawImage import DrawImage
from Gene import GeneC, GeneT
import random

image = Image.open('yellowCircle.png').convert('RGB')
size = image.size
mutate_rate = 0.05
POP_SIZE = 5


def InitialPopulation():
    chromos = []
    for i in range(50):
        # chromos.append(Chromosome(image, 1, size, 'Triangle'))
        chromos.append(Chromosome(image, 1, size, 'Circle'))
    chromos = sorted(chromos, key=lambda x: x.fitness)
    fit = chromos[0]
    for n in range(50):
        chromos = []
        for i in range(50):
            # temp = Chromosome(image, 1, size, 'Triangle')
            temp = Chromosome(image, 1, size)
            chromos.append(Chromosome(image, 1, size, 'Circle'))
            temp.copy(fit)
            temp.genes.append(GeneC(size))
##            temp.genes.append(GeneT(size))
            temp.nCircles += 1
            temp.image = DrawImage(temp.genes, temp.size)
            temp.fitness = temp.howFit()
            chromos.append(temp)
        chromos = sorted(chromos, key=lambda x: x.fitness)
        fit = chromos[0]
    return fit


def mutate(children):
    pop = []
    for i in range(len(children)):
        for j in range(len(children[i].genes)):
            if mutate_rate >= random.random():
                gene = GeneC(size)
##                gene = GeneT(size)
                children[i].genes[j] = gene
        children[i].image = DrawImage(children[i].genes, children[i].size)
        children[i].fitness = children[i].howFit()
        pop.append(children[i])
    return pop


def select(pop, n):
    pop = sorted(pop, key=lambda x: x.fitness)
    fit = pop[0]
    if n % 20 == 0:
        print("gen#" + str(n) + " - ", fit.fitness)
    if n in [0, 100, 500] or n % 1000 == 0:
        fit.image.saveImage(n)
        with open('log.txt', 'w+') as save:
            save.write(str(n) + '\n')
            if pop[0].type == 'Triangle':
                save.write('Triangle\n')
                for i in range(len(pop)):
                    save.write(str(pop[i].nCircles) + '\n')
                    save.write(str(pop[i].size) + '\n')
                    for j in range(len(pop[i].genes)):
                        save.write(str(pop[i].genes[j].pos1) + '\n')
                        save.write(str(pop[i].genes[j].pos2) + '\n')
                        save.write(str(pop[i].genes[j].pos3) + '\n')
                        save.write(str(pop[i].genes[j].RGBA) + '\n')
            else:
                save.write('Circle\n')
                for i in range(len(pop)):
                    save.write(str(pop[i].nCircles) + '\n')
                    save.write(str(pop[i].size) + '\n')
                    for j in range(len(pop[i].genes)):
                        save.write(str(pop[i].genes[j].pos) + '\n')
                        save.write(str(pop[i].genes[j].rad) + '\n')
                        save.write(str(pop[i].genes[j].RGBA) + '\n')
    return fit, pop


##def evolve():
##    global mutate_rate
##    initial=[]
##    for i in range(POP_SIZE):
##        print("generating initial population")
##        initial.append(InitialPopulation())
##    fittest,initial=select(initial,0)
##    parents=initial[:POP_SIZE//2]
##    gen=1
def evolve(load=False):
    global mutate_rate
    if not load:
        initial = []
        for i in range(POP_SIZE):
            print("generating initial population")
            initial.append(InitialPopulation())
        fittest, initial = select(initial, 0)
        parents = initial[:POP_SIZE // 2]
        gen = 1
    else:
        with open('log.txt', 'r') as f:
            gen = int(f.readline().strip('\n'))
            type = f.readline().strip('\n')
            line = f.readline()
            parents = []
            while line:
                n = int(line.strip('\n'))
                size = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                if type == 'Triangle':
                    temp = Chromosome(image, n, type='Triangle')
                    temp.size = size
                    temp.genes = []
                    for i in range(n):
                        pos1 = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                        pos2 = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                        pos3 = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                        RGBA = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                        gene_temp = GeneT()
                        gene_temp.pos1 = pos1
                        gene_temp.pos2 = pos2
                        gene_temp.pos3 = pos3
                        gene_temp.RGBA = RGBA
                        temp.genes.append(gene_temp)
                else:
                    temp = Chromosome(image, n)
                    temp.size = size
                    temp.genes = []
                    for i in range(n):
                        pos = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                        rad = int(f.readline().strip('\n'))
                        RGBA = tuple([int(x) for x in f.readline().strip('(').strip(')\n').split(',')])
                        gene_temp = GeneC()
                        gene_temp.pos = pos
                        gene_temp.rad = rad
                        gene_temp.RGBA = RGBA
                        temp.genes.append(gene_temp)
                temp.image = DrawImage(temp.genes, temp.size)
                temp.fitness = temp.howFit()
                parents.append(temp)
                line = f.readline()
            fittest = parents[0]
    for i in range(100000):
        children = []
        while len(parents) > 1:
            p1 = random.choice(parents)
            parents.remove(p1)
            p2 = random.choice(parents)
            crossover2(p1, p2, children)
        pop = mutate(children)
        pop.append(fittest)
        fittest, parents = select(pop, gen)
        parents = parents[:POP_SIZE // 2]
        gen += 1


def crossover(parent1, parent2, children):
    r = random.random()
    cp = int(size[0] * r)
    if parent1.genes[0].type == 'triangle':
        child1 = [gene for gene in parent1.genes if
                  gene.pos1[0] <= cp and gene.pos2[0] <= cp and gene.pos3[0] <= cp] + [
                     gene for gene in parent2.genes if gene.pos1[0] > cp and gene.pos2[0] > cp and gene.pos3[0] > cp]
        child2 = [gene for gene in parent2.genes if
                  gene.pos1[0] <= cp and gene.pos2[0] <= cp and gene.pos3[0] <= cp] + [
                     gene for gene in parent1.genes if gene.pos1[0] > cp and gene.pos2[0] > cp and gene.pos3[0] > cp]
        temp1 = Chromosome(image, len(child1), size, 'Triangle')
        temp2 = Chromosome(image, len(child2), size, 'Triangle')
    else:
        child1 = [gene for gene in parent1.genes if gene.pos[0] <= cp] + [gene for gene in parent2.genes if
                                                                          gene.pos[0] > cp]
        child2 = [gene for gene in parent2.genes if gene.pos[0] <= cp] + [gene for gene in parent1.genes if
                                                                          gene.pos[0] > cp]
        temp1 = Chromosome(image, len(child1), size)
        temp2 = Chromosome(image, len(child2), size)
    temp1.genes = child1
    children.append(temp1)
    temp2.genes = child2
    children.append(temp2)


def crossover2(parent1, parent2, children):
    """ creates new offsprings using crossover at a certain point"""
    crossover_point = random.randint(0, len(parent1.genes))
    child1 = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
    child2 = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
    # temp1 = Chromosome(image, len(child1), size, 'Triangle')
    temp1 = Chromosome(image, len(child1), size, 'Circle')
    temp1.genes = child1
    children.append(temp1)
    # temp2 = Chromosome(image, len(child2), size, 'Triangle')
    temp2 = Chromosome(image, len(child2), size,'Circle')
    temp2.genes = child2
    children.append(temp2)


evolve()
