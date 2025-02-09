from ast import Str
from turtle import onclick
from numpy.lib.function_base import append, select
import pygame as pg
import pygame_gui as gui
from options import *
from utils import set_proportion_by_frame
from myui import *

class info:

    def __init__(self, app):
        self.app = app
        self.msg_text = ''
        # self.surface = pg.Surface(WIN_SIZE)
        pg.font.init()
        #self.win_info = gui.elements.UIWindow(pg.Rect((0, 0), (SC_WIDTH, SC_HIGHT)), self.app.manager)
        self.main_panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((FIELD_WIDTH, 0), (P_INFO, SC_HIGHT)),
                                                    starting_layer_height=0,
                                                    manager=self.app.manager,
                                                    margins={
                                                        'left': 0, 'top': 3, 'right': 0, 'bottom': 3}
                                                    # container=self.win_info
                                                    )

        self.map_panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((0, 0), (P_INFO, 320)),
                                                   starting_layer_height=0,
                                                   manager=self.app.manager,
                                                   margins={
                                                       'left': 0, 'top': 3, 'right': 0, 'bottom': 3},
                                                   container=self.main_panel_info,
                                                   element_id='map_info'
                                                   )

        self.panel_info = gui.elements.UIPanel(relative_rect=pg.Rect((0, 320), (P_INFO, SC_HIGHT-320)),
                                               starting_layer_height=0,
                                               manager=self.app.manager,
                                               margins={
                                                   'left': 0, 'top': 3, 'right': 0, 'bottom': 3},
                                               container=self.main_panel_info,
                                               element_id='panel_info'
                                               )

        # self.text_rect = pg.Rect((0, 64), (INFO_WIDTH, 150))
        # text
        # pic pic.rect
        # list items [{'id:1, 'count':45},{'id':12, 'count':1},{'id':1, 'count':1}]

        self.msg_line = 0
        self.top = 0
        self.msg_info_list = []
        # gui.elements.UITextBox(
        # f'',
        # relative_rect=self.text_rect, manager=self.app.manager, container=self.panel_info, object_id='textinfo')
        # self.start_button = gui.elements.UIButton(relative_rect=self.text_rect,
        #                                                 text='Start',
        #                                                 manager=self.app.manager)

        # self.pic_rect = pg.Rect((0+INFO_WIDTH//2-63//2, 0), (63, 63))
        # self.pic_info = gui.elements.UIImage(self.pic_rect,  self.app.terrain.field_img[0], self.app.manager, container=self.panel_info)

        # debuf info
        self.debug_font = pg.font.SysFont('times', 14, True)
        self.debug_textlist = []

        # self.panels = []
        # self.panels.append(self.building_panel_info)
        # self.panels.append(self.terrain_panel_info)

    def start(self):
        self.msg_line = 0
        self.top = 0

    def stop(self):
        if self.msg_line > len(self.msg_info_list)-1:
            return
        while self.msg_line < len(self.msg_info_list):
            item = self.msg_info_list.pop()
            item['ui'].kill()
            # self.app.manager
            del item['ui']
        self.msg_line = 0
        self.top = 0
        # self.panel_info.rebuild()

    def update(self):
        pass


    def draw(self):
        # self.surface.fill(pg.Color(255,0,0))
        for item in self.debug_textlist:
            self.text_surface = self.debug_font.render(item['text'], True, (255, 0, 0))
            self.app.screen.blit(self.text_surface, item['pos'])
        self.debug_textlist.clear()

    def set(self, text, img_index):
        self.msg_text = text
        # self.text_info.html_text = f'<font face=fira_code size=4>{self.msg_text}</font>'
        # self.pic_info.set_image(self.app.terrain.field_img[img_index])

        # self.text_info.rebuild()

    def _tohtml(self, html_text):
        pass
        # top = 0
        # for list_item in self.msg_info_list:
        #     if gui.elements.UITextBox(list_item).html_text==html_text:
        #         pass
        #     else:
        #         top += gui.elements.UITextBox(list_item).rect[1]

        # self.msg_info_list.append(
        #     gui.elements.UITextBox(
        #         f'<font face=fira_code size=4>{html_text}</font>',
        #         relative_rect=self.text_rect,
        #         manager=self.app.manager,
        #         container=self.panel_info,
        #         object_id='textinfo'
        #     )
        # )

    def clear(self):
        self.msg_line = 0
        self.top = 0
        for item in self.msg_info_list:
            del item

        self.msg_info_list = []

    def debug(self, pos, text):
        debugtext = f'{text}'
        self.debug_textlist.append({'pos': pos, 'text': debugtext})
        
    def _create_text_info(self, text, top_pos):
        text_rect = pg.Rect((0, top_pos), (INFO_WIDTH, -1))
        textui = gui.elements.UITextBox(
            text,
            relative_rect=text_rect,
            wrap_to_height=True,
            manager=self.app.manager,
            container=self.panel_info,
            object_id='textinfo'
        )
        return({'ui': textui, 'type': type(textui).__name__}, textui.get_relative_rect()[3])
        
    def _create_pic_info(self, pic, top_pos, justify='center', size=None):
        if size: 
            pic_relativity_rect = pg.Rect(pic.get_rect())
            pic_relativity_rect.size = set_proportion_by_frame(pic_relativity_rect.size, size)
        else:
            pic_relativity_rect = pg.Rect(pic.get_rect())
        if justify=='left': 
            justify = 0
        elif justify=='center':
            justify = INFO_WIDTH//2-pic_relativity_rect.width//2
        pic_rect = pg.Rect((justify, top_pos), pic_relativity_rect.size)
        picui = myUIImage(
            relative_rect=pic_rect,
            image_surface=pic,
            manager=self.app.manager,
            container=self.panel_info
            
        )
        return({'ui': picui, 'type': type(picui).__name__}, picui.get_relative_rect()[3])


    def _create_button_info(self, button_text, rect, justify='center', object_id='button'):
        button_rect = pg.Rect(rect)
        if button_rect.w==-2: button_rect.w = INFO_WIDTH
        butui = gui.elements.UIButton(
            relative_rect=button_rect,
            text=button_text,
            manager=self.app.manager,
            container=self.panel_info,
            object_id=object_id
        )
        if button_rect.w<0:
            if justify=='left': 
                justify = 0
            elif justify=='center':
                justify = INFO_WIDTH//2-butui.get_relative_rect().width//2
            elif justify=='right':
                justify = INFO_WIDTH-butui.get_relative_rect().width
            butui.set_relative_position((justify,button_rect.top))
        return({'ui': butui, 'type': type(butui).__name__}, butui.get_relative_rect()[3])

    def _create_item_info(self, item, top_pos, object_id, justify):
        if justify=='left': 
            justify = 0
        elif justify=='center':
            justify = INFO_WIDTH//2-64//2
        
        item_rect = pg.Rect((justify, top_pos), (-1, -1))
        itemui= UIItem(
            relative_rect=item_rect,
            image_surface=self.app.data.data['block_type'][item['id']]['img'],
            count=item['count'],
            manager=self.app.manager,
            container=self.panel_info,
            object_id=object_id
        )
        return({'ui': itemui, 'type': type(itemui).__name__}, itemui.get_relative_rect()[3])

    def _create_items_list(self, block_list):
        list = []
        for item in block_list:
            image_surface=self.app.data.data['block_type'][int(item['id'])]['img']
            list.append({'img':image_surface, 'count': item['count']})
        return(list)
        
    def _create_items_list_info(self, block_list, top_pos):  # blocklist [{"id":"1","count:"1"},...] items: [{"img":surf, "count": int},...]
        items_list = self._create_items_list(block_list)
        items_rect = pg.Rect((0, top_pos), (-1, -1))
        itemsui= UIItemsList(
            relative_rect=items_rect,
            items_list=items_list,
            manager=self.app.manager,
            container=self.panel_info,
            object_id='item_label_m'
        )
        return({'ui': itemsui, 'type': type(itemsui).__name__}, itemsui.get_relative_rect()[3])

    def _create_progress_bar_info(self, top_pos):  
        bar_rect = pg.Rect((0, top_pos), (P_INFO, 7))
        progressui = myUIProgressBar(
            relative_rect=bar_rect,
            manager=self.app.manager,
            container=self.panel_info
            # object_id='progress_bar'
        )
        progressui.set_relative_position(bar_rect)

        return({'ui': progressui, 'type': type(progressui).__name__}, progressui.get_relative_rect()[3])


    def _create_button_list_info(self, buttons_line, top_pos):
        rect = pg.Rect((0, top_pos), (INFO_WIDTH, -1))
        butlineui = UIButtonLine(
                    relative_rect=rect,
                    buttons=buttons_line,
                    manager=self.app.manager,
                    container=self.panel_info
                )        
        return({'ui': butlineui, 'type': type(butlineui).__name__}, butlineui.get_relative_rect()[3])


    def _shift_next_position(self, delta_top):
        if delta_top==0: return
        for i in range(self.msg_line+1, len(self.msg_info_list)):
            item = self.msg_info_list[i]['ui']
            rect = item.get_relative_rect()
            item.set_relative_position((rect[0], rect[1]+delta_top))
            
            
    def append_text(self, text):
        html_text = f'<font face=fira_code size=3>{text}</font>'
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_text_info(html_text, self.top)
            self.msg_info_list.append(element)
            self.top += hight
            self.msg_line += 1
            return

        if self.msg_info_list[self.msg_line]['type'] == 'UITextBox':
            if self.msg_info_list[self.msg_line]['ui'].html_text == html_text:
                self.top += self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[
                    3]
                self.msg_line += 1
            else:
                oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[
                    3]
                self.msg_info_list[self.msg_line]['ui'].html_text = html_text
                self.msg_info_list[self.msg_line]['ui'].rebuild()
                newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[
                    3]
                dtop = newtop - oldtop
                self._shift_next_position(dtop)
                self.top += newtop
                self.msg_line += 1

        else:
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[
                    3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']

            element, newtop = self._create_text_info(html_text, self.top)
            self.msg_info_list[self.msg_line] = element

            dtop = newtop - oldtop
            self.top += newtop
            self._shift_next_position(dtop)             
            self.msg_line += 1

    
    def append_pic(self, pic, justify='center', size=None):
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_pic_info(pic, self.top, justify=justify)
            self.msg_info_list.append(element)
            self.top += hight
            self.msg_line += 1
            return          
        
        if self.msg_info_list[self.msg_line]['type'] == 'UIImage':
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].set_image(pic)
            newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            dtop = newtop - oldtop
            self.top += newtop
            self._shift_next_position(dtop)
            self.msg_line += 1
        else:
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']
            

            element, newtop = self._create_pic_info(pic, self.top, justify=justify, size=size)
            self.msg_info_list[self.msg_line] = element
            self.top += newtop
            dtop = newtop - oldtop
            self._shift_next_position(dtop)
            self.msg_line += 1
        

    def append_item(self, item, object_id='item_label_b', justify='left'):
        item_pic = self.app.data.data['block_type'][item['id']]['img']
        item_count = item['count']
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_item_info(item, self.top, object_id, justify)
            self.msg_info_list.append(element)
            self.top += hight
            self.msg_line += 1
            return          

        if self.msg_info_list[self.msg_line]['type'] == 'UIItem':
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].set_item(item_pic, item_count)
            newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            dtop = newtop - oldtop
            self.top += newtop
            self._shift_next_position(dtop)
            self.msg_line += 1
        else: 
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']

            element, newtop = self._create_item_info(item, self.top, object_id, justify)
            self.msg_info_list[self.msg_line] = element
            self.top += newtop
            dtop = newtop - oldtop
            self._shift_next_position(dtop)
            self.msg_line += 1
     
    def append_progress_bar(self, procent):
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_progress_bar_info(self.top)
            self.msg_info_list.append(element)
            self.top += hight
            self.msg_line += 1
            return     

        if self.msg_info_list[self.msg_line]['type'] == 'myUIProgressBar':
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].set_current_progress(procent)
            newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            dtop = newtop - oldtop
            self.top += newtop
            # gui.elements.UIProgressBar.set_relative_position
            self.msg_info_list[self.msg_line]['ui'].update_containing_rect_position()
            
            if dtop:
                self._shift_next_position(dtop)
            self.msg_line += 1
        else: 
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']

            element, newtop = self._create_progress_bar_info(self.top)
            
            self.msg_info_list[self.msg_line] = element
            self.top += newtop
            dtop = newtop - oldtop
            # if dtop:
            self._shift_next_position(dtop)
            self.msg_line += 1     
        
    
    def append_list_items(self, block_list):
        # [{"id":1,"count":3},{"id":3,"count":13}...]
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_items_list_info(block_list, self.top)
            self.msg_info_list.append(element)
            self.top += hight
            self.msg_line += 1
            return     
        
        if self.msg_info_list[self.msg_line]['type'] == 'UIItemsList':
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].set_items_list(self._create_items_list(block_list))
            newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            dtop = newtop - oldtop
            self.top += newtop
            self._shift_next_position(dtop)
            
            # self.msg_info_list[self.msg_line]['ui'].rebuild()
            self.msg_line += 1
        else: 
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']

            element, newtop = self._create_items_list_info(block_list, self.top)
            self.msg_info_list[self.msg_line] = element
            self.top += newtop
            dtop = newtop - oldtop
            self._shift_next_position(dtop)
            self.msg_line += 1 
        
    def clear_info(self):
        self.app.info.start()
        # self.app.info.append_text(f'')
        self.app.info.stop()

    def append_button(self, button_text, w=-1,h=-1,justify='center', next_line=True, left=0, object_id='button'):
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_button_info(button_text, rect=(left,self.top, w,h), justify=justify, object_id=object_id)
            self.msg_info_list.append(element)
            if next_line:
                self.top += hight
                self.msg_line += 1
            return(element['ui'])
        
        if self.msg_info_list[self.msg_line]['type'] == 'UIButton':
            if self.msg_info_list[self.msg_line]['ui'].text == button_text:
                if next_line:
                    self.top += self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[
                        3]
                    self.msg_line += 1
                return(self.msg_info_list[self.msg_line-1]['ui'])
            else:            
                oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
                self.msg_info_list[self.msg_line]['ui'].set_text(button_text)
                newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
                dtop = newtop - oldtop
                self._shift_next_position(dtop)
                if next_line:
                    self.top += newtop
                    self.msg_line += 1
                return(self.msg_info_list[self.msg_line-1]['ui'])
        
        else:
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']
            

            element, newtop = self._create_button_info(button_text, rect=(self.top, left, w,h), justify=justify, object_id=object_id)
            self.msg_info_list[self.msg_line] = element
            if next_line:
                self.top += newtop
                self.msg_line += 1
            dtop = newtop - oldtop
            self._shift_next_position(dtop)

            return(element['ui'])
        
    def append_buttons_line(self, buttons_line):
        if len(self.msg_info_list) < self.msg_line+1:
            element, hight = self._create_button_list_info(buttons_line, self.top)
            self.msg_info_list.append(element)
            self.top += hight
            self.msg_line += 1
            return(element['ui'])      
        
        if self.msg_info_list[self.msg_line]['type'] == 'UIButtonLine':
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].set_buttons(buttons_line)
            newtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            dtop = newtop - oldtop
            self.top += newtop
            self._shift_next_position(dtop)
            self.msg_line += 1
            return(self.msg_info_list[self.msg_line-1]['ui'])
        else: 
            oldtop = self.msg_info_list[self.msg_line]['ui'].get_relative_rect()[3]
            self.msg_info_list[self.msg_line]['ui'].kill()
            del self.msg_info_list[self.msg_line]['ui']

            element, newtop = self._create_button_list_info(buttons_line, self.top)
            self.msg_info_list[self.msg_line] = element
            self.top += newtop
            dtop = newtop - oldtop
            self._shift_next_position(dtop)
            self.msg_line += 1
        
            return(element['ui'])        
