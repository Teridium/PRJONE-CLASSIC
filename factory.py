import pygame as pg
from options import *
from storage  import *
import random as rnd
import numpy as np


class factory:
    def __init__(self, list, app, blueprint,  x, y):
        self.app = app
        self.list = list
        self.id = blueprint['id']
        self.name = blueprint['name']
        self.efficiency = blueprint['efficiency']
        self.tile_pos = (x, y)
        self.size = (blueprint['dim']['w'], blueprint['dim']['h'])
        self.allow_recipe_list = []

        if 'plan' in blueprint.keys():
            self.plan = np.transpose(blueprint['plan'])
        else:
            self.plan = None
        self.demolition = blueprint['demolition']
        self.pic = list.factory_img[blueprint['id']]
        self.pic_id = blueprint['id']

        self.recipe = None
        if 'use_recipes' in blueprint.keys():
            base_recipe_id = blueprint['use_recipes']['selected_id']
            self.recipe = self.get_recipe_by_id(base_recipe_id)
            self.allow_recipe_list = blueprint['use_recipes']['allowed_id']

        if 'storage' in blueprint.keys():
            self.storage = storage(app, self, blueprint['storage'])
        
        if 'operate' in blueprint.keys():
            self.operate = (blueprint['operate'])
            self.app.terrain.set_operate(x+self.size[0]//2,y+self.size[1]//2, self.operate)
        else:
            self.operate = 0
        if 'detect' in blueprint.keys():
            self.detect = (blueprint['detect'])
            self.app.terrain.set_discover(x+self.size[0]//2,y+self.size[1]//2, self.detect)
        else:
            self.detect = 0
        
        # if 'detect' in bp.keys():
        #     discover_radius = bp['detect']
        #     self.app.terrain.set_discover(x+new_factory.size[0]//2,y+new_factory.size[1]//2, discover_radius)
        # if 'operate' in bp.keys():
        #     operate_radius = bp['operate']
        #     self.app.terrain.set_operate(x+new_factory.size[0]//2,y+new_factory.size[1]//2, operate_radius)



        self.working = False
        self.timer = app.timer
        self.time = 0

    def get_recipe_by_id(self, id):    
        result = -1
        self.app.terrain.data['recipes']
        for i in self.app.terrain.data['recipes']:
            if i['id']==id: 
                return i
        return result
        
        
    def get_resources(self, minproc=100, maxproc=100):
        if minproc==maxproc: 
            proc=maxproc
        else:
            proc = rnd.randrange(minproc, maxproc)
        res, count = np.unique(self.plan, return_counts=True)
        all_res = (res, np.int64(count*(proc/100)))
        return(all_res)
    
    @property
    def demolition_list_items_100(self):
        res = self.get_resources()
        list_items = []
        i=0
        for item in res[0]:
            if item and item!=0:
                list_items.append({'id':item,'count':res[1][i]})
            i+=1
        return(list_items)
    
    def draw(self, surface):
        screen_pos = self.app.terrain.demapping(self.tile_pos)
        f_rect = pg.Rect(screen_pos, (self.size[0]*TILE, self.size[1]*TILE))
        if pg.Rect(VIEW_RECT).colliderect(f_rect):
            if self.app.factories.selected==self:
                surface.blit(self.pic, f_rect)
                pg.draw.rect(surface, pg.Color('gray'), f_rect, 1)
            else:
                surface.blit(self.pic, f_rect)
            
    def update(self):
        if self.recipe is None: return
        if not self.working:
            # to-do: resource translate begin
            if 'in' in self.recipe.keys(): 
                in_res=self.recipe['in']
            else: 
                in_res=None

            if self.app.player.inv.exist(in_res):
                self.app.player.inv.delete(in_res)
                self.time = self.timer.get_ticks()
                self.working = True
        else:
            if self.timer.get_ticks()-self.time>self.recipe['time']/self.efficiency*1000:
                # to-do: resource translate end
                
                self.app.player.inv.insert(self.recipe['out'])
                self.working = False
        
    @property
    def progress(self):
        if self.working:
            now = self.timer.get_ticks()
            return((now-self.time)/(self.recipe['time']/self.efficiency*1000))      
        else:
            return(0)

    @property
    def incom(self):
        if not self.recipe is None:
            if 'in' in self.recipe.keys():
                return(self.recipe['in'])      
        return(None)

    @property
    def outcom(self):
        if not self.recipe is None:
            if 'out' in self.recipe.keys():
                return(self.recipe['out'])      
        return(None)

    @property
    def process_time(self):
        if not self.recipe is None:
            if 'time' in self.recipe.keys():
                return(self.recipe['time']*1000)      
        return(0)

class factory_list:
    def __init__(self, app):
        self.app = app
        self.list = []
        self.active = None

        self.factory_img = [0 for i in app.terrain.data['factory_type']]
        for img in app.terrain.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())
        # self.factory_img_rect = self.factory_img[0].get_rect()

    def add(self, bp, b_map, x, y):
        width = bp['dim']['w']
        hight = bp['dim']['h']
        for j in range(y, y+hight):
            for i in range(x, x+width):
                b_map[i,j] = -1

        new_factory = factory(self, self.app, bp, x,y)
        self.list.append(new_factory)
      
            
        return(new_factory)
            
        

    def delete(self,b_map, factory):
        width, hight = factory.size
        x, y = factory.tile_pos
        for i in range(x, x+width):
            for j in range(y, y+hight):
                b_map[i, j] = 0
                
        if factory.operate>0:
            self.app.terrain.set_operate(x+factory.size[0]//2,y+factory.size[1]//2, factory.operate, -1)
                
                
        self.list.remove(factory)

        
    def factory(self, tile_pos):
        for f in self.list:
            if pg.Rect(f.tile_pos,f.size).collidepoint(tile_pos):
                return(f)
        return()

    def draw(self, surface):
        for f in self.list:
            f.draw(surface)
            
    def update(self):
        # update
        for f in self.list:
            f.update()
            
        # control
            
    @property
    def rect_list_all(self):
        f_list = []
        for item in self.list:
            f_list.append(pg.Rect(item.tile_pos, item.size))
        return f_list
        
    @property
    def selected(self):
        return self.active
    
    def select(self, num):
        if num!=-1: 
            self.active = self.list[num]

    def unselect(self):
        self.active = None

    def get_by_num(self, num):
        if num>-1 and num<len(self.list):
            return self.list[num]
        else:
            return None
