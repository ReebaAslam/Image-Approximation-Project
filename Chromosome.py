from Gene import GeneC, GeneT
from PIL import Image, ImageChops
from DrawImage import DrawImage
import numpy as np
from functools import reduce
import operator


##class Chromosome:
##    def __init__(self,image,n,size):
##        self.nCircles=n
##        self.target=image
##        self.size=size
##        self.genes=self.GenerateGenes(self.size)
##        self.image=DrawImage(self.genes,self.size)
##        self.fitness=self.howFit()
class Chromosome:
    def __init__(self, image, n, size=None,type='Circle'):
        self.nCircles = n
        self.target = image
        self.size = size
        self.type = type
        if size:
            self.genes = self.GenerateGenes(self.size)
            self.image = DrawImage(self.genes, self.size)
            self.fitness = self.howFit()

    def GenerateGenes(self, size):
        genes = []
        for i in range(self.nCircles):
            if self.type == 'Circle':
                genes.append(GeneC(size))
            else:
                genes.append(GeneT(size))
        return genes

    def howFit(self):
        #https://github.com/DING-PENG/image-approx
        #https://github.com/Keilan/pyointillism
        image = self.image.generateImage()
        i1 = np.array(self.target, np.int16)
        i2 = np.array(image, np.int16)
        dif = np.sum(np.abs(i1 - i2))
        pos = (dif / 255.0 * 100) / i1.size
        h = ImageChops.difference(self.target, image).histogram()
        pix = np.sqrt(reduce(operator.add,
                             list(map(lambda h, i: h * (i ** 2),
                                      h, list(range(256)) * 3))) /
                      (float(self.size[0]) * self.size[1]))
        return pix + pos

    def copy(self, chromo):
        self.nCircles = chromo.nCircles
        self.target = chromo.target
        self.size = chromo.size
        self.genes = chromo.genes[:]
        self.image = chromo.image
        self.fitness = chromo.fitness
