import pygame as pg
from pygame.locals import *
import numpy as np
import random as rd
import configparser

car_ini=configparser.ConfigParser()
car_ini.read('./car.ini',encoding='UTF-8')

window_size=WIDTH,HEIGHT=1000,700
bg_color=(0,0,0)
FPS=30

pg.init()
screen=pg.display.set_mode(window_size)
pg.display.set_caption('outrun')

class Car:
    global car_ini
    def __init__(self,model):
#   初期化
        self.model=model
        self.power=[]
        self.rpm=1000
        self.kmh_be=0
        self.kmh=0
        self.gear=1000
        self.gear_ck=0
        self.gear_n=0
        self.speed=0
        self.power_array=0
        self.gear_ratio=[]
        self.final=0
        self.outer_cir=0
        self.spd=0
        self.rev=0
        self.weight=0
#   車両データ読み込み
        self.speed=int(car_ini[f'{self.model}']['speed'])
        self.rev=int(car_ini[f'{self.model}']['rev'])
        for i in range(0,int(self.rev/100)):
            self.power.append(int(car_ini[f'{self.model}']['rpm'+str(i*100)]))
        for i in range(1,self.speed+1):
            self.gear_ratio.append(float(car_ini[f'{self.model}'][f'g{i}']))
        self.final=float(car_ini[f'{self.model}']['final']) 
        self.outer_cir=float(car_ini[f'{self.model}']['outer_cir'])
        self.weight=int(car_ini[f'{self.model}']['weight'])
#   車速計測
    def vehicle_spd(self):
        for i in range(0,int(self.rev/100)):
            if(int(self.rpm)<int(i+1)*100):
                self.power_array=i
                break
        self.kmh_be=int((float(self.rpm)*float(self.outer_cir)*60.0)/(self.gear*self.final*1000.0))
        torque=((self.power[self.power_array]/1.3596)/(self.rpm*2*3.14/60/100))
        acc=((torque*self.gear*self.final)/(self.outer_cir*self.weight))
        self.kmh=self.kmh+acc*0.125
        print(self.kmh)
#   エンジン
    def engine(self):
        pg.event.pump()
        self.pressed=pg.key.get_pressed()
        if((self.pressed[K_w])and(self.rpm<self.rev)):
            for i in range(0,int(self.rev/100)):
                if(int(self.rpm)<int(i+1)*100):
                    self.power_array=i
                    break
                
class meter:
    def __init__(self):
#   画像読み込み(メーター系)
        self.defi=pg.image.load('./image/defi_250.png')
        self.defi_arrow=pg.image.load('./image/defi_arrow.png')
        self.defi=pg.transform.scale(self.defi,(200,200))
        self.defi_arrow=pg.transform.scale(self.defi_arrow,(200,200))

    def write(self,rpm):
        self.arrow_deg=rpm*0.03*-1
        self.defi_arrow_angle=self.arrow_deg
        
    def display(self):
        screen.blit(self.defi,(800,500))
        screen.blit(self.defi_arrow,(800,500))
        

driving=Car('rx8')
defi=meter()
defi.display()

def main():
#   画像読み込み

    #screen.fill(bg_color)
    clock=pg.time.Clock()
    while True:
        driving.engine()
        driving.vehicle_spd()
        #screen.fill(bg_color)
        pg.display.update()
        clock.tick(FPS)

if(__name__=='__main__'):
    main()
    

        