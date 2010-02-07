import pygame

class Video:
    def __init__(self):
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
        self.size = map(lambda x:int(x/1.5) , pygame.display.list_modes()[0] )

        #SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 860
        #(640,480))#TODO cambiar (esta asi para que me entre en la pantalla

    
    def get_screen(self):
        self.__make_screen()
        return self.__screen

    def set_size(self, size):
        self.size = size
        if hasattr(self,'_Video__screen'):
            self.__screen = pygame.display.set_mode(self.size, self.flags)

    def __make_screen(self):
        if not hasattr(self,'_Video__screen'):
            self.__screen = pygame.display.set_mode(self.size, self.flags)

    def init_video(self):
        if not hasattr(self,'_Video__screen'):
            pygame.display.set_mode(self.__size, self.flags)
    
    def update(self):
        self.__make_screen()
        pygame.display.flip()
