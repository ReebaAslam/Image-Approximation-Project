import random


WIDTH_PROP=2
class GeneT:
    def __init__(self,size):
        self.pos1=(random.randint(0,size[0]),random.randint(0,size[1]))
        self.pos2=(random.randint(0,size[0]),random.randint(0,size[1]))
        self.pos3=(random.randint(0,size[0]),random.randint(0,size[1]))
        #self.rad=random.randint(20,size[0]//WIDTH_PROP)
        self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.ImageSize= size
        self.type='Triangle'
        
    def gene_mutate(self,rate):
        if rate<=random.random():
            change=random.randint(0,3)
            if change==0:
                self.pos1=(random.randint(0,size[0]),random.randint(0,size[1]))
            elif change==1:
                self.pos2=(random.randint(0,size[0]),random.randint(0,size[1]))
            elif change==2:
                self.pos3=(random.randint(0,size[0]),random.randint(0,size[1]))
            else:
                self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))                

class GeneC:
    def __init__(self,size):
        self.pos=(random.randint(0,size[0]),random.randint(0,size[1]))
        self.rad=random.randint(20,size[0]//WIDTH_PROP)
        self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.ImageSize= size
        self.type='Circle'
        
    def gene_mutate(self,rate):
        if rate<=random.random():
            change=random.randint(0,2)
            if change==0:
                self.pos=(random.randint(0,size[0]),random.randint(0,size[1]))
            elif change==1:
                self.rad=random.randint(20,size[0]//WIDTH_PROP)
            else:
                self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
