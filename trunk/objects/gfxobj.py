from library.stdmodules import module
from library import core
import pygame

class gfxobj(pygame.sprite.Sprite, module.Module):
    def __init__(self, name, func):
        module.Module.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        f = pygame.font.Font("data/font.ttf", 40)
        self.image = f.render(name, True, (255, 125, 0))
        self.image2 = f.render(name, True, (255, 200, 125))
        self.rect = self.image.get_rect()
        self.func = func
        
        self.g = pygame.sprite.Group()
        self.g.add(self)
        
        self.bind( "hover", self.change, self.change2 )
        self.bind( "click", self.onclick )
        self.bind( "click", self.onclick2, self.onclick3 )
    
    def change(self, *args):
        print "on hover"
        self.image, self.image2 = self.image2, self.image
    
    def change2(self, *args):
        print "off hover"
        self.image, self.image2 = self.image2, self.image
    
    def onclick(self, *args):
        print "click"
        #core.core.get_app()['SceneManager'].change_scene(self.func)
    
    def onclick2(self, *args):
        print "click2"
        #core.core.get_app()['SceneManager'].change_scene(self.func)
    
    def onclick3(self, *args):
        print "click3"
        core.core.get_app()['SceneManager'].change_scene(self.func)
        
    def update(self):
        self.g.draw(core.core.video.get_screen())
        

