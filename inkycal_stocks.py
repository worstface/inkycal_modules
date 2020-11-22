#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Stocks Module for Inky-Calendar Project

Version 0.2: Migration to Inkycal 2.0.0
Version 0.1: Migration to Inkycal 2.0.0b

by https://github.com/worstface
"""
from inkycal.modules.template import inkycal_module
from inkycal.custom import *

try:
  import yfinance as yf
except ImportError:
  print('yfinance is not installed! Please install with:')
  print('pip3 install yfinance')

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)
logger.setLevel(level=logging.ERROR)

class Stocks(inkycal_module):

  name = "Stocks - Displays stock market infos"

  def __init__(self, config):
  
    super().__init__(config)

    config = config['config']

    # give an OK message (optional)
    print('{0} loaded'.format(filename))

#############################################################################
#                 Validation of module specific parameters                  #
#############################################################################

  def _validate(self):
    """Validate module-specific parameters"""

    # Here, we are checking if do_something (from init) is True/False
    if not isinstance(self.do_something, bool):
      print('do_something has to be a boolean: True/False')


#############################################################################
#                       Generating the image                                #
#############################################################################

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

    #################################################################
    
    parsed_tickers = []
    parsed_tickers_colour = []
    
    for ticker in self.config['tickers']:         
          logger.info('preparing data for {0}...'.format(ticker))

          yfTicker = yf.Ticker(ticker)

          try:
            stockInfo = yfTicker.info
            stockName = stockInfo['shortName']
          except Exception:
            stockName = ticker
            logger.warning('Failed to get ticker info! Using the ticker symbol as name instead.')

          stockHistory = yfTicker.history("2d")
          previousQuote = (stockHistory.tail(2)['Close'].iloc[0])
          currentQuote = (stockHistory.tail(1)['Close'].iloc[0])   
          currentGain = currentQuote-previousQuote       
          currentGainPercentage = (1-currentQuote/previousQuote)*-100

          tickerLine = '{}: {:.2f} {:+.2f} ({:+.2f}%)'.format(stockName, currentQuote, currentGain, currentGainPercentage)
          logger.info(tickerLine)
          parsed_tickers.append(tickerLine)
          
          if currentGain < 0:
            parsed_tickers_colour.append(tickerLine)
          else:
            parsed_tickers_colour.append("")
    
    # Write/Draw something on the black image    
    for _ in range(len(parsed_tickers)):
      write(im_black, line_positions[_], (line_width, line_height),
              parsed_tickers[_], font = self.font, alignment= 'left')
              
    del parsed_tickers
              
    # Write/Draw something on the colour image    
    for _ in range(len(parsed_tickers_colour)):
      write(im_colour, line_positions[_], (line_width, line_height),
              parsed_tickers_colour[_], font = self.font, alignment= 'left')

    del parsed_tickers_colour
    
    #################################################################

    # Save image of black and colour channel in image-folder
    return im_black, im_colour