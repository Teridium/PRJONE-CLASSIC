from array import array
from multiprocessing.dummy import Array
from sys import flags
from typing import Iterable, Union, Tuple, Dict
from unittest import result
import utils 

import pygame
import pygame_gui

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement
from pygame_gui.core.utility import render_white_text_alpha_black_bg, basic_blit, apply_colour_to_surface


class UIItemsList(UIElement):
    
        # itemsui= UIItemsList(
        #     relative_rect=items_rect,
        #     items_list=items_list,
        #     manager=self.app.manager,
        #     container=self.panel_info,
        #     object_id='item_label_m'
        # )    
    
    def __init__(self,
                 relative_rect: pygame.Rect,
                 items_list,
                 manager: IUIManagerInterface,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 object_id: Union[ObjectID, str, None] = None,
                 anchors: Dict[str, str] = None,
                 visible: int = 1):

        super().__init__(relative_rect, manager, container,
                         starting_height=1,
                         layer_thickness=1,
                         anchors=anchors,
                         visible=visible)

        self._create_valid_ids(container=container,
                               parent_element=parent_element,
                               object_id=object_id,
                               element_id='item')
        
        self.items_list = items_list
        self.pic_size = (relative_rect.height, relative_rect.height)

        self.font = None
        self.text_colour = None
        self.padding = (5, 5)
        self.text_shadow_colour = None
        self.text_shadow = False
        self.text_shadow_size = 1
        self.text_shadow_offset = (0,0)
        self.relative_rect.size = (0,0)
        
        self.item_img_list = []
        for item in items_list:
            # new_image = pygame.surface.Surface((self.relative_rect.size),
            #                                 flags=pygame.SRCALPHA,
            #                                 depth=32)
            # new_image.fill(pygame.Color('#00000000'))
            
            item_img = pygame_gui.elements.UIImage(
                self.relative_rect,
                item['img'],
                manager=manager,
                container=container
            )
            self.item_img_list.append((item_img, item['count']))

        self.rebuild_from_changed_theme_data()        

        
    
    def rebuild_from_changed_theme_data(self):
        """
        Checks if any theming parameters have changed, and if so triggers a full rebuild of
        the element.

        """
        super().rebuild_from_changed_theme_data()
        any_changed = False

        font = self.ui_theme.get_font(self.combined_element_ids)
        if font != self.font:
            self.font = font
            any_changed = True    
            
        text_colour = self.ui_theme.get_colour_or_gradient('normal_text', self.combined_element_ids)
        if text_colour != self.text_colour:
            self.text_colour = text_colour
            any_changed = True
            
        pic_size = self.ui_theme.get_misc_data('size', self.combined_element_ids)
        if pic_size != self.pic_size and (self.pic_size[0]==-1 or self.pic_size[1]==-1):
            self.pic_size = (int(pic_size)-self.padding[0]*2, int(pic_size)-self.padding[1]*2)
            any_changed = True
        
        def tuple_extract(str_data: str) -> Tuple[int, int]:
            return int(str_data.split(',')[0]), int(str_data.split(',')[1])

        if self._check_misc_theme_data_changed(attribute_name='padding',
                                               default_value=(5, 5),
                                               casting_func=tuple_extract):
            self.pic_size = (int(pic_size)-self.padding[0]*2, int(pic_size)-self.padding[1]*2)
            any_changed = True    
            
        text_shadow_colour = self.ui_theme.get_colour('text_shadow', self.combined_element_ids)
        if text_shadow_colour != self.text_shadow_colour:
            self.text_shadow_colour = text_shadow_colour
            any_changed = True

        def parse_to_bool(str_data: str):
            return bool(int(str_data))

        if self._check_misc_theme_data_changed(attribute_name='text_shadow',
                                               default_value=False,
                                               casting_func=parse_to_bool):
            any_changed = True

        if self._check_misc_theme_data_changed(attribute_name='text_shadow_size',
                                               default_value=1,
                                               casting_func=int):
            any_changed = True

        if self._check_misc_theme_data_changed(attribute_name='text_shadow_size',
                                               default_value=1,
                                               casting_func=int):
            any_changed = True

        def tuple_extract(str_data: str) -> Tuple[int, int]:
            return int(str_data.split(',')[0]), int(str_data.split(',')[1])

        if self._check_misc_theme_data_changed(attribute_name='text_shadow_offset',
                                               default_value=(0, 0),
                                               casting_func=tuple_extract):
            any_changed = True
            
        
        if any_changed:
            self.rebuild()
        
    def kill(self):
        # self.item_count.kill()
        for item in self.item_img_list:
            item[0].kill()
            del item
        self.items_list.clear()
            
        return super().kill()

    def set_items_list(self, new_item_list):
        if new_item_list!=self.items_list:
            self.items_list=new_item_list

            # self.item_img_list.clear()

            if len(self.item_img_list)>=len(self.items_list): 
                # delete unwanted items
                for item in self.item_img_list[len(self.items_list):len(self.item_img_list)]:
                    item[0].kill()
                del self.item_img_list[len(self.items_list):len(self.item_img_list)]
                i=0
                for item in self.items_list:
                    self.item_img_list[i][0].original_image = item['img']
                    self.item_img_list[i][0].set_image(item['img'])
                    item=(self.item_img_list[i][0], int(item['count']))
                    self.item_img_list[i]=item
                    i+=1
                    
                
                
                

            if len(self.item_img_list)<len(self.items_list): 
                i=0
                for item in self.items_list:
                    if i<len(self.item_img_list):
                        self.item_img_list[i][0].original_image = item['img']
                        self.item_img_list[i][0].set_image(item['img'])
                        item=(self.item_img_list[i][0], int(item['count']))
                        self.item_img_list[i]=item
                    else:
                        item_img = pygame_gui.elements.UIImage(
                            self.relative_rect,
                            item['img'],
                            manager=self.ui_manager,
                            container=self.ui_container
                        )
                        self.item_img_list.append((item_img, item['count']))
                    i+=1
                    

                    
                

            
            self.rebuild()


    def _rebuild_shadow(self, new_image, text_render_rect, text):
        shadow_text_render = render_white_text_alpha_black_bg(self.font, text)
        apply_colour_to_surface(self.text_shadow_colour, shadow_text_render)
        for y_pos in range(-self.text_shadow_size, self.text_shadow_size + 1):
            shadow_text_rect = pygame.Rect((text_render_rect.x + self.text_shadow_offset[0],
                                            text_render_rect.y + self.text_shadow_offset[1]
                                            + y_pos),
                                           text_render_rect.size)
            basic_blit(new_image, shadow_text_render, shadow_text_rect)
        for x_pos in range(-self.text_shadow_size, self.text_shadow_size + 1):
            shadow_text_rect = pygame.Rect((text_render_rect.x + self.text_shadow_offset[0]
                                            + x_pos,
                                            text_render_rect.y + self.text_shadow_offset[1]),
                                           text_render_rect.size)
            basic_blit(new_image, shadow_text_render, shadow_text_rect)
        for x_and_y in range(-self.text_shadow_size, self.text_shadow_size + 1):
            shadow_text_rect = pygame.Rect(
                (text_render_rect.x + self.text_shadow_offset[0] + x_and_y,
                 text_render_rect.y + self.text_shadow_offset[1] + x_and_y),
                text_render_rect.size)
            basic_blit(new_image, shadow_text_render, shadow_text_rect)
        for x_and_y in range(-self.text_shadow_size, self.text_shadow_size + 1):
            shadow_text_rect = pygame.Rect(
                (text_render_rect.x + self.text_shadow_offset[0] - x_and_y,
                 text_render_rect.y + self.text_shadow_offset[1] + x_and_y),
                text_render_rect.size)
            basic_blit(new_image, shadow_text_render, shadow_text_rect)
   
   
    def set_relative_position(self, newpos):
        super().set_relative_position(newpos)
        left = newpos[0]
        for i, item in enumerate(self.item_img_list):
            item[0].set_relative_position((left, newpos[1]))
            left += item[0].relative_rect.w
            

            

    def rebuild(self):
        left = self.relative_rect.left
        self.relative_rect.size = (len(self.item_img_list)*(self.pic_size[0]+self.padding[0]), self.pic_size[1]+self.padding[1])
        for item in self.item_img_list:
            # item[0]['count'] = self.items_list
            
            # newpos = (left, item[0].relative_rect.top)
            item[0].relative_rect.size = (self.pic_size[0]+self.padding[0]*2, self.pic_size[1]+self.padding[1]*2)
            item[0].set_relative_position((left, self.relative_rect.top))
            left += self.pic_size[0]+self.padding[0]
        
        
            new_image = pygame.surface.Surface(item[0].relative_rect.size,
                                            flags=pygame.SRCALPHA,
                                            depth=32)
            new_image.fill(pygame.Color('#00000000'))
            pic_render_relative_rect = item[0].get_relative_rect()
            
            if item[1]!=-1:
                text_render = render_white_text_alpha_black_bg(self.font, str(item[1]))
                apply_colour_to_surface(self.text_colour, text_render)
                text_render_rect = text_render.get_rect()
                text_render_rect.topleft = (pic_render_relative_rect.w-text_render_rect.w-self.padding[0], pic_render_relative_rect.h-text_render_rect.h-self.padding[1])

            utils.basic_blit(new_image, pygame.transform.smoothscale(item[0].original_image, self.pic_size), (self.padding[0],self.padding[1]))

            if item[1]!=-1:
                if self.text_shadow:
                    self._rebuild_shadow(new_image, text_render_rect, str(item[1]))
                basic_blit(new_image, text_render,  text_render_rect.topleft)


            item[0].set_image(new_image)
            


class UIItem(UIItemsList):
    def __init__(self,
                 relative_rect: pygame.Rect,
                 image_surface: pygame.surface.Surface,
                 count: int,
                 manager: IUIManagerInterface,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 object_id: Union[ObjectID, str, None] = None,
                 anchors: Dict[str, str] = None,
                 visible: int = 1):


        items_list = [{'img':image_surface, 'count':count}]

        super().__init__(relative_rect=relative_rect,
                        items_list=items_list,
                        manager=manager,
                        container=container,
                        parent_element=parent_element,
                        object_id=object_id,
                        anchors=anchors,
                        visible=visible)

    def kill(self):
        return super().kill()


    def set_item(self, new_item_pic, new_item_count: int):
        item_list = [{'img':new_item_pic, 'count':new_item_count}]
        super().set_items_list(item_list)

class myUIImage(pygame_gui.elements.UIImage):
    
    def set_image(self, pic):
        super().set_image(pic) 
        self.relative_rect.size = self.image.get_rect().size
        
        
class UIButtonLine(pygame_gui.elements.UIButton):
    def __init__(self, relative_rect: pygame.Rect,
                 buttons: None,
                 manager: IUIManagerInterface,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None,
                 starting_height:int=1,
                 anchors: Dict[str, str] = None,
                 object_id: Union[ObjectID, str, None] = None,
                 generate_click_events_from_list: Iterable[int] = frozenset([pygame.BUTTON_LEFT]),
                 visible: int = 1
                 ):
    
        self.relative_rect = relative_rect
        self.manager = manager
        self.container = container

        self.ui_buttons, self.relative_rect.height = self._create_buttons(buttons)
        self.txt_buttons = buttons
        
        
        super().__init__(relative_rect,
                    text='',
                    manager=manager,
                    container=container,
                    starting_height = 1,
                    visible = 0
                    )
        
        
        
        self._create_valid_ids(container=container,
                               parent_element=parent_element,
                               object_id=object_id,
                               element_id='button_line')
        
        
        self.rebuild_from_changed_theme_data()
        
    def rebuild_from_changed_theme_data(self):
        for button in self.ui_buttons:
            button.rebuild_from_changed_theme_data()
                
     
    def _create_buttons(self, buttons):
        # # num_col:len_col:frac_col
        buttons_ui = []
        frac_col = len(buttons)
        if frac_col==0:
            return buttons_ui
        len_col = 1
        width = len_col*self.container.get_relative_rect().w//frac_col
        for i, button in enumerate(buttons):
            num_col = i
            left = num_col*self.container.get_relative_rect().w//frac_col
            button_rect = pygame.Rect(left, self.relative_rect.top, width, self.relative_rect.height)
            if button_rect.w==-2: button_rect.w = self.container.w
            butui = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=button['text'],
                manager=self.manager,
                container=self.container,
                object_id=button['id']
            )
            buttons_ui.append(butui)
        return buttons_ui, butui.get_relative_rect().height
        
    def set_buttons(self, new_buttons):

        if new_buttons!=self.txt_buttons:
            self.ui_buttons, self.relative_rect.height = self._create_buttons(new_buttons)
            self.txt_buttons = new_buttons
            
        
    def kill(self):
        for button in self.ui_buttons:
            button.kill()
            del button
        self.ui_buttons.clear()
        
        return super().kill()
    
    def set_relative_position(self, newpos):
        super().set_relative_position(newpos)
        for item in self.ui_buttons:
            item.set_relative_position(newpos)
            
        
    
    
class myUIProgressBar(pygame_gui.elements.UIProgressBar):
    def update(self, time_delta: float):
        super().update(time_delta)
        self.set_relative_position(self.rect)
