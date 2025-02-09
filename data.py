import json
from PIL import ImageFilter, Image

import cv2
import numpy as np
import pygame as pg

from options import *
# from sequence import * 
from utils import convert_opencv_img_to_pygame, cvimage_grayscale


class data:
    def __init__(self) -> None:
        f = open('data/data.json', encoding='utf-8')
        self.data = json.load(f)
        f.close

        self.factory_img = [None for i in self.data['factory_type']]
        # self.block_img = [None for i in self.data['block_type']]     

    def get_recipe_by_id(self, id):    
        for i in self.data['recipes']:
            if i['id']==id: 
                return i
        return None

    def get_block_by_id(self, id):    
        for i in self.data['block_type']:
            if i['id']==id: 
                return i
        return None

    def get_terrain_by_id(self, id):    
        for i in self.data['terrain_type']:
            if i['id']==id: 
                return i
        return None

    def get_terrain_by_name(self, id):    
        for i in self.data['terrain_type']:
            if i['name']==id: 
                return i
        return None


    def get_tool_by_name(self, name):    
        for i in self.data['toolbar']:
            if i['name']==name: 
                return i
        return None

    def get_block_by_name(self, name):    
        for i in self.data['block_type']:
            if i['name']==name: 
                return i
        return None


    def get_img(self, id, img_type):
        for i in self.data[img_type]:
            if i['id']==id: 
                return i['img']
        

    def init_sprites(self):
        for img in self.data['factory_type']:
            self.factory_img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())

        for item in self.data['terrain_type']:
            item['img'] = pg.image.load(path.join(img_dir, item['pic'])).convert_alpha()
            cvimg = cv2.imread(path.join(img_dir, item['pic']))
            item['img_bw'] = convert_opencv_img_to_pygame(cvimage_grayscale(cvimg))
            
            img = pg.image.load(path.join(img_dir, item['pic'])).convert_alpha()
            blueprint = pg.Surface(img.get_size(), pg.SRCALPHA)
            blueprint.fill((255, 0, 0, 80))
            img.blit(blueprint, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
            item['img_bp'] = img
            
        for item in self.data['block_type']:
            item['img'] = (pg.image.load(path.join(img_dir, item['pic'])).convert_alpha())
            
            img = pg.image.load(path.join(img_dir, item['pic'])).convert_alpha()
            blueprint = pg.Surface(img.get_size(), pg.SRCALPHA)
            blueprint.fill((255, 0, 0, 80))
            img.blit(blueprint, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
            item['img_bp'] = img
            
        for item in self.data['factory_type']:
            item['img'] = (pg.image.load(path.join(img_dir, item['pic'])).convert_alpha())

        for item in self.data['recipes']:
            item['img'] = (pg.image.load(path.join(img_dir, item['pic'])).convert_alpha())
            
        # self.block_img = [0 for i in self.data['block_type']]
        # for img in self.data['block_type']:
        #     self.block_img[img['id']] = (pg.image.load(
        #         path.join(img_dir, img['pic'])).convert_alpha())
        # self.block_img_rect = self.block_img[1].get_rect()

            
        
        
    def GetTileInfo(self, terrain, name, tilepos):
        if not tilepos:
            pic_idx = self.FindTInfo('id', 'hyperspace')
            return (self.GetInfo(name, pic_idx))

        return(self.data.get('terrain_type')[terrain.field[tilepos[0], tilepos[1]]][name])

    def GetInfo(self, name, id):
        return(self.data.get('terrain_type')[id][name])

    def FindBInfo(self, name, stroke):
        for item in self.data.get('block_type'):
            if item['name'] == stroke:
                return(item[name])

    def GetBData(self, key, stroke):
        for item in self.data.get('block_type'):
            if item[key] == stroke:
                return(item)

    def GetTData(self, key, stroke):
        for item in self.data.get('terrain_type'):
            if item[key] == stroke:
                return(item)

    def GetFData(self, key, stroke):
        for item in self.data.get('factory_type'):
            if item[key] == stroke:
                return(item)

    def FindTInfo(self, name, stroke):
        for item in self.data.get('terrain_type'):
            if item['name'] == stroke:
                return(item[name])

    def FindInfo(self, name, stroke, b_type):
        if b_type == 'block':
            return(self.FindBInfo(name, stroke))
        elif b_type == 'terrain':
            return(self.FindTInfo(name, stroke))
        

        
    def get_bdata(self, key, stroke):
        for item in self.data.get('block_type'):
            if item[key] == stroke:
                return(item)

    def get_tdata(self, key, stroke):
        for item in self.data.get('terrain_type'):
            if item[key] == stroke:
                return(item)

    def get_fdata(self, key, stroke):
        for item in self.data.get('factory_type'):
            if item[key] == stroke:
                return(item)
    
