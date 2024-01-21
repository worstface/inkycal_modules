"""
Inkycal Comics module
by https://github.com/worstface
"""

import comics
import xkcd

from inkycal.custom import *
from inkycal.modules.inky_image import Inkyimage as Images
from inkycal.modules.template import inkycal_module
from datetime import datetime

logger = logging.getLogger(__name__)


class Comics(inkycal_module):
    name = "Comics - Displays comics from gocomic.com and xkcd.com"

    # required parameters
    requires = {

        "comic": {
            "label": "Enter the comic name"
        },
        "mode": {
            "label": "Select the mode",
            "options": ["latest", "random"],
            "default": "latest"
        },
        "palette": {
            "label": "Picture color palette",
            "options": ["bw", "bwr", "bwy"]
        },
        "orientation": {
            "label": "Please select the desired orientation",
            "options": ["vertical", "horizontal"]
        }
    }

    def __init__(self, config):

        super().__init__(config)

        config = config['config']

        self.comic = config['comic']
        self.mode = config['mode']
        self.palette = config['palette']
        self.orientation = config['orientation']

        # give an OK message
        print(f'Inkycal Comics loaded')

    def generate_image(self):
        """Generate image for this module"""

        # Create tmp path
        tmpPath = f"{top_level}/temp"

        if not os.path.exists(tmpPath):
            os.mkdir(tmpPath)

        # Define new image size with respect to padding
        im_width = int(self.width - (2 * self.padding_left))
        im_height = int(self.height - (2 * self.padding_top))
        im_size = im_width, im_height
        logger.info('image size: {} x {} px'.format(im_width, im_height))

        # Create an image for black pixels and one for coloured pixels (required)
        im_black = Image.new('RGB', size=im_size, color='white')
        im_colour = Image.new('RGB', size=im_size, color='white')

        # Check if internet is available
        if internet_available():
            logger.info('Connection test passed')
        else:
            raise Exception('Network could not be reached :/')

        logger.info(f'getting {self.comic} picture...')

        if self.comic == 'xkcd':
            if self.mode == 'random':
                xkcdComic = xkcd.getRandomComic()
                xkcdComic.download(output=tmpPath, outputFile=f"{self.comic}.png")
            else:
                xkcdComic = xkcd.getLatestComic()
                xkcdComic.download(output=tmpPath, outputFile=f"{self.comic}.png")
        else:
            if self.mode == 'random':
                comics.search(self.comic).random_date().download(f"{tmpPath}/{self.comic}.png")
            else:
                comics.search(self.comic).date(datetime.today()).download(f"{tmpPath}/{self.comic}.png")

        logger.info(f'got {self.comic} picture...')

        comicSpaceBlack = Image.new('RGBA', (im_width, im_height), (255, 255, 255, 255))
        comicSpaceColour = Image.new('RGBA', (im_width, im_height), (255, 255, 255, 255))

        im = Images()
        im.load(f"{tmpPath}/{self.comic}.png")
        im.remove_alpha()
        
        im.autoflip(self.orientation)

        imageAspectRatio = im_width / im_height
        comicAspectRatio = im.image.width / im.image.height

        if comicAspectRatio > imageAspectRatio:
            imageScale = im_width / im.image.width
        else:
            imageScale = im_height / im.image.height

        comicHeight = int(im.image.height * imageScale)

        im.resize(width=int(im.image.width * imageScale), height=comicHeight)

        im_comic_black, im_comic_colour = im.to_palette(self.palette)

        comicCenterPosY = int((im_height / 2) - ((im.image.height) / 2))
        centerPosX = int((im_width / 2) - (im.image.width / 2))

        comicSpaceBlack.paste(im_comic_black, (centerPosX, comicCenterPosY))
        im_black.paste(comicSpaceBlack)

        comicSpaceColour.paste(im_comic_colour, (centerPosX, comicCenterPosY))
        im_colour.paste(comicSpaceColour)

        im.clear()
        logger.info(f'added comic image')

        # Save image of black and colour channel in image-folder
        return im_black, im_colour
