from Chromosome import Chromosome
from PIL import Image,ImageChops
from DrawImage import DrawImage
from Gene import Gene
import random

image=Image.open('firefox.png').convert('RGB')
size=image.size
mutate_rate=0.5
POP_SIZE=5

def InitialPopulation():
    chromos=[]
    for i in range(50):
        chromos.append(Chromosome(image,1,size))
    chromos=sorted(chromos,key=lambda x: x.fitness)
    fit=chromos[0]
    for n in range(50):
        chromos=[]
        for i in range(50):
            temp=Chromosome(image,1,size)
            temp.copy(fit)
            temp.genes.append(Gene(size))
            temp.nCircles+=1
            temp.image=DrawImage(temp.genes,temp.size)
            temp.fitness=temp.howFit()
            chromos.append(temp)
        chromos=sorted(chromos,key=lambda x: x.fitness)
        fit=chromos[0]
    return fit

def mutate(children):
    pop=[]
    for i in range(len(children)):
        for j in range(len(children[i].genes)):
            if mutate_rate>=random.random():
                gene=Gene(size)
                children[i].genes[j]=gene
        children[i].image=DrawImage(children[i].genes,children[i].size)
        children[i].fitness=children[i].howFit()
        pop.append(children[i])
    return pop

def select(pop,n):
    pop=sorted(pop,key=lambda x: x.fitness)
    fit=pop[0]
    if n%20==0:
        print("gen#"+str(n)+" - ",fit.fitness)
    if n in [0,100,500] or n%1000==0:
        fit.image.saveImage(n)
    return fit,pop

def evolve():
    global mutate_rate
    initial=[]
    for i in range(POP_SIZE):
        print("generating initial population")
        initial.append(InitialPopulation())
    fittest,initial=select(initial,0)
    parents=initial[:POP_SIZE//2]
    gen=1     
    while True:
        for i in range(100):
            children=[]
            while len(parents)>1:
                p1=random.choice(parents)
                parents.remove(p1)
                p2=random.choice(parents)
                crossover(p1,p2,children)
            pop=mutate(children)
            fittest,parents=select(pop,gen)
            parents=parents[:POP_SIZE//2]
            gen+=1
        mutate_rate*=0.8
        
def crossover(parent1,parent2,children):
    r=random.random()
    cp=int(size[0]*r)
    child1=[gene for gene in parent1.genes if gene.pos[0]<=cp]+[gene for gene in parent2.genes if gene.pos[0]>cp]
    child2=[gene for gene in parent2.genes if gene.pos[0]<=cp]+[gene for gene in parent1.genes if gene.pos[0]>cp]
    temp1=Chromosome(image,len(child1),size)
    temp1.genes=child1
    children.append(temp1)
    temp2=Chromosome(image,len(child2),size)
    temp2.genes=child2
    children.append(temp2)

    
