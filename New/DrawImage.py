##import pygame
from PIL import Image, ImageDraw

#some standard colors     
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

class DrawImage:
    def __init__(self,pop,size):
        self.pop=pop
        self.size=size
        self.image=self.generateImage()

    def generateImage(self):
        im = Image.new('RGB', self.size, WHITE)
        draw = ImageDraw.Draw(im, 'RGBA')
        for chromo in self.pop:
            pos1=(chromo.pos[0]-chromo.rad, chromo.pos[1]-chromo.rad)
            pos2=(chromo.pos[0]+chromo.rad, chromo.pos[1]+chromo.rad)
            draw.ellipse([pos1,pos2],
                         fill=chromo.RGBA, outline=chromo.RGBA)
        del draw
        return im

    def saveImage(self, gen):
        self.image.save("gen# " +str(gen)+'.png')


