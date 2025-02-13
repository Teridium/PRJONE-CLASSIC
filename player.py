from numpy import cos, sin
import pygame as pg
import pygame_gui as gui
from options import *
from inv import *
from terrain import terrain


class player:
    def __init__(self, app):
        self.app = app
        self.inv = inv(self.app, self)
        self.dig = False
        self.timer = app.timer
        self.start_dig = 0
        self.is_openinv = False
        self.demolition = False
        self.warmup = 0
        self.pos = ()        
        
    def update(self):
        self.inv.update()
    
    def draw(self):
        if self.is_openinv:
            self.inv.draw()
    
    # Place the item selected from the inventory on titlepos the ground
    # player.inv.selected_backpack_cell - selected inventory item 
    def build(self, field):
        if self.inv.selected_backpack_cell>-1:
            item = self.inv.item
            place = field.GetInfo('name', field.field[field.tile_pos[0], field.tile_pos[1]])
            build_item, build_type = field.Get_info_block_placed(item, place)   
            if build_type=='terrain':
                field.field[field.tile_pos[0], field.tile_pos[1]] = build_item['id']
                self.use_selected()
            elif build_type=='block':
                field.building_map[field.tile_pos[0], field.tile_pos[1]]=build_item['id']
                self.use_selected()     
                self.app.ui_tech.refresh_site_content(field.tile_pos)
                
    
    def manual_dig(self, field, tilepos, time):
        if not self.dig:
            self.tile_pos = tilepos
            self.dig = True
            self.warmup = self.timer.get_ticks()
            self.app.mouse.setcursor(cursor_type.dig)
        else:
            dt = self.timer.get_ticks()-self.warmup
            if tilepos==self.tile_pos:
                if dt>time*1000:
                    self.warmup = self.timer.get_ticks()
                    field.dig_succes(self, tilepos)
                    self.stop_dig()
                    return(True)
            else:
                self.stop_dig()
                    
    
    def stop_dig(self):
        if self.dig:
            self.app.mouse.setcursor(cursor_type.normal)
            self.dig = False
            self.hp = 100
            
            

            self.app.info.debug((0,30), f'{self.hp} - dig: {self.dig}')
       
    def manual_demolition(self, field, tilepos, time):
        if not self.demolition:
            self.tile_pos = tilepos
            self.demolition = True
            self.warmup = self.timer.get_ticks()
            self.app.mouse.setcursor(cursor_type.dig)
            return(False)
        else:
            dt = self.timer.get_ticks()-self.warmup
            if tilepos==self.tile_pos:
                if dt>time*1000:
                    self.warmup = self.timer.get_ticks()
                    field.demolition_succes(self, tilepos)
                    self.stop_demolition()
                    return(True)
            else:
                self.stop_demolition()
                
                

    def stop_demolition(self):
        if self.demolition:
            self.app.mouse.setcursor(cursor_type.normal)
            self.demolition = False
            self.warmup = 0

            
    def pickup(self, loot, count=1):
        self.inv.add(loot, count)
     
    def use_selected(self):
        self.inv.delete_selected_backpack_cell()
        
    def fall(self, pos):
        terra = self.app.terrain
        bp = terra.GetFData('name', 'Escape pod')
        b_map = terra.building_map
        factory=self.app.factories.add(bp, b_map, pos[0], pos[1])
        # bp = terra.GetFData('name', 'quarry_2')
        # factory=self.app.factories.add(bp, b_map, pos[0]+5, pos[1]+5)
        pos = (pos[0]+factory.size[0]//2, pos[1]+factory.size[1]//2)
        self.scorch_ground(pos, 4)
        self.add_water(pos, 7)
        self.go_pos(terra, pos)
        self.set_spawn(pos)
        
    def go_pos(self, terra, pos):
        if terra.onMap(pos[0],pos[1]):
            terra.pos = pos
            
    def set_spawn(self, pos):
        self.pos = pos
        
    def go_spawn(self):
        terra = self.app.terrain
        self.go_pos(terra, self.pos)
        
    def scorch_ground(self, pos, rad):
        for angle in range(0, 360,2):
            r = randrange(0, rad)
            x,y = round(pos[0]+r * cos(angle)-0.5), round(pos[1]+r * sin(angle)-0.5)
            self.app.terrain.field[x,y] = self.app.terrain.GetTData('name', 'scorched_ground')['id']
            self.app.terrain.building_map[x,y] = 0
    def add_water(self, pos, rad):
        angle = randrange(0, 360)
        x = rad * cos(angle)
        y = rad * sin(angle)
        self.app.terrain.field[round(pos[0]+x-0.5),round(pos[1]+y-0.5)] = self.app.terrain.GetTData('name', 'water')['id']
        
            
