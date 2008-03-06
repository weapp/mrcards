#!/usr/bin/python
import pygame
import gtk
import pygtk
if __name__ == "__main__":
    img=pygame.image.load("blanca.png")
    rect_blanca = img.get_rect()
    
    pos_suit=(13,34)
    pos_num=(13,17)
    
        
    suits=("a","b","c","d")
    for j in range(4):    
        for i in range(12):
            z=i+1
            
            #img2=pygame.image.load(str(suits[j])+".png")
            #rect = img2.get_rect()
            #rect.center=pos_suit
            #img.blit(img2, rect)
            #rect.center=(rect_blanca[2]-pos_suit[0],rect_blanca[3]-pos_suit[1])
            #img.blit(pygame.transform.rotozoom(img2, 3*180, 1), rect)
            
            img=pygame.image.load("blanca.png")
            
            img3=pygame.image.load(suits[j]+".png")
            rect = img3.get_rect()
            rect.center=pos_suit
            
            img.blit(img3, rect)
            rect.center=(rect_blanca[2]-pos_suit[0],rect_blanca[3]-pos_suit[1])
            img.blit(pygame.transform.rotozoom(img3, 3*180, 1), rect)
        
            
            img3=pygame.image.load(str(z)+".png")
            rect = img3.get_rect()
            rect.center=pos_num
            
            img.blit(img3, rect)
            rect.center=(rect_blanca[2]-pos_num[0],rect_blanca[3]-pos_num[1])
            img.blit(pygame.transform.rotozoom(img3, 3*180, 1), rect)
        
            pygame.image.save(img,str(suits[j])+" "+str(z)+".tga",)


    img=pygame.image.load("__.png")
    pygame.image.save(img,"00.tga")
    
