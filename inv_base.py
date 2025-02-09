from logging import warn
from random import randrange
import pygame as pg
import pygame_gui as gui
from mouse import *
from options import *


class inv:
    def __init__(self, app, pos=(-2, -2), inv_cells=(10, 10), inv_cell_h=48, inv_margin=15, bg_color=pg.Color(33, 40, 45), bg_hover_color=pg.Color(33, 40, 65)):
        '''
        pos x = -1 - left,  -2 - center, -3 rigth, y = -1 top, -2 center, -3 left
        '''
        self.app = app

        self.selected_cell_num = None
        self.cells = []
        self.hover_cell_num = None
        self.is_open = False
        self.is_hover = False

        # calculate const position and view
        self.inv_cell_cw, self.inv_cell_ch = inv_cells
        self.inv_margin = inv_margin
        self.inv_cell_w = inv_cell_h
        self.inv_cell_h = inv_cell_h
        self.inv_cell_size = (self.inv_cell_w, self.inv_cell_h)
        self.inv_cell_count = self.inv_cell_cw * self.inv_cell_ch
        self.inv_width, self.inv_hight = self.inv_cell_w*self.inv_cell_cw + \
            (self.inv_cell_cw-1)+self.inv_margin*2, self.inv_cell_h * \
            self.inv_cell_ch+(self.inv_cell_ch-1)+self.inv_margin*2
        self.inv_size = (self.inv_width, self.inv_hight)
        self.inv_pos_x, self.inv_pos_y = pos
        if self.inv_pos_x < 0:
            if self.inv_pos_x == -1:
                self.inv_pos_x = 0
            if self.inv_pos_x == -2:
                self.inv_pos_x = FIELD_WIDTH // 2 - self.inv_width // 2
            if self.inv_pos_x == -3:
                self.inv_pos_x = FIELD_WIDTH - self.inv_width
        if self.inv_pos_y < 0:
            if self.inv_pos_y == -1:
                self.inv_pos_y = 0
            if self.inv_pos_y == -2:
                self.inv_pos_y = FIELD_HIGHT // 2 - self.inv_hight // 2
            if self.inv_pos_y == -3:
                self.inv_pos_y = FIELD_HIGHT - self.inv_hight
        self.inv_pos = (self.inv_pos_x, self.inv_pos_y)

        self.surface = pg.Surface(self.inv_size)
        self.bgimg = pg.image.load(path.join(img_dir, 'invbg.png')).convert()
        self.bgimg = pg.transform.scale(self.bgimg, self.inv_cell_size)
        
        self.bgimgactive = pg.image.load(
            path.join(img_dir, 'invbgactive.png')).convert()
        self.bgimgactive = pg.transform.scale(self.bgimgactive, self.inv_cell_size)
        
        self.bgrect = self.bgimg.get_rect()
        self.bg_color = bg_color
        self.bg_hover_color = bg_hover_color
        self.font = pg.font.Font(None, 15)

        self.first_pressed = True
        self.first_click = True

    @property
    def item(self):
        if self.selected_cell_num is None:
            return(None)
        return(self.cells[self.selected_cell_num])
    
    def unselect(self):
        if self.selected_cell_num is None: return
        self.selected_cell_num = None
        
        
    def select(self, item_num):
        if not self.cells: return
        if item_num<0 or item_num>len(self.cells): return
        self.selected_cell_num = item_num

    def get_cell(self, pos):
        pos2 = ((pos[0]-self.inv_pos_x-self.inv_margin)//(self.inv_cell_w+1),
                (pos[1]-self.inv_pos_y-self.inv_margin)//(self.inv_cell_h+1))
        cell = (pos[0]-self.inv_pos_x-self.inv_margin)//(self.inv_cell_w+1) + \
            (pos[1]-self.inv_pos_y-self.inv_margin)//(self.inv_cell_h+1) * \
            self.inv_cell_cw
        is_inv_hover = pg.Rect(self.inv_pos ,self.inv_size).collidepoint(pos)
        if cell < 0 or cell > self.inv_cell_count or pos2[0] < 0 or pos2[0] > self.inv_cell_cw-1:
            return(None, None, is_inv_hover)
        else:
            if cell > -1 and cell < len(self.cells):
                block = self.cells[cell]
            else:
                block = None
            return(cell, block, is_inv_hover)

    def get_pos(self, cell_number):
        col = cell_number % self.inv_cell_cw
        row = cell_number // self.inv_cell_cw
        return (col * (self.inv_cell_w+1) + self.inv_margin, row *(self.inv_cell_h+1)+self.inv_margin)

    def update(self):
        if not self.app.is_modal(self):
            return
        self.keystate = pg.key.get_pressed()
        self.mouse_button = pg.mouse.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()
        self.hover_cell_num, self.hover_item, self.is_hover = self.get_cell(self.mouse_pos)        
        if not self.is_open: self.is_hover = False
        
    def draw_cells(self):
        #  draw bg cells
        for i in range(self.inv_cell_count):
            pos = self.get_pos(i)
            if self.hover_cell_num == i:
                # hover
                self.surface.blit(self.bgimgactive, pos)
            else:
                # normal
                self.surface.blit(self.bgimg, pos)
        
    def draw_items(self):
        # if img_array is None: return
        i=-1
        for item in self.cells:
            i+=1
            pos = self.get_pos(i)
            # pos = (i%10*self.inv_cell_h+i%self.inv_cell_cw+self.inv_margin, i//self.inv_cell_ch*self.inv_cell_h+i//self.inv_cell_ch+self.inv_margin)
            icon_size = (self.inv_cell_size[0]*0.9, self.inv_cell_size[1]*0.9)
            item_pos = (pos[0]+(self.inv_cell_w // 2 - icon_size[0] // 2), pos[1]+(self.inv_cell_h // 2 - icon_size[1] // 2))
            #img
            pic = pg.transform.scale(item['img'], icon_size)
            self.surface.blit(pic, item_pos)
            if item==self.item:
                rect_selection = (pos, self.inv_cell_size)
                pg.draw.rect(self.surface, pg.Color('yellow'), rect_selection, 1)
        
    def draw(self):
        if not self.is_open:
            return

        if self.is_hover:
            self.surface.fill(self.bg_hover_color)
        else:
            self.surface.fill(self.bg_color)
        
        self.draw_cells()

        self.draw_items()

    def set_image(self, cell, img):
        cell['img'] = img
        
    def open(self):
        self.is_open = True
        
    def close(self):
        self.is_open = False