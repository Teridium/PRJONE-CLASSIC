import pygame as pg
import pygame_gui as gui
from options import *

class storage:
    def __init__(self, app, owner, count, list_items=[], list_allows=[]):
        '''
        app - game class
        owner - owner class
        count - cell count universal 
        list_items - add items
        where:
            {'id':1, 'count':1}
            id - id item  (-1  empty cell)
            count - item count
        list_allows - description allow to store item id
        where:
            {'id':-1, 'count':0}
            id - id item  (-1 any items)
            count - limit item count (-1 any count)
        '''
        self.app = app
        self.owner = owner
        self.count = count
        if not list_items:
            self.cell = [{'id':-1, 'count':0} for i in range(0, count)]
        else:
            self.cell = list_items.copy()

        if not list_allows:
            self.allow = [{'id':-1, 'count':-1} for i in range(0, count)]
        else:
            self.allow = list_allows.copy()
        
        self.ui = storage_ui(app, self)

    def is_allow_item(self, item):
        allow_count = -1
        find_cell = -1
        id = item['id']
        count = item['count']
        for num, allow in enumerate(self.allow):
            if self.cell[num]['id']==-1:
                if allow['id']==-1 or allow['id']==id:
                    find_cell = num
                else: 
                    continue
                if allow['count']==-1:
                    allow_count = count
                    break
                else:
                    allow_count = min(allow['count'], count)
                    break
            elif self.cell[num]['id']==id:
                find_cell = num
                if allow['count']==-1 or (allow['id']==id and allow['count']>=count+self.cell[num]['count']):
                    allow_count = count
                    break
                else:
                    allow_count = allow['count']-self.cell[num]['count']
                    break
            else: continue
        return(find_cell, allow_count)
           
    def add_items(self, list_items):
        not_fit = [] #items not fit on storage and return
        for item in list_items:
            find_cell, allow_count = self.is_allow_item(item)
            if find_cell==-1:
                self.add_item(not_fit, item)
            elif allow_count<0:
                self.add_item(not_fit, item)
            elif allow_count<item['count']:
                self.add_item_to_cell(find_cell, {'id':item['id'],'count':allow_count})
                self.add_item(not_fit, {'id':item['id'], 'count':item['count']-allow_count})
            else:
                self.add_item_to_cell(find_cell, {'id':item['id'],'count':allow_count})

        return(not_fit)
         
    def add_item_to_cell(self, num, item):
        self.cell[num] = {'id':item['id'], 'count':item['count']+self.cell[num]['count']}

    def add_item(self, list, new_item):
        for item in list:
            if item['id']==new_item['id']:
                item['count'] += new_item['count']
                return
        list.append(new_item)


    def update(self):
        self.ui.update()
    
    def draw(self):
        self.ui.draw()

class storage_ui:
    def __init__(self, app, storage):
        self.app = app
        self.storage = storage
        
    def update(self):
        pass
    
    def draw(self):
        pass


