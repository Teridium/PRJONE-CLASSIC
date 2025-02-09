from random import randint
import numpy as np
import pygame as pg
import pygame_gui as gui
from mouse import *
from myui import UIItemsList, myUIImage
from options import *

class UI_tech_blueprints:
    def __init__(self, app):
        self.app = app
        self.visible = False
        self.keypressed = False
        self.wnd = None
        self.create_wnd()

    def create_wnd(self, visible=False):
        self.wnd = gui.elements.UIWindow(pg.Rect(TECH_WND_RECT), 
                                         self.app.manager,
                                         'Чертежи технологий:',
                                         visible=visible,
                                         )
        
    def hide(self):
        self.wnd.hide()
        self.visible = False
        
    def update(self):
        if not self.app.is_modal(self): return
        
        keystate = pg.key.get_pressed()
        if keystate[pg.K_b]:
            if not self.keypressed:
                self.keypressed = True
                if not self.wnd.visible:
                    self.wnd.show()
                    self.app.player.is_openinv = False
                else:
                    self.wnd.hide()
                self.visible = bool(self.wnd.visible)
        else:
            self.keypressed = False



        
            
        
    def draw(self):
        pass
    
class ui_tech:
    def __init__(self, app):
        self.app = app
        
        self.enabled = True
        self.first_pressed = [False, False, False]
        
        self.area = pg.Rect(0,0,0,0)
        self.start = self.area
        self.allow = True
        self.on_click_delete_button = None
        self.control_buttons = []
        
        self.tech_sites = tech_sites(self.app)
        self.bg_blue = pg.Surface((TILE,TILE), pg.SRCALPHA)
        pg.draw.rect(self.bg_blue, pg.Color(64,128,255,128), (0,0,TILE, TILE))
        self.bg_red = pg.Surface((TILE,TILE), pg.SRCALPHA)
        pg.draw.rect(self.bg_red, pg.Color(255,32,128,128), (0,0,TILE, TILE))
        self.wnd = gui.elements.UIWindow(pg.Rect(TECHINFO_WND_RECT), 
                                         self.app.manager,
                                         'Технология:',
                                         visible=False,
                                         object_id='tech_wnd'
                                         )        
        
        self.info_img = None 
        self.info_name = None
        self.info_text = None
        self.in_img = None
        self.out_img = None
        self.in_text = None
        self.out_text = None
        self.ok_button = None
        self.turn_text = None
        self.detect_text = None
        self.operate_text = None
        
    @property
    def selected_site(self):
        if self.tech_sites.selected_site:
            if self.tech_sites.selected_site.status != TECH_A_DELETE:
                return self.tech_sites.selected_site
        return None

    @property
    def selected_factory(self):
        return self.app.factories.selected


    def site(self, num):
        return self.tech_sites.get_by_num(num)
        
        
    def process_events(self, event):
        if event.type == pg.USEREVENT:
            if event.user_type == gui.UI_BUTTON_PRESSED:
                if self.control_buttons:
                    if event.ui_object_id == 'panel.panel_info.del_button': 
                        self.tech_sites.delete_selected()
                    elif event.ui_object_id == 'panel.panel_info.run_button': 
                        self.tech_sites.start_research_selected()
                    elif event.ui_object_id == 'panel.panel_info.view_tech_button': 
                        # show tech window
                        self.show_tech_selected()
                        # open tech
                        self.tech_sites.open_research_selected()
                        # remove lab
                        self.tech_sites.delete_selected()
                    elif event.ui_object_id == 'panel.panel_info.chg_recipe_button':
                        if self.app.inv_recipe.is_open: return
                        self.show_recipes()
                if event.ui_element == self.ok_button:
                    self.wnd.hide()
                    self.app.clear_modal()
                    
    def show_recipes(self):
        self.app.inv_recipe.load_recipe(self.selected_factory.allow_recipe_list, self.selected_factory.recipe)
        self.app.inv_recipe.is_open = True

    def show_tech_selected(self):
        self.app.set_modal(self.wnd)
        
        if not self.selected_site: return
        
        bp_id = self.selected_site.blueprint_id
        
        bp = self.app.terrain.data['factory_type'][bp_id]

        if 'use_recipes' in bp.keys():
            rp = self.app.terrain.data['recipes'][bp['use_recipes']['selected_id']]
        else:
            rp = None
         
        wnd_width = self.wnd.get_relative_rect().width-self.wnd.border_width*2-self.wnd.shadow_width*2
        pos = 0
        paddind = (10,0,10,0)
        pic = self.app.factories.factory_img[bp_id]
        pic_size = pic.get_size()
        if self.info_img:
            self.info_img.set_image(pic)
            self.info_img.set_relative_position((wnd_width//2-pic_size[0]//2,pos))
            pos += self.info_img.get_relative_rect().h
        else:
            self.info_img = myUIImage(pg.Rect((wnd_width//2-pic_size[0]//2,pos),pic_size), pic, self.app.manager, container=self.wnd)
            pos += self.info_img.get_relative_rect().h
            
        name = bp['name']
        if self.info_name:
            self.info_name.set_text(name)
            self.info_name.set_relative_position((0,pos))
            pos += self.info_name.get_relative_rect().h
        else:
            self.info_name = gui.elements.UILabel(pg.Rect(0,pos,wnd_width,-1), name, self.app.manager, container=self.wnd)
            pos += self.info_name.get_relative_rect().h

        info_text = bp.get('info')
        if info_text:
            if self.info_text:
                self.info_text.set_text(info_text)
                self.info_text.set_relative_position((0, pos))
                pos += self.info_text.get_relative_rect().h
            else:
                self.info_text = gui.elements.UITextBox(
                    info_text, 
                    pg.Rect(0,pos,wnd_width,-1), 
                    self.app.manager, 
                    container=self.wnd, 
                    wrap_to_height=True,
                    object_id='wnd_info_text')
                pos += self.info_text.get_relative_rect().h
        elif self.info_text:
            self.info_text.kill()
            self.info_text = None

        if rp:
            res_in = rp.get('in')
        else:
            res_in = None
        if res_in:
            if self.in_text:
                self.in_text.set_relative_position((paddind[0],pos))
                pos += self.in_text.get_relative_rect().h
                self.in_img.set_items_list(self.app.info._create_items_list(res_in))
                self.in_img.set_relative_position((paddind[0],pos))
                pos += self.in_img.get_relative_rect().h
            else:
                self.in_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), 'Вход:', self.app.manager, container=self.wnd, object_id='label_left')
                pos += self.in_text.get_relative_rect().h
                self.in_img = UIItemsList(pg.Rect(paddind[0],pos,-1,-1), self.app.info._create_items_list(res_in), self.app.manager, container=self.wnd, object_id='item_label_m')
                pos += self.in_img.get_relative_rect().h
        elif self.in_text:
            self.in_text.kill()
            self.in_text = None
            self.in_img.kill()
            self.in_img = None

        if rp:
            res_out = rp.get('out')
        else:
            res_out = None
        if res_out:
            if self.out_text:
                self.out_text.set_relative_position((paddind[0],pos))
                pos += self.out_text.get_relative_rect().h
                self.out_img.set_items_list(self.app.info._create_items_list(res_out))
                self.out_img.set_relative_position((paddind[0],pos))
                pos += self.out_img.get_relative_rect().h
            else:
                self.out_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), 'Выход:', self.app.manager, container=self.wnd, object_id='label_left')
                pos += self.out_text.get_relative_rect().h
                self.out_img = UIItemsList(pg.Rect(paddind[0],pos,-1,-1), self.app.info._create_items_list(res_out), self.app.manager, container=self.wnd, object_id='item_label_m')
                pos += self.out_img.get_relative_rect().h
        elif self.out_text:
            self.out_text.kill()
            self.out_text = None
            self.out_img.kill()
            self.out_img = None

        if rp:
            turn = rp.get('time')
        else:
            turn = None
        if turn:
            if self.turn_text:
                self.turn_text.set_text(f'Производственный цикл (сек): {turn}')
                self.turn_text.set_relative_position((paddind[0],pos))
                pos += self.turn_text.get_relative_rect().h
            else:
                self.turn_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), f'Производственный цикл (сек): {turn}', self.app.manager, container=self.wnd, object_id='label_left')
                pos += self.turn_text.get_relative_rect().h
        elif self.turn_text:
            self.turn_text.kill()
            self.turn_text = None
        
        detect = bp.get('detect')
        if detect:
            if self.detect_text:
                self.detect_text.set_text(f'Радар: {detect}')
                self.detect_text.set_relative_position((paddind[0],pos))
                pos += self.detect_text.get_relative_rect().h
            else:
                self.detect_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), f'Радар: {detect}', self.app.manager, container=self.wnd, object_id='label_left')
                pos += self.detect_text.get_relative_rect().h
        elif self.detect_text:
            self.detect_text.kill()
            self.detect_text = None
        
        operate = bp.get('operate')
        if operate:
            if self.operate_text:
                self.operate_text.set_text(f'Управление: {operate}')
                self.operate_text.set_relative_position((paddind[0],pos))
                pos += self.operate_text.get_relative_rect().h
            else:
                self.operate_text = gui.elements.UILabel(pg.Rect(paddind[0],pos,wnd_width-paddind[2]-paddind[0],-1), f'Управление: {operate}', self.app.manager, container=self.wnd, object_id='label_left')
                pos += self.operate_text.get_relative_rect().h
        elif self.operate_text:
            self.operate_text.kill()
            self.operate_text = None
        


        if not self.ok_button:
            ok_rect = pg.Rect(paddind[0],0,wnd_width-paddind[2]-paddind[0],-1)
            ok_rect.bottomright = (-10,-10)
            self.ok_button = gui.elements.UIButton(ok_rect,'OK', self.app.manager, container=self.wnd, 
                                                   anchors={'left': 'right',
                                                            'right': 'right',
                                                            'top': 'bottom',
                                                            'bottom': 'bottom'})
            pos += self.ok_button.get_relative_rect().h
            
        self.wnd.show()

    def view_terrain_info(self, tilepos):
        # self.app.info.debug((0,10),)
        if not pg.Rect(VIEW_RECT).collidepoint(self.app.mouse.pos): return

        if not tilepos:
            pic_idx = self.app.terrain.FindTInfo('id', 'hyperspace')
            data = self.app.terrain.GetInfo('name', pic_idx)
            # self.app.info.set(self.text, pic_idx)
            self.app.info.append_pic(self.app.terrain.field_img[pic_idx][0])
            self.app.info.append_text(f'<b>{data}</b><br>(???,???)')
            return

        if self.app.terrain.dark_cover[tilepos]:
            self.app.info.append_text(f'Территория не открыта')
            return

        select_terrain = self.app.terrain.field[tilepos[0], tilepos[1]]
        select_building = self.app.terrain.building_map[tilepos[0], tilepos[1]]

        terrain_data = self.app.terrain.GetTData('id', select_terrain)
        terrain_name = terrain_data['name']
        terrain_pic = self.app.terrain.field_img[select_terrain][0]

        self.app.info.append_pic(terrain_pic)
        self.app.info.append_text(f'<b>{terrain_name}</b><br>{tilepos}</b>')

        if strtobool(self.app.terrain.GetTileInfo('allow_dig', tilepos)) and select_building == 0:
            time = terrain_data['dig']['time']
            loot = terrain_data['dig']['loot']
            self.app.info.append_text('Ожидаемые ресурсы:')
            self.app.info.append_list_items(loot)
            self.app.info.append_text(f'Время добычи(сек): {time}')

        if select_building > 0:
            block_data = self.app.terrain.GetBData('id', select_building)
            block_name = block_data['name']
            time = block_data['demolition']
            loot = select_building
            lootcount = 1
            self.app.info.append_item(
                {'id': select_building, 'count': -1}, justify='center')
            self.app.info.append_text(f'<b>{block_name}</b>')
            self.app.info.append_text('Ресурсы при разборе:')
            self.app.info.append_item(
                {'id': loot, 'count': lootcount}, 'item_label_m')
            self.app.info.append_text(f'Время разбора(сек): {time}')


    def view_tech_site_ui(self):
        if self.selected_site is None: return
        if self.selected_site.status != TECH_A_DELETE:
            self.app.info.append_text(f'Лаборатория: {self.selected_site.name}')
            # self.app.info.append_pic(self.selected_site.pic)    
            self.app.info.append_text(f' - размер: {self.selected_site.rect.size}')
        if self.selected_site.status == TECH_A_NEW or self.selected_site.status == TECH_A_RESULT:
            if self.selected_site.resource_research:
                self.app.info.append_text(f'Стоимость исследования:')
                self.app.info.append_list_items(self.selected_site.resource_research)
                process_time_sec = self.selected_site.process_time/1000
                self.app.info.append_text(f'Время исследования(сек):{process_time_sec:10.3f}')
                
            buttons_line = []
            buttons_line.append({'text':'Удалить', 'id':'del_button'})
            if self.selected_site.resource_research:
                buttons_line.append({'text':'Запуск', 'id':'run_button'})
            self.control_buttons = self.app.info.append_buttons_line(buttons_line)
            # button = get_button_by_text('Запуск')
        if self.selected_site.status == TECH_A_PROGRESS:
            self.app.info.append_progress_bar(self.selected_site.progress)
        if self.selected_site.status == TECH_A_COMPLETE:
            self.app.info.append_text(f'Технология исследована:')
            buttons_line = []
            buttons_line.append({'text':'Посмотреть', 'id':'view_tech_button'})
            self.control_buttons = self.app.info.append_buttons_line(buttons_line)
    
    def view_factories_ui(self, tile_pos):
        if self.selected_factory is None: 
            select_factory = self.app.factories.factory(tile_pos)
            if not select_factory: return
        else:
            select_factory = self.selected_factory
        self.app.info.append_pic(self.app.data.factory_img[select_factory.pic_id])
        self.app.info.append_progress_bar(select_factory.progress)
        if select_factory.working:
            working_text = '(Работает)'
        else:
            working_text = '(Не работает)'

        self.app.info.append_text(
            f'<b>{select_factory.name}</b>{working_text}')
        if select_factory.incom:
            self.app.info.append_text('Вход:')
            self.app.info.append_list_items(select_factory.incom)
        if select_factory.outcom:
            self.app.info.append_text('Выход:')
            self.app.info.append_list_items(select_factory.outcom)
        if select_factory.process_time:
            process_time_sec = select_factory.process_time/1000
            self.app.info.append_text(
                f'Производство: {process_time_sec:0.1f} сек')

        if len(select_factory.allow_recipe_list)>1:
            buttons_line = []
            buttons_line.append({'text':'Рецепт', 'id':'chg_recipe_button'})
            self.control_buttons = self.app.info.append_buttons_line(buttons_line)

        
        self.app.info.append_text(
            f'Разборка: {select_factory.demolition} сек')
        if select_factory.demolition_list_items_100:
            # self.app.info.append_text('Ресурсы при разборе:')
            self.app.info.append_list_items(
                select_factory.demolition_list_items_100)
        if select_factory.detect:
            self.app.info.append_text(
                f'Радар: {select_factory.detect} 10м')
        if select_factory.operate:
            self.app.info.append_text(
                f'Операционный радиус: {select_factory.operate} 10м')

    def update(self):
        
        if not self.app.is_modal(self): return
        
        self.tech_sites.update()
        keystate = pg.key.get_pressed()
        
        if  (self.app.ui_tech_bp.visible or
            self.app.player.is_openinv):
            return
        
        mouse_button = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        mouse_tile_pos = self.app.terrain.mapping(mouse_pos)
        if not mouse_tile_pos: return

# start info
        self.app.info.start()

        if self.selected_site:
            self.view_tech_site_ui()
        if self.app.factories.selected:
            self.view_factories_ui(mouse_tile_pos)

        if not self.selected_site and not self.app.factories.selected:
            self.view_tech_site_ui()
            self.view_factories_ui(mouse_tile_pos)
            self.view_terrain_info(mouse_tile_pos)
        
        self.app.inv_recipe.view_recipe_info()



        self.app.info.stop()
# stop info
        if not mouse_button[0]:
            if mouse_button[2] and not self.first_pressed[2]:
                # Rigth mouse button
                # first push button
                self.first_pressed[2] = True
                self.area.topleft = mouse_tile_pos
                self.area.size = (1,1)
                self.tech_sites.unselect()
                self.app.factories.unselect()

                
            elif self.first_pressed[2] and not mouse_button[2]:
                # release button
                self.first_pressed[2] = False
                if self.area.size==(1,1):
                    # click to cell
                    click_area_screen = pg.Rect((0,0),mouse_pos)
                    if click_area_screen.colliderect(VIEW_RECT):
                        self.enabled = False
                        self.app.mouse.setcursor(cursor_type.normal)

                else:
                    # add area
                    # if self.allow:
                        # content = self.app.terrain.building_map[self.area.left:self.area.right,
                        #                             self.area.top:self.area.bottom]
                        # self.tech_sites.add(self.area, content)
                    self.area = pg.Rect(0,0,0,0)
            elif mouse_button[2]:
                # on drag
                pass
                # self.area.left = min(mouse_tile_pos[0], self.start.left)
                # self.area.top = min(mouse_tile_pos[1], self.start.top)
                # self.area.size = (abs(self.start.left-mouse_tile_pos[0])+1, abs(self.start.top-mouse_tile_pos[1])+1)
                # self.allow = (self.area.collidelist(self.app.factories.rect_list_all)==-1)
                # self.allow = self.allow and (self.area.collidelist(self.tech_sites.rect_list_all)==-1)
                # lookup = self.app.terrain.operate[self.area.left:self.area.right, self.area.top:self.area.bottom]
                # self.allow = self.allow and np.min(lookup)
            
            

        if not mouse_button[2]:
            if mouse_button[0] and not self.first_pressed[0]:
                # first push button
                self.first_pressed[0] = True
                self.area.topleft = mouse_tile_pos
                self.area.size = (1,1)
                self.start = self.area.copy()
            elif self.first_pressed[0] and not mouse_button[0]:
                # release button
                self.first_pressed[0] = False
                if self.area.size==(1,1):
                    # click to cell
                    click_area_screen = pg.Rect((0,0),mouse_pos)
                    if click_area_screen.colliderect(VIEW_RECT):
                        area_num = self.area.collidelist(self.tech_sites.rect_list_all)
                        factory_num = self.area.collidelist(self.app.factories.rect_list_all)
                        if area_num!=-1: 
                            self.app.factories.unselect()
                            self.tech_sites.select(area_num)
                        if factory_num!=-1: 
                            self.tech_sites.unselect()
                            self.app.factories.select(factory_num)
                            

                else:
                    # add area
                    if self.allow:
                        content = self.app.terrain.building_map[self.area.left:self.area.right,
                                                    self.area.top:self.area.bottom]
                        self.tech_sites.add(self.area, content)
                        self.app.factories.unselect()
                    self.area = pg.Rect(0,0,0,0)

            elif mouse_button[0]:
                # on drag
                self.area.left = min(mouse_tile_pos[0], self.start.left)
                self.area.top = min(mouse_tile_pos[1], self.start.top)
                self.area.size = (abs(self.start.left-mouse_tile_pos[0])+1, abs(self.start.top-mouse_tile_pos[1])+1)
                self.allow = (self.area.collidelist(self.app.factories.rect_list_all)==-1)
                self.allow = self.allow and (self.area.collidelist(self.tech_sites.rect_list_all)==-1)
                lookup = self.app.terrain.operate[self.area.left:self.area.right, self.area.top:self.area.bottom]
                self.allow = self.allow and np.min(lookup)
            
    def draw(self, surface):
        self.tech_sites.draw(surface)
        
        # draw cursor area
        if self.area.size!=(1,1):
            for i in range(self.area.left, self.area.right):
                for j in range(self.area.top, self.area.bottom):
                    screen_pos = self.app.terrain.demapping((i,j))
                    f_rect = pg.Rect(screen_pos, (TILE, TILE))
                    if self.allow:
                        surface.blit(self.bg_blue, f_rect.topleft)
                    else:
                        surface.blit(self.bg_red, f_rect.topleft)
        
    def refresh_site_content(self, tile_pos):
        
        self.area.topleft = tile_pos
        self.area.size = (1,1)

        area_num = self.area.collidelist(self.tech_sites.rect_list_all)
        if area_num>-1:
            tech_site = self.tech_sites.get_by_num(area_num)
            content = self.app.terrain.building_map[tech_site.rect.left:tech_site.rect.right,
                                        tech_site.rect.top:tech_site.rect.bottom]
            tech_site.refresh(content)

        ui_tech.area = pg.Rect(0,0,0,0)                  
    
        

class tech_sites:
    
    def __init__(self, app):
        self.app = app
        self.list = []
        self.active = None
        # load pic resources 
        self.img = [0 for i in self.app.img_res['tech-ui_img']]
        for img in self.app.img_res['tech-ui_img']:
            self.img[img['id']] = (pg.image.load(
                path.join(img_dir, img['pic'])).convert_alpha())

        ss = spritesheet(surface=self.img[self.get_img_data('name', 'mark')['id']])
        self.img_mark = ss.images_slice(3,1)
        # self.img_mark = ss.load_strip(pg.Rect(0,0,64,64), 2)
        
            
        self.data = app.terrain.data['factory_type']
        # self.selected_site = None
        # close bp all factory 
        for item in self.data:
            item['open'] = False #debug: set on False after
            
    def get_img_data(self, key, stroke):
        for item in self.app.img_res['tech-ui_img']:
            if item[key] == stroke:
                return(item)



    @property
    def rect_list_all(self):
        f_list = []
        for item in self.list:
            f_list.append(item.rect)
        return f_list
    
    @property
    def selected_site(self):
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
    
    def add(self, area, content):
        # print(f'{area}')
        t_site = tech_area(self, self.app, area.copy(), content)
        self.active = t_site
        self.list.append(t_site)
        return t_site
    
    def delete_selected(self):
        self.list.remove(self.active)
        self.active.delete()
        
    def draw(self, surface):
        # self.app.info.start
        # for img in self.img_mark:
        #     self.app.info.append_pic(img, justify='left')
        # self.app.info.stop
        
        
        for item in self.list:
            item.draw(surface)
    
    def update(self):
        for item in self.list:
            item.update()
    
    def start_research_selected(self):
        if self.active:
            self.active.start_research()
    
    def open_research_selected(self):
        if not self.active: return
        self.active.open_research()


    
class tech_area:
    def __init__(self, list, app, rect, content):
        self.rect = rect
        self.app = app
        self.list = list
        self.result = np.zeros(rect.size, dtype=np.integer)
        self.result_bool = np.zeros(rect.size, dtype=np.bool_)
        
        
        self.content = np.array(content)
        self.resource_research, self.process_time = self.calc_resource_research()

        self.pic = self.create_pic(is_select=False)
        self.pic_selected = self.create_pic(is_select=True)
        self.complete_pic = self.create_complete_pic()
        self.result_pic = None
        num = randint(0,99999999)
        self.name = f'lab{num:0>8d}'
        self.status = TECH_A_NEW
        self.blueprint_id = None
        self.complete_procent = 0
        self.timer = app.timer
        self.time_start = 0
        
        self.scan_ani_pos = 0
        
    def draw(self, surface):
        screen_pos = self.app.terrain.demapping(self.rect.topleft)
        a_rect = pg.Rect(screen_pos, (self.rect.size[0]*TILE, self.rect.size[1]*TILE))
        if pg.Rect(VIEW_RECT).colliderect(a_rect):
            if self.list.selected_site!=self:
                surface.blit(self.pic, a_rect)
            else:
                surface.blit(self.pic_selected, a_rect)
            if self.status==TECH_A_RESULT:
                surface.blit(self.result_pic, a_rect)
                
            if self.status==TECH_A_PROGRESS:
                pg.draw.line(surface, pg.Color(0,189,243,255), (a_rect.left, self.scan_ani_pos+a_rect.top), (a_rect.right, self.scan_ani_pos+a_rect.top), 3)
                self.scan_ani_pos += 1
                if self.scan_ani_pos+a_rect.top>a_rect.bottom: 
                    self.scan_ani_pos = 0
                    
            if self.status==TECH_A_COMPLETE:
                surface.blit(self.complete_pic, a_rect)
            
    def delete(self):
        del self.result
        del self.content
        del self.pic
        del self.pic_selected
        self.status = TECH_A_DELETE
        
    def create_result_pic(self):
        pic = pg.Surface((self.rect.size[0]*TILE, self.rect.size[1]*TILE), flags=pg.SRCALPHA)
        pg.Surface.fill(pic, pg.Color(0,255,0,64))
        for j in range(0,(self.rect.h)*TILE, TILE):
            for i in range(0,(self.rect.w)*TILE, TILE):
                a_rect = pg.Rect((i,j), (TILE,TILE))  
                tile = self.result[i//TILE][j//TILE]
                if tile!=0:
                    # pic.blit(self.list.img[1], a_rect)  
                    
                    pic.blit(self.list.img_mark[tile-1], a_rect)  
        return pic
        
    def create_complete_pic(self):
        pic = pg.Surface((self.rect.size[0]*TILE, self.rect.size[1]*TILE), flags=pg.SRCALPHA)
        pg.Surface.fill(pic, pg.Color(0,255,0,64))
        for j in range(0,(self.rect.h)*TILE, TILE):
            for i in range(0,(self.rect.w)*TILE, TILE):
                a_rect = pg.Rect((i,j), (TILE,TILE))  
                pic.blit(self.list.img_mark[2], a_rect)  
        return pic
        
        
    def create_pic(self, is_select):
        pic = pg.Surface((self.rect.size[0]*TILE, self.rect.size[1]*TILE), flags=pg.SRCALPHA)
        
        if is_select: 
            pic_res = 0
            pg.Surface.fill(pic, pg.Color(64,128,255,64))
            
        else:
            pic_res = 3
            pg.Surface.fill(pic, pg.Color(128,128,128,128))
            
        down_img = pygame.transform.rotate(self.list.img[pic_res], 180)
        left_img = pygame.transform.rotate(self.list.img[pic_res], 270)
        rigth_img = pygame.transform.rotate(self.list.img[pic_res], 90)
        tr_img = pygame.transform.rotate(self.list.img[1], 90)
        br_img = pygame.transform.rotate(self.list.img[1], 180)
        bl_img = pygame.transform.rotate(self.list.img[1], 270)
        for i in range(TILE,(self.rect.w-1)*TILE, TILE):
            a_rect = pg.Rect((i,0), self.rect.size)
            pic.blit(self.list.img[pic_res], a_rect)
            b_rect = pg.Rect((i,(self.rect.h-1)*TILE), self.rect.size)
            pic.blit(down_img, b_rect)
            
        for j in range(TILE,(self.rect.h-1)*TILE, TILE):
            a_rect = pg.Rect((0,j), self.rect.size)
            pic.blit(rigth_img, a_rect)
            b_rect = pg.Rect(((self.rect.w-1)*TILE,j), self.rect.size)
            pic.blit(left_img, b_rect)
            
        c_rect = pg.Rect((0,0), self.rect.size)
        pic.blit(self.list.img[1], c_rect)
        c_rect = pg.Rect(((self.rect.w-1)*TILE,0), self.rect.size)
        pic.blit(bl_img, c_rect)
        c_rect = pg.Rect(((self.rect.w-1)*TILE,(self.rect.h-1)*TILE), self.rect.size)
        pic.blit(br_img, c_rect)
        c_rect = pg.Rect((0,(self.rect.h-1)*TILE), self.rect.size)
        pic.blit(tr_img, c_rect)
        return pic

    def refresh(self, content):
        self.content = content.copy()
        self.resource_research, self.process_time = self.calc_resource_research()
        
    def calc_resource_research(self):
        result=[]
        process_time = 0
        res, count = np.unique(self.content, return_counts=True)
        for i,id in enumerate(res):
            if id==0: continue
            if count[i]==0: continue
            result.append({'id':id, 'count':count[i]})
            process_time += count[i]*5*1000
        return result, process_time
    
    def start_research(self):
        if not self.app.player.inv.exist(self.resource_research):
            return
        self.app.player.inv.delete(self.resource_research)
        self.status = TECH_A_PROGRESS
        self.time_start = self.timer.get_ticks()

    def open_research(self):
        for item in self.list.data:
            if item['id']==self.blueprint_id:
                item['open'] = True   
                return     

    @property
    def progress(self):
        if self.status==TECH_A_PROGRESS:
            now = self.timer.get_ticks()
            return(((now-self.time_start)/self.process_time))      
        elif self.status==TECH_A_RESULT:
            return(100)
        else:
            return(0)
    
    def update(self):
        if self.status == TECH_A_NEW:
            pass
        elif self.status == TECH_A_PROGRESS:
            if self.timer.get_ticks()-self.time_start>self.process_time:
                # research done, generate result
                self.status = TECH_A_RESULT
                self.calc_result()
        elif self.status == TECH_A_RESULT:
            if self.complete_procent == 100:
                self.status = TECH_A_COMPLETE    
        elif self.status == TECH_A_COMPLETE:
            pass

    def get_similar_plans(self, content, blueprints):
    # get similar plan by content
        shape = content.shape
        max = -1 
        complete = 0
        result_bool = None
        blueprint_id = None
        for bp in blueprints:
            if bp['open']: continue
            if bp['dim']['w']!=shape[0] or bp['dim']['h']!=shape[1]: continue
            if not bp.get('plan'): continue
            _res = (np.transpose(bp['plan'])==content)
            sum = _res.sum()
            if sum > max:
                max = sum
                result_bool = _res
                blueprint_id = bp['id']
        if result_bool is None:
            result_bool = (False==content)
            result_bool.fill(False)
        else: complete = round(max/(shape[0]*shape[1])*100)
        return result_bool, blueprint_id, complete

    def calc_result(self):
        # calc result array for check research
        # self.content
        # self.result
        # self.list.data - bp
        
        if self.blueprint_id==None:
            self.result_bool, self.blueprint_id, self.complete_procent = self.get_similar_plans(self.content, self.list.data)
        else:
            self.result_bool = (np.transpose(self.list.data[self.blueprint_id]['plan'])==self.content)
            self.complete_procent = round(self.result_bool.sum()/np.count_nonzero(self.list.data[self.blueprint_id]['plan'])*100)
            
        # rebuild result
        # 0 - none 
        # 1 - wrong
        # 2 - right

        for i, row in enumerate(self.result_bool):
            for j, val in enumerate(row):
                if self.result_bool[i][j]:
                    self.result[i][j]=2
                else:
                    self.result[i][j]=1
                    
        self.result_pic = self.create_result_pic()
                    
