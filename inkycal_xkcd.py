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
import os

try:
  import xkcd
except ImportError:
  print('xkcd is not installed! Please install with:')
  print('pip3 install xkcd')

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)

class Xkcd(inkycal_module):

  name = "xkcd - Displays comics from xkcd.com by Randall Munroe"

  # required parameters
  requires = {

    "mode": {
        "label":"Please select the mode",
        "options": ["latest", "random"],
        "default": "latest"      
        },
    "alt": {
        "label": "Would you like to add the alt text below the comic?",
        "options": ["yes", "no"],
        "default": "yes"
        }
    }

  def __init__(self, config):

    super().__init__(config)

    config = config['config']
   
    self.mode = config['mode']
    self.alt = config['alt']

    # give an OK message
    print(f'{filename} loaded')
    
  def generate_image(self):
    """Generate image for this module"""   

    # Create tmp path
    tmpPath = '/tmp/inkycal_xkcd/'

    try:
        os.mkdir(tmpPath)
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
            
    if self.mode == 'random':
        xkcdComic = xkcd.getRandomComic()
    else:
        xkcdComic = xkcd.getLatestComic()
    
    xkcdComic.download(output=tmpPath, outputFile='xkcdComic.png')

    logger.info(f'got xkcd comic...')
    title_lines = []
    title_lines.append(xkcdComic.getTitle())
    
    if self.alt == "yes":
        alt_text = xkcdComic.getAltText() # get the alt text, too (I break it up into multiple lines later on)
   
        # break up the alt text into lines
        alt_lines = []
        current_line = ""
        for _ in alt_text.split(" "):
            # this breaks up the alt_text into words and creates each line by adding
            # one word at a time until the line is longer than the width of the module
            # then it appends the line to the alt_lines array and starts testing a new line
            if self.font.getsize(current_line + _ + " ")[0] < im_width:
                current_line = current_line + _ + " "
            else:
                alt_lines.append(current_line)
                current_line = _ + " "
        alt_lines.append(current_line) # this adds the last line to the array (or the only line, if the alt text is really short)
        altHeight = int(line_height*len(alt_lines))
    else:
        altHeight = 0 # this is added so that I don't need to add more "if alt is yes" conditionals when centering below. Now the centering code will work regardless of whether they want alttext or not
        
    comicSpace = Image.new('RGBA', (im_width, im_height), (255,255,255,255))
    comicImage = Image.open(tmpPath+'/xkcdComic.png')    
    headerHeight = int(line_height*3/2)

    comicImage.thumbnail((im_width,im_height-headerHeight), Image.BICUBIC)
    centerPosX = int((im_width/2)-(comicImage.width/2))

    headerCenterPosY = int((im_height/2)-((comicImage.height+headerHeight+altHeight)/2))
    comicCenterPosY = int((im_height/2)-((comicImage.height+headerHeight+altHeight)/2)+headerHeight)
    altCenterPosY = int((im_height/2)-((comicImage.height+headerHeight+altHeight)/2)+headerHeight+comicImage.height)

    comicSpace.paste(comicImage, (centerPosX, comicCenterPosY))
    logger.info(f'added comic image')
    
    im_black.paste(comicSpace)
    # Write the title on the black image 
    write(im_black, (0, headerCenterPosY), (line_width, line_height),
              title_lines[0], font = self.font, alignment= 'center')
    
    if self.alt == "yes":
        # write alt_text
        for _ in range(len(alt_lines)):
          write(im_black, (0, altCenterPosY+_*line_height), (line_width, line_height),
                    alt_lines[_], font = self.font, alignment='center')

    # Save image of black and colour channel in image-folder
    return im_black, im_colour

if __name__ == '__main__':
  print(f'running {filename} in standalone/debug mode')
