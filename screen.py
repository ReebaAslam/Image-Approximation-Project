import pygame


class Screen():
    def __init__(self, size):
        pygame.display.init()
        self.size=size
        self.screen=None
        #surface for transparency
        self.surface=pygame.Surface(self.size,pygame.SRCALPHA)
        
    def setScreen(self):
        #initializing display
        pygame.display.init()
        if pygame.display.get_init():
            #setting up the screen
            self.screen=pygame.display.set_mode(list(self.size))
            self.screen.fill(WHITE)     #white background
            self.screen.blit(self.surface,(0,0))    #blitting the transparent surface
            pygame.display.update() #updating screen

    def DrawPop(self, pop, gen):
        if not pygame.display.init():
            return False
        #Loop until the user clicks the close button.
        done = False
##        clock = pygame.time.Clock()
        i=0
        while i<len(pop):
     
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
##            clock.tick(10)
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
            #chromosomes in population are drawn
            if i<len(pop):
                chromo=pop[i]
                pygame.draw.circle(self.surface,chromo.RGBA,chromo.pos,chromo.rad,0)
            elif i==len(pop):
                #screen is updated once all the population has been drawn on the surface
                self.screen.blit(self.surface,(0,0))
                pygame.display.update()
            i+=1
        #image is saved only when all of the population has been drawn       
##        if i>=len(pop):
        imgName="gen#"+str(gen)+".jpg"
        pygame.image.save(self.screen, imgName)
        pygame.display.quit()
        return True
