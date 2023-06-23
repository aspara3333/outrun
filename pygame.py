import pygame as pg
import numpy as np
import random as rd
import configparser

car_ini=configparser.ConfigParser()
car_ini.read('car.ini',encoding='utf-8')

class Car:
    def __init__(self):
#   初期化
        self.power=[]
        self.rpm=0
        self.kmh_be=0
        self.kmh=0
        self.gear=0
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
        self.speed=int(car_ini[f'{self}']['speed'])
        self.rev=int(car_ini[f'{self}']['rev']) 
        for i in range(1,self.speed+1):
            self.gear_ratio[i]=float(car_ini[f'{self}'][f'g{i}'])
        self.final=float(car_ini[f'{self}']['final']) 
        self.outer_cir=float(car_ini[f'{self}']['outer_cir'])
        self.weight=int(car_ini[f'{self}']['weight'])
    
    def vehicle_spd(self):
        for i in range(0,int(self.rev/100)):
            if(int(self.rpm)<int(i+1)*100):
                power_array=i
                break
        self.kmh_be=int((float(self.rpm)*float(self.outer_cir)*60.0)/(self.gear*self.final*1000.0))
        torque=((self.power[self.power_array]/1.3596)/(self.rpm*2*3.14/60/100))
        acc=((torque*self.gear*self.final)/(self.outer_cir*self.weight))
        self.kmh=self.kmh+acc*0.125
        