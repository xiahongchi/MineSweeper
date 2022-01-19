class TwoDimensionArray:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.array=[]
        for i in range(0,x*y):
            self.array.append(0)
    def f(self,x,y):
        if x<=self.x and x>=1 and y<=self.y and y>=1:
            return self.array[self.y*(x-1)+(y-1)]
        else:
            return None
import sys
import pygame
from random import randint
from pygame.sprite import Sprite
class MineSweeper:
    def __init__(self,x,y,mine_num):
        pygame.init()
        self.screen=pygame.display.set_mode((27*x,27*y+27))
        pygame.display.set_caption("MineSweeper")
        self.x=x
        self.y=y
        self.mine_num=mine_num
        self.mine_num_alive_fake=mine_num
        self.smog_num=self.x*self.y
        self.arr=TwoDimensionArray(self.x,self.y)
        self.word_rect=pygame.Rect(0,self.y*27,300,27)
        self.fontObj = pygame.font.Font('freesansbold.ttf',20)
        self.mines=pygame.sprite.Group()
        self.smogs=pygame.sprite.Group()
        self.flags=pygame.sprite.Group()
        self.Lose_Value=False
        self.Win_Value=False

    def boom(self,i,j):
        for smog in self.smogs.copy():
            if smog.x==i and smog.y==j:
                self.smogs.remove(smog)
                self.smog_num-=1
        if self.arr.f(i,j) == 0:
            if i-1>=1 and j-1>=1: 
                for smog in self.smogs.copy():
                    if smog.x==i-1 and smog.y==j-1:
                        self.boom(i-1,j-1)                                            
            if i-1>=1:
                for smog in self.smogs.copy():
                    if smog.x==i-1 and smog.y==j:
                        self.boom(i-1,j)                            
            if j-1>=1:
                for smog in self.smogs.copy():
                    if smog.x==i and smog.y==j-1:
                        self.boom(i,j-1)                            
            if i-1>=1 and j+1<=self.y:
                for smog in self.smogs.copy():
                    if smog.x==i-1 and smog.y==j+1:
                        self.boom(i-1,j+1)                            
            if j+1<=self.y:
                for smog in self.smogs.copy():
                    if smog.x==i and smog.y==j+1:
                        self.boom(i,j+1)                            
            if i+1<=self.x and j+1<=self.y:
                for smog in self.smogs.copy():
                    if smog.x==i+1 and smog.y==j+1:
                        self.boom(i+1,j+1)                            
            if i+1<=self.x:
                for smog in self.smogs.copy():
                    if smog.x==i+1 and smog.y==j:
                        self.boom(i+1,j)                            
            if i+1<=self.x and j-1>=1:
                for smog in self.smogs.copy():
                    if smog.x==i+1 and smog.y==j-1:
                        self.boom(i+1,j-1)

    def start_game(self):
        for i in range(1,self.x+1):
            for j in range(1,self.y+1):
                new_smog=Smog(self,i,j)
                self.smogs.add(new_smog)
        for smog in self.smogs.sprites():
            smog.draw_smog()
        for i in range(1,self.x):
            l_color = (255, 255, 255)
            point1=(i*27,0)
            point2=(i*27,self.y*27)
            points=[point1,point2]
            pygame.draw.lines(self.screen, l_color, 0, points, 1)
        for j in range(1,self.y):
            l_color = (255, 255, 255)
            point1=(0,j*27)
            point2=(self.x*27,j*27)
            points=[point1,point2]
            pygame.draw.lines(self.screen, l_color, 0, points, 1)
        pygame.display.flip()
        flag_break=True
        while flag_break:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y < self.y*27 :
                        x=x//27+1
                        y=y//27+1
                        left,mid,right=pygame.mouse.get_pressed()
                        if left:
                            arr_new=[]
                            for i in range(self.mine_num):
                                while True:
                                    born_num=randint(0,self.x*self.y-1)
                                    if born_num != self.y*(x-1)+(y-1) and born_num not in arr_new:
                                        self.arr.array[born_num]=-1
                                        arr_new.append(born_num)
                                        break
                            for i in range(1,self.x+1):
                                for j in range(1,self.y+1):
                                    mine=0
                                    if self.arr.f(i,j)!=-1:
                                        if i-1>=1 and j-1>=1 and self.arr.f(i-1,j-1)==-1: 
                                            mine+=1
                                        if i-1>=1 and self.arr.f(i-1,j)==-1:
                                            mine+=1
                                        if j-1>=1 and self.arr.f(i,j-1)==-1:
                                            mine+=1
                                        if i-1>=1 and j+1<=self.y and self.arr.f(i-1,j+1)==-1:
                                            mine+=1
                                        if j+1<=self.y and self.arr.f(i,j+1)==-1:
                                            mine+=1
                                        if i+1<=self.x and j+1<=self.y and self.arr.f(i+1,j+1)==-1:
                                            mine+=1
                                        if i+1<=self.x and self.arr.f(i+1,j)==-1:
                                            mine+=1
                                        if i+1<=self.x and j-1>=1 and self.arr.f(i+1,j-1)==-1:
                                            mine+=1
                                        self.arr.array[self.y*(i-1)+(j-1)]=mine
                                    new_mine=Mine(self,self.arr.f(i,j),i,j)
                                    self.mines.add(new_mine)
                            if self.arr.f(x,y)==0:
                                self.boom(x,y)
                            else:
                                for smog in self.smogs.copy():
                                    if smog.x==x and smog.y==y:
                                        self.smogs.remove(smog)
                                        self.smog_num-=1
                            flag_break=False
                            if self.smog_num==self.mine_num:
                                self.Win_Value=True
                            break

    def run_game(self):
        game_run_value=True
        while game_run_value:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y < self.y*27 :
                        x=x//27+1
                        y=y//27+1
                        left,mid,right=pygame.mouse.get_pressed()
                        if left:
                            if self.arr.f(x,y)==0:
                                self.boom(x,y)
                            else:
                                for smog in self.smogs.copy():
                                    if smog.x==x and smog.y==y:
                                        self.smogs.remove(smog)
                                        self.smog_num-=1
                            if self.arr.f(x,y)==-1:
                                self.Lose_Value=True
                        elif mid:
                            mid_value=True
                            for smog in self.smogs.copy():
                                if smog.x==x and smog.y==y:
                                    mid_value=False
                            if mid_value:
                                local_flag_num=0
                                if x-1>=1 and y-1>=1: 
                                    for flag in self.flags.copy():
                                        if flag.x==x-1 and flag.y==y-1:
                                            local_flag_num+=1                                               
                                if x-1>=1:
                                    for flag in self.flags.copy():
                                        if flag.x==x-1 and flag.y==y:
                                            local_flag_num+=1                             
                                if y-1>=1:
                                    for flag in self.flags.copy():
                                        if flag.x==x and flag.y==y-1:
                                            local_flag_num+=1                              
                                if x-1>=1 and y+1<=self.y:
                                    for flag in self.flags.copy():
                                        if flag.x==x-1 and flag.y==y+1:
                                            local_flag_num+=1                              
                                if y+1<=self.y:
                                    for flag in self.flags.copy():
                                        if flag.x==x and flag.y==y+1:
                                            local_flag_num+=1                              
                                if x+1<=self.x and y+1<=self.y:
                                    for flag in self.flags.copy():
                                        if flag.x==x+1 and flag.y==y+1:
                                            local_flag_num+=1                              
                                if x+1<=self.x:
                                    for flag in self.flags.copy():
                                        if flag.x==x+1 and flag.y==y:
                                            local_flag_num+=1                             
                                if x+1<=self.x and y-1>=1:
                                    for flag in self.flags.copy():
                                        if flag.x==x+1 and flag.y==y-1:
                                            local_flag_num+=1
                                #####################
                                if local_flag_num==self.arr.f(x,y):
                                    if x-1>=1 and y-1>=1: 
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x-1 and flag.y==y-1:
                                                open_value=False
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x-1 and smog.y==y-1:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if x-1>=1:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x-1 and flag.y==y:
                                                open_value=False  
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x-1 and smog.y==y:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if y-1>=1:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x and flag.y==y-1:
                                                open_value=False
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x and smog.y==y-1:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if x-1>=1 and y+1<=self.y:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x-1 and flag.y==y+1:
                                                open_value=False
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x-1 and smog.y==y+1:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if y+1<=self.y:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x and flag.y==y+1:
                                                open_value=False   
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x and smog.y==y+1:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if x+1<=self.x and y+1<=self.y:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x+1 and flag.y==y+1:
                                                open_value=False
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x+1 and smog.y==y+1:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if x+1<=self.x:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x+1 and flag.y==y:
                                                open_value=False
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x+1 and smog.y==y:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                                    if x+1<=self.x and y-1>=1:
                                        open_value=True
                                        for flag in self.flags.copy():
                                            if flag.x==x+1 and flag.y==y-1:
                                                open_value=False 
                                        if open_value:
                                            for smog in self.smogs.copy():
                                                if smog.x==x+1 and smog.y==y-1:
                                                    if self.arr.f(smog.x,smog.y)==0:
                                                        self.boom(smog.x,smog.y)
                                                    else:
                                                        self.smogs.remove(smog)
                                                        self.smog_num-=1
                                                        if self.arr.f(smog.x,smog.y)==-1:
                                                            self.Lose_Value=True
                        elif right:
                            flag_t=True
                            if self.flags.sprites():
                                for flag in self.flags.copy():
                                    if flag.y==y and flag.x==x:
                                        self.flags.remove(flag)
                                        self.mine_num_alive_fake+=1
                                        flag_t=False
                            if flag_t:
                                for smog in self.smogs.copy():
                                    if smog.x==x and smog.y==y:
                                        new_flag=Flag(self,x,y)
                                        self.flags.add(new_flag)
                                        self.mine_num_alive_fake-=1
                            
            if self.smog_num==self.mine_num:
                self.Win_Value=True
            for mine in self.mines.sprites():
                mine.blitme()
            for smog in self.smogs.sprites():
                smog.draw_smog()
            for flag in self.flags.sprites():
                flag.blitme()
            for i in range(1,self.x):
                l_color = (255, 255, 255)
                point1=(i*27,0)
                point2=(i*27,self.y*27)
                points=[point1,point2]
                pygame.draw.lines(self.screen, l_color, 0, points, 1)
            for j in range(1,self.y):
                l_color = (255, 255, 255)
                point1=(0,j*27)
                point2=(self.x*27,j*27)
                points=[point1,point2]
                pygame.draw.lines(self.screen, l_color, 0, points, 1)
            if self.Lose_Value:
                game_run_value=False
                for mine in self.mines.sprites():
                    if mine.n==-1:
                        mine.blitme()
                self.textSurfaceObj = self.fontObj.render("LOSE!(Press Q to Quit)                               ",True,(255,255,255),(0,0,0))
            elif self.Win_Value:
                game_run_value=False
                for smog in self.smogs.sprites():
                    smog.image=pygame.image.load(f"images/flag.png")
                    smog.rect=smog.image.get_rect()
                    smog.rect.x=(smog.x-1)*27
                    smog.rect.y=(smog.y-1)*27
                    smog.screen.blit(smog.image,smog.rect)
                self.textSurfaceObj = self.fontObj.render("WIN!(Press Q to Quit)                                ",True,(255,255,255),(0,0,0))
            else:
                self.textSurfaceObj = self.fontObj.render("                                                     ",True,(255,255,255),(0,0,0))
                self.screen.blit(self.textSurfaceObj,self.word_rect)
                self.textSurfaceObj = self.fontObj.render(f"remained unflagged mines: {self.mine_num_alive_fake}",True,(255,255,255),(0,0,0))
            self.screen.blit(self.textSurfaceObj,self.word_rect)
            pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        sys.exit()

class Flag(Sprite):
    def __init__(self,ai_game,x,y):
        super().__init__()
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.image=pygame.image.load(f"images/flag.png")
        self.rect=self.image.get_rect()
        self.rect.x=(x-1)*27
        self.rect.y=(y-1)*27
        self.x=x
        self.y=y
    def blitme(self):
        self.screen.blit(self.image,self.rect)

class Smog(Sprite):
    def __init__(self,ai_game,x,y):
        super().__init__()
        self.x=x
        self.y=y
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.color=(60,60,60)
        self.rect=pygame.Rect(0,0,27,27)
        self.rect.x=(x-1)*27
        self.rect.y=(y-1)*27
    def draw_smog(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
class Mine(Sprite):
    def __init__(self,ai_game,n,x,y):
        super().__init__()
        self.x=x
        self.y=y
        self.n=n
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.image=pygame.image.load(f"images/{n}.png")
        self.rect=self.image.get_rect()
        self.rect.x=(x-1)*27
        self.rect.y=(y-1)*27
    def blitme(self):
        self.screen.blit(self.image,self.rect)
if __name__=='__main__':
    x=int(input("雷盘宽度："))
    y=int(input("雷盘高度："))
    while 1:
        mine_num=int(input("地雷数量："))
        if mine_num<x*y:
            break
        else:
            print("地雷数量超过上限！重输！")
    ai=MineSweeper(x,y,mine_num)
    ai.start_game()
    ai.run_game()