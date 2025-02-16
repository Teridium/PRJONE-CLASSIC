from cv2 import CV_8U
import pygame
from typing import Union, Tuple, Dict

import pygame
import numpy as np

def convert_to_grayscale(image):
    """Преобразует изображение в черно-белое с сохранением прозрачности."""
    image_bw = image.copy()
    arr = pygame.surfarray.array3d(image_bw)  # Преобразуем изображение в массив
    alpha = pygame.surfarray.array_alpha(image_bw)  # Получаем альфа-канал
    
    # Усредняем значения каналов (R, G, B) для получения оттенков серого
    gray = np.dot(arr[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    
    # Создаем черно-белый массив с тремя одинаковыми каналами (R=G=B)
    gray_arr = np.stack([gray, gray, gray], axis=-1)
    
    # Создаем поверхность с поддержкой прозрачности
    image_bw = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    
    # Заполняем поверхность прозрачным цветом
    image_bw.fill((0, 0, 0, 0))
    
    # Записываем черно-белое изображение в surface
    pygame.surfarray.blit_array(image_bw, gray_arr)
    
    # Добавляем обратно альфа-канал
    pygame.surfarray.pixels_alpha(image_bw)[:] = alpha
    
    return image_bw

def basic_blit(destination: pygame.surface.Surface,
               source: pygame.surface.Surface,
               pos: Union[Tuple[int, int], pygame.Rect],
               area: Union[pygame.Rect, None] = None):
    """
    The basic blitting function to use. WE need to wrap this so we can support pre-multiplied alpha
    on post 2.0.0.dev10 versions of pygame and regular blitting on earlier versions.

    :param destination: Destination surface to blit on to.
    :param source: Source surface to blit from.
    :param pos: The position of our blit.
    :param area: The area of the source to blit from.

    """
    destination.blit(source, pos, area, special_flags=pygame.BLEND_ALPHA_SDL2)
    
# def convert_opencv_img_to_pygame(opencv_image):
#     """
# Convert OpenCV images for Pygame.

#     see https://gist.github.com/radames/1e7c794842755683162b
#     see https://github.com/atinfinity/lab/wiki/%5BOpenCV-Python%5D%E7%94%BB%E5%83%8F%E3%81%AE%E5%B9%85%E3%80%81%E9%AB%98%E3%81%95%E3%80%81%E3%83%81%E3%83%A3%E3%83%B3%E3%83%8D%E3%83%AB%E6%95%B0%E3%80%81depth%E5%8F%96%E5%BE%97
#     """
#     if len(opencv_image.shape) == 2:
#         #For grayscale images
#         cvt_code = cv2.COLOR_GRAY2RGB
#     else:
#         #In other cases:
#         cvt_code = cv2.COLOR_BGR2RGB
#     rgb_image = cv2.cvtColor(opencv_image, cvt_code).swapaxes(0, 1)
#     #Generate a Surface for drawing images with Pygame based on OpenCV images
#     pygame_image = pygame.surfarray.make_surface(rgb_image)

#     return pygame_image
    
# def cvimage_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def set_proportion_by_frame(sprite_size, frame_size):
    sprite_width, sprite_height = sprite_size
    frame_width, frame_height = frame_size
    
    ratio_w = frame_width / sprite_width
    ratio_h = frame_height / sprite_height
    ratio = min(ratio_w, ratio_h)
    
    proportional_width = sprite_width * ratio
    proportional_height = sprite_height * ratio
    
    return (proportional_width, proportional_height)    