#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Tweets Module for Inky-Calendar Project

by https://github.com/worstface
"""
from inkycal.modules.template import inkycal_module
from inkycal.custom import *

try:
  import twint
except ImportError:
  print('twint is not installed! Please install with:')
  print('pip3 install twint')
  
try:
  import qrcode
except ImportError:
  print('qrcode is not installed! Please install with:')
  print('pip3 install qrcode[pil]')

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)

class Tweets(inkycal_module):

  name = "Tweets - Displays Twitter tweets"

  # required parameters
  optional = {

    "username": {

      "label": "You can display any information by using "               
              }
    }

  def __init__(self, config):

    super().__init__(config)

    config = config['config']
   
    self.username = config['username']

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
    line_positions = [
      (0, spacing_top + _ * line_height ) for _ in range(max_lines)]

    logger.debug(f'line positions: {line_positions}')
      
    logger.info(f'preparing twint configuration...')

    twintConfig = twint.Config()
    
    twintConfig.Username = self.username
    twintConfig.Limit = 20
    twintConfig.Store_object = True
    twintConfig.Hide_output = True

    twint.run.Search(twintConfig)
    tweets = twint.output.tweets_list
    
    lastTweet = tweets[0]
    
    logger.info(lastTweet.username)
    logger.info(lastTweet.name)
    logger.info(lastTweet.tweet)
    logger.info(lastTweet.timestamp)
    logger.info(lastTweet.link)

    # Write/Draw something on the black image    

    # Write/Draw something on the colour image    

    # Save image of black and colour channel in image-folder
    return im_black, im_colour

if __name__ == '__main__':
  print(f'running {filename} in standalone/debug mode')
