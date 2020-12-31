#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
xkcd Module for Inky-Calendar Project

by https://github.com/worstface
"""
from inkycal.modules.template import inkycal_module
from inkycal.custom import *
from dateutil.parser import *
from dateutil.tz import *
from datetime import *

try:
  import xkcd
except ImportError:
  print('xkcd is not installed! Please install with:')
  print('pip3 install xkcd')
  
try:
  import qrcode
except ImportError:
  print('qrcode is not installed! Please install with:')
  print('pip3 install qrcode[pil]')

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)

class Xkcd(inkycal_module):

  name = "xkcd - Displays xkcd comics"

  # required parameters
  requires = {

    "mode": {
        "label": "mode "               
        }          
    }

  def __init__(self, config):

    super().__init__(config)

    config = config['config']
   
    self.mode = config['mode']
    self.mode = 'latest'

    # give an OK message
    print(f'{filename} loaded')
    
  def generate_image(self):
    """Generate image for this module"""   

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

    # Set some parameters for formatting feeds
    line_spacing = 1
    line_height = self.font.getsize('hg')[1] + line_spacing
    line_width = im_width
    max_lines = (im_height // (self.font.getsize('hg')[1] + line_spacing))

    logger.debug(f"max_lines: {max_lines}")

    # Calculate padding from top so the lines look centralised
    spacing_top = int( im_height % line_height / 2 )

    # Calculate line_positions
    line_positions = [(0, spacing_top + _ * line_height ) for _ in range(max_lines)]

    logger.debug(f'line positions: {line_positions}')
      
    logger.info(f'getting xkcd comic...')
    xkcdComic = xkcd.getLatestComic() 
    xkcdComic.download(output='.', outputFile='xkcdComic.png')

    logger.info(f'got xkcd comic...')
   
    logger.info(f'preparing tweet image...')
    tweet_lines = []
    tweet_lines_colour = []    
         
    comicSpace = Image.new('RGBA', (im_width, im_height), (255,255,255,255))
    comicImage = Image.open('xkcdComic.png')
    comicSpace.paste(comicImage,(0,0))
    logger.info(f'added comic image')   
    
    im_black.paste(comicSpace)

    # Write/Draw something on the black image   
    for _ in range(len(tweet_lines)):
      if _+1 > max_lines:
        logger.error('Ran out of lines for tweet_lines_black')
        break
      write(im_black, line_positions[_], (line_width, line_height),
              tweet_lines[_], font = self.font, alignment= 'left')    

    # Write/Draw something on the colour image
    for _ in range(len(tweet_lines_colour)):
      if _+1 > max_lines:
        logger.error('Ran out of lines for tweet_lines_colour')
        break
      write(im_colour, line_positions[_], (line_width, line_height),
              tweet_lines_colour[_], font = self.font, alignment= 'left')    

    # Save image of black and colour channel in image-folder
    return im_black, im_colour

if __name__ == '__main__':
  print(f'running {filename} in standalone/debug mode')