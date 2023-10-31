import pygame as pg
from pygame.locals import *
import numpy as np
import random as rd
import configparser

car_ini=configparser.ConfigParser()
car_ini.read('./car.ini',encoding='UTF-8')

window_size=WIDTH,HEIGHT=1542,1080
bg_color=(0,0,0)
FPS=30
#262    360
pg.init()
screen=pg.display.set_mode(window_size)
pg.display.set_caption('outrun')

def rotate(screen,image,angle):
    rotated=pg.transform.rotate(image,angle)
    size=rotated.get_size()
    pos=(image.x+image.w/2-size[0]/2,image.y+image.h/2-size[1]/2)
    screen.blit(rotated,pos)

class Car:
    global car_ini
    def __init__(self,model,tm):
#   初期化
        self.model=model
        self.power=[]
        self.rpm=1000
        self.kmh=0
        self.gear=1
        self.gear_ck=0
        self.gear_n=1
        self.speed=0
        self.power_array=0
        self.gear_ratio=[]
        self.final=0
        self.outer_cir=0
        self.radius=0
        self.spd=0
        self.rev=0
        self.weight=0
        self.torque=0
        self.shift=0
        self.rpm_shift=0
        self.transmission=tm
#   車両データ読み込み
        self.speed=int(car_ini[f'{self.model}']['speed'])
        self.rev=int(car_ini[f'{self.model}']['rev'])
        for i in range(0,int(self.rev/100)):
            self.power.append(int(car_ini[f'{self.model}']['rpm'+str(i*100)]))
        for i in range(2,self.speed+2):
            self.gear_ratio.append(float(car_ini[f'{self.model}'][f'g{i-1}']))
        self.final=float(car_ini[f'{self.model}']['final']) 
        self.outer_cir=float(car_ini[f'{self.model}']['outer_cir'])
        self.radius=int(car_ini[f'{self.model}']['radius'])
        self.weight=int(car_ini[f'{self.model}']['weight'])
        self.gear=self.gear_ratio[0]
#   車速計測
    def vehicle_spd(self):
    #    for i in range(0,int(self.rev/100)):
    #        if(int(self.rpm)<int(i+1)*100):
    #            self.power_array=i
    #            break
        if(self.gear_n==0):
            self.kmh=self.kmh
        else:
            self.kmh=int((float(self.rpm))/((self.gear)*(self.final))*float(self.outer_cir)*60.0/1000.0)
        self.torque=((self.power[self.power_array]/1.3596)/(self.rpm*2*3.14/60/100))
        acc=((self.power_array*2*self.gear*self.final)/(self.radius*self.weight))
        print(f'TORQUE:{round(self.torque,0)}, RPM:{self.rpm}, km/h:{round(self.kmh,0)}, gear:{self.gear_n}, gear_ratio:{self.gear}, acc:{acc}, power_array:{self.power_array}')
#   エンジン
    def engine(self):
        pg.event.pump()
        self.pressed=pg.key.get_pressed()
#        print(self.pressed[K_w])
        if(self.shift==0):
#       アクセル
            if((self.pressed[K_w]==True)and(self.rpm<self.rev)and(self.rpm>300)):
                for i in range(0,int(self.rev/100)):
                    if(int(self.rpm)<int(i+1)*100):
                        self.power_array=i
                        self.rpm=self.rpm+(int(self.power[self.power_array]))
                        break
                    
#       アクセルオフ
            elif((self.pressed[K_w]==False)and(self.rpm>600)):
                print('kansei')
                self.rpm=self.rpm-50
                
#       ブレーキ
            if((self.pressed[K_s]==True)and(self.rpm>100)):
                print('brake')
                self.rpm=self.rpm-100
                
#       セル
            if((self.pressed[K_c]==True)and(self.rpm<500)):
                self.rpm=self.rpm+100

#               MT
            if(self.transmission=='MT'):    
                if(self.gear_ck==0):
                    
    #           シフトアップ
                    if((self.pressed[K_LSHIFT]==True)and(self.gear_n<self.speed)):
                        self.gear_n=self.gear_n+1
                        self.gear=self.gear_ratio[self.gear_n-1]
                        self.rpm_shift=self.rpm-(self.rpm/4)
                        self.shift=1
                        
    #           シフトダウン
                    elif((self.pressed[K_LCTRL]==True)and(self.gear_n-1>0)):
                        self.gear_n=self.gear_n-1
                        self.gear=self.gear_ratio[self.gear_n-1]
                        self.rpm_shift=self.rpm+(self.rpm/4)
                        self.shift=2
                    self.gear_ck=1
                if((self.pressed[K_LSHIFT]==False)and(self.pressed[K_LCTRL]==False)):
                    self.gear_ck=0
#               AT
            elif(self.transmission=='AT'):
                if(self.gear_ck==0):
    #           シフトアップ       
                    if((self.rpm>(self.rev-1500))and(self.gear_n<self.speed)):
                        self.gear_n=self.gear_n+1
                        self.gear=self.gear_ratio[self.gear_n-1]
                        self.rpm_shift=self.rpm-(self.rpm/4)
                        self.shift=1
                        self.gear_ck=1
    #           シフトダウン
                    elif((self.rpm<3500)and(self.gear_n-1>0)):
                        self.gear_n=self.gear_n-1
                        self.gear=self.gear_ratio[self.gear_n-1]
                        self.rpm_shift=self.rpm+(self.rpm/4)
                        self.shift=2
                        self.gear_ck=1
                    
#       シフトアップ中
        elif(self.shift==1):
            self.rpm=self.rpm-100
            if(self.rpm<self.rpm_shift):
                self.shift=0
                self.gear_ck=0
                
#       シフトダウン中
        elif(self.shift==2):
            self.rpm=self.rpm+100
            if(self.rpm>self.rpm_shift):
                self.shift=0
                self.gear_ck=0
                
        for i in range(0,int(self.rev/100)):
            if(int(self.rpm)<int(i+1)*100):
                self.power_array=i
                break
                        
class meter:
    def __init__(self):
#   画像読み込み(メーター系)
        self.defi=pg.image.load('./image/defi_250.png')
        self.defi_arrow=pg.image.load('./image/defi_arrow.png')
        self.defi_arrow_rotate=pg.image.load('./image/defi_arrow.png')
        self.defi_arrow_rotated=pg.image.load('./image/defi_arrow.png')
        self.defi=pg.transform.scale(self.defi,(300,300))
        self.defi_arrow=pg.transform.scale(self.defi_arrow,(300,300))
        self.arrow_deg=0
        self.arrow_pos=0,0
        self.arrow_size=0

    def write(self,rpm):
        self.arrow_deg=rpm*0.03*-1
        self.defi_arrow_angle=self.arrow_deg
        self.defi_arrow_rotate=pg.transform.rotate(self.defi_arrow,self.arrow_deg)
        self.arrow_rotate_size=self.defi_arrow_rotate.get_size()
        self.arrow_size=self.defi_arrow.get_size()
        self.arrow_pos=((self.arrow_size[0]+self.arrow_size[1]/2-self.arrow_rotate_size[0]/2)+950,(self.arrow_size[1]+self.arrow_size[1]/2-self.arrow_rotate_size[1]/2)+475)
        
    def display(self):
        screen.blit(self.defi,(1250,775))
        screen.blit(self.defi_arrow_rotate,self.arrow_pos)
        
class background:
    def __init__(self):
        self.backgrounds=[]
        self.odo=0
        for i in range(1,41):
            self.backgrounds.append(pg.image.load(f'./image/processed/start/outrun{i:04}.png'))
#            print(self.backgrounds[i-1])
        self.bflag=pg.image.load('./image/processed/start/blue_flag.png')
        self.yflag=pg.image.load('./image/processed/start/yellow_flag.png')
        self.rflag=pg.image.load('./image/processed/start/red_flag.png')
        screen.blit(self.rflag,(0,0))
        
#    def write(self):
          
    
    
driving=Car('rx8','AT')
defi=meter()
defi.display()
bg=background()


def main():
#   画像読み込み

    #screen.fill(bg_color)
    clock=pg.time.Clock()
    while True:
        driving.engine()
        driving.vehicle_spd()
        defi.write(driving.rpm)
        defi.display()
        pg.display.update()
        screen.fill(bg_color)
        clock.tick(FPS)

if(__name__=='__main__'):
    main()
    

        