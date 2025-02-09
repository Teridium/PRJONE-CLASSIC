import pygame as pg
import pygame_gui as gui

from inv_base import inv
from mouse import *
from options import *


class inv_recipe(inv):
    def __init__(self, app):
        super().__init__(app, (-3, -2), (2,5), inv_cell_h=64,  bg_color=pg.Color('#1f1f1f'), bg_hover_color=pg.Color('#2f2f2f'), inv_margin=5)
        self.mouse_button = pg.mouse.get_pressed()
        
    
    def update(self):
        super().update()
        # self.keystate = pg.key.get_pressed()
        # self.mouse_button = pg.mouse.get_pressed()
        # self.mouse_pos = pg.mouse.get_pos()
        # self.hover_cell_num, self.hover_item, self.is_hover = self.get_cell(self.mouse_pos)        
        
        
        if not self.is_open: return
      
        mouse_status_type = self.app.mouse.status['tile_action']
        mouse_status_button = self.app.mouse.status['button']
      
        if self.keystate[pg.K_ESCAPE] or (mouse_status_type == 1 and mouse_status_button==1):
            if self.first_pressed:
                self.first_pressed = False 
                self.is_open = False
                self.clear()
        else:
            self.first_pressed = True
            
        if self.mouse_button[0]:
            if self.first_click:
                self.first_click = False 
                if not self.hover_cell_num is None and self.hover_cell_num<len(self.cells):
                    # select item
                    self.select(self.hover_cell_num)
                    selected_factory = self.app.factories.selected
                    selected_factory.recipe = self.item                   
                    self.is_open = False
                    self.clear()
        else:
            self.first_click = True
        
        if not self.mouse_button[0]:
            if self.mouse_button[2]:
                self.is_open = False
                self.clear()

    
    def draw(self):
        if not self.is_open: return
        super().draw()
        # self.draw_items()
        self.app.screen.blit(self.surface, self.inv_pos)

    def load_recipe(self, allow_recipe_list, select_recipe):
        for i, recipe_id in enumerate(allow_recipe_list):
            recipe = self.app.data.get_recipe_by_id(recipe_id)
            self.cells.append(recipe)
            recipe['img'] = (pg.image.load(path.join(img_dir, recipe['pic'])).convert_alpha())                    
            if recipe_id == select_recipe['id']:
                self.select(i)
        
    def clear(self):
        self.cells.clear()
        
    def view_recipe_info(self):
        mouse_pos = pg.mouse.get_pos()
        cell_num, recipe, is_hover = self.get_cell(mouse_pos)
        if cell_num is None: return
        if recipe is None: return
        name = recipe['name']
        self.app.info.append_text(f'Рецепт: {name}')
        self.app.info.append_pic(recipe['img'])
        if 'in' in dict.keys(recipe):
            self.app.info.append_text('Вход:')
            self.app.info.append_list_items(recipe['in'])
        if 'out' in dict.keys(recipe):
            self.app.info.append_text('Выход:')
            self.app.info.append_list_items(recipe['out'])
        process = recipe['time']
        self.app.info.append_text(
            f'Производство: {process:0.1f} сек')
        
            
            