import random

WIDTH_PROP = 2


##class GeneT:
##    def __init__(self,size):
##        self.pos1=(random.randint(0,size[0]),random.randint(0,size[1]))
##        self.pos2=(random.randint(0,size[0]),random.randint(0,size[1]))
##        self.pos3=(random.randint(0,size[0]),random.randint(0,size[1]))
##        self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
##        self.ImageSize= size
##        self.type='Triangle'
##        
##    def gene_mutate(self,rate):
##        if rate<=random.random():
##            change=random.randint(0,3)
##            if change==0:
##                self.pos1=(random.randint(0,self.ImageSize[0]),random.randint(0,self.ImageSize[1]))
##            elif change==1:
##                self.pos2=(random.randint(0,self.ImageSize[0]),random.randint(0,self.ImageSize[1]))
##            elif change==2:
##                self.pos3=(random.randint(0,self.ImageSize[0]),random.randint(0,self.ImageSize[1]))
##            else:
##                self.RGBA=(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))                

class GeneC:
    def __init__(self, size=None):
        if size:
            self.pos = (random.randint(0, size[0]), random.randint(0, size[1]))
            self.rad = random.randint(5, size[0] // WIDTH_PROP)
            self.RGBA = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.pos = None
            self.rad = None
            self.RGBA = None
        self.ImageSize = size
        self.type = 'Circle'


class GeneT:
    def __init__(self, size=None):
        if size:
            self.pos1 = (random.randint(0, size[0]), random.randint(0, size[1]))
            self.pos2 = (random.randint(0, size[0]), random.randint(0, size[1]))
            self.pos3 = (random.randint(0, size[0]), random.randint(0, size[1]))
            self.RGBA = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.pos1 = None
            self.pos2 = None
            self.pos3 = None
            self.RGBA = None
        self.ImageSize = size
        self.type = 'Triangle'
