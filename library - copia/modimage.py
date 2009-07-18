from images import getImage 
import module
import pygame

class ModuleImage (module.Module):
    def __init__(self,surface,image="None",position=(0,0)):
        module.Module.__init__(self)
        self.player=getImage(image)
        self.surface=surface
        self.position = self.player.get_rect().move(*position)
        self.need_update.append(self.player.get_rect())
        
    def draw(self,rect):
        pos_image=self.player.get_rect().move(self.position[0],self.position[1])
        clip=rect.move(-pos_image[0],-pos_image[1])
        self.surface.blit(self.player, rect, clip)
        self.need_update=[]
