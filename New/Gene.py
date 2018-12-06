import random


WIDTH_PROP=2
class Gene:
    def __init__(self,size):
        self.pos1=(random.randint(0,size[0]),random.randint(0,size[1]))
        self.pos2=(random.randint(0,size[0]),random.randint(0,size[1]))
        self.pos3=(random.randint(0,size[0]),random.randint(0,size[1]))
        #self.rad=random.randint(20,size[0]//WIDTH_PROP)
        self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.ImageSize= size
        
    def gene_mutate(self):
        pass
