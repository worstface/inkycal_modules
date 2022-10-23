#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Webshot module for Inkycal
by https://github.com/worstface
"""
from inkycal.modules.template import inkycal_module
from inkycal.custom import *
from dateutil.parser import *
from dateutil.tz import *
from datetime import *
import os

from inkycal.modules.inky_image import Inkyimage as Images

try:
  from htmlwebshot import WebShot
except ImportError:
  print('webshot is not installed! Please install with:')
  print('pip3 install webshot')

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)

class Webshot(inkycal_module):

  name = "Webshot - Displays screenshots of webpages"
  
  # required parameters
  requires = {

    "url": {
        "label":"Please enter the url",
        },
    "palette": {
        "label":"Which color palette should be used for the webshots?",
        "options": ["bw", "bwr", "bwy"]
        }
    }
    
  optional = {
  
    "crop_x": {
        "label":"Please enter the crop x-position",
        },
    "crop_y": {
        "label":"Please enter the crop y-position",
        },    
    "crop_w": {
        "label":"Please enter the crop width",
        },
    "crop_h": {
        "label":"Please enter the crop height",
        }
    }

  def __init__(self, config):

    super().__init__(config)

    config = config['config']
    
    self.url = config['url']
    self.palette = config['palette']
          
    if config["crop_h"] and isinstance(config["crop_h"], str):
      self.crop_h = int(config["crop_h"])
    else:
      self.crop_h = 2000
      
    if config["crop_w"] and isinstance(config["crop_w"], str):
      self.crop_w = int(config["crop_w"])
    else:
      self.crop_w = 2000
      
    if config["crop_x"] and isinstance(config["crop_x"], str):
      self.crop_x = int(config["crop_x"])
    else:
      self.crop_x = 0
      
    if config["crop_y"] and isinstance(config["crop_y"], str):
      self.crop_y = int(config["crop_y"])
    else:
      self.crop_y = 0
   
    # give an OK message
    print(f'{filename} loaded')
    
  def generate_image(self):
    """Generate image for this module"""

    # Create tmp path
    tmpFolder = '/tmp/inkycal_webshot/'

    try:
        os.mkdir(tmpFolder)
    except OSError:
        print ("Creation of tmp directory %s failed" % path)
    else:
        print ("Successfully created tmp directory %s " % path)

    # Define new image size with respect to padding
    im_width = int(self.width - (2 * self.padding_left))
    im_height = int(self.height - (2 * self.padding_top))
    im_size = im_width, im_height
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Create an image for black pixels and one for coloured pixels (required)
    im_black = Image.new('RGB', size = im_size, color = 'white')
    im_colour = Image.new('RGB', size = im_size, color = 'white')

    # Check if internet is available
    if internet_available() == True:
      logger.info('Connection test passed')
    else:
      raise Exception('Network could not be reached :/')
      
    logger.info(f'preparing webshot from {self.url}... cropH{self.crop_h} cropW{self.crop_w} cropX{self.crop_x} cropY{self.crop_y}')
        
    shot = WebShot()
    
    shot.params = {
    "--crop-x": self.crop_x,
    "--crop-y": self.crop_y,
    "--crop-w": self.crop_w,
    "--crop-h": self.crop_h,
    }
    
    logger.info(f'getting webshot from {self.url}...')
    
    shot.create_pic(url=self.url, output="/tmp/inkycal_webshot/webshot.png")

    logger.info(f'got webshot...')
              
    webshotSpaceBlack = Image.new('RGBA', (im_width, im_height), (255,255,255,255))  
    webshotSpaceColour = Image.new('RGBA', (im_width, im_height), (255,255,255,255)) 
      
    im = Images()
    im.load('/tmp/inkycal_webshot/webshot.png')
    im.remove_alpha()
    
    imageAspectRatio = im_width / im_height
    webshotAspectRatio = im.image.width / im.image.height
        
    if webshotAspectRatio > imageAspectRatio:
        imageScale = im_width / im.image.width
    else:
        imageScale = im_height / im.image.height        
        
    webshotHeight = int(im.image.height * imageScale)      
            
    im.resize( width=int(im.image.width * imageScale), height= webshotHeight)        
    
    im_webshot_black, im_webshot_colour = im.to_palette(self.palette)  

    webshotCenterPosY = int((im_height/2)-((im.image.height)/2))
    
    centerPosX = int((im_width/2)-(im.image.width/2))
    
    webshotSpaceBlack.paste(im_webshot_black, (centerPosX, webshotCenterPosY))
    im_black.paste(webshotSpaceBlack)
    
    webshotSpaceColour.paste(im_webshot_colour, (centerPosX, webshotCenterPosY))
    im_colour.paste(webshotSpaceColour)
    
    im.clear()
    logger.info(f'added webshot image')    
   
    # Save image of black and colour channel in image-folder
    return im_black, im_colour  

if __name__ == '__main__':
  print(f'running {filename} in standalone/debug mode')
