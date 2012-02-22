import sys
import pygame
from pygame.locals import *
import util

BLACK = (0, 0, 0)
FPS = 30
PICTURE_DIR = "/home/james/Pictures/wallpapers"
UPDATE_PICTURE_EVENT = USEREVENT + 1
PICTURE_DELAY = 10000   # Time between pictures in milliseconds


# TODO: Can this be improved to make it more easily imported by other 
#       applications?
#
# Class to encapsulate the entire application
class Screensaver():
    """..."""

    def __init__(self):
        """..."""
        # TODO: Is this the best place to call this
        pygame.init()
        
        self._set_screen_size()
        self._initialize_screen()
        self._initialize_clock()
        
        self.pics = util.Pictures()
        
        self.run()
        
    def _set_screen_size(self):
        """..."""
    
        # get size of fullscreen display into screen_x, screen_y
        modes = pygame.display.list_modes()    # defaults to fullscreen
        modes.sort()                           # largest goes last
        self.screen_x, self.screen_y = modes[-1]
        self.screen_ratio = float(self.screen_x) / self.screen_y
        
    def _initialize_screen(self):
        """..."""
        
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y),
                                              pygame.FULLSCREEN )
        pygame.display.set_caption('Slideshow Screensaver')
        
    def _initialize_clock(self):
        self.fps_clock = pygame.time.Clock()
        
    def show_picture(self):
        
        #Cover up image in the background
        self.screen.fill(BLACK)
    
        random_pic = self.pics.get_random()
        image = pygame.image.load(random_pic).convert()
        
        # Resize image to fit on screen
        image_x, image_y = image.get_size()
        image_ratio = float(image_x) / image_y
        if image_ratio >= self.screen_ratio:
            resized_x = self.screen_x
            resized_y = (resized_x * image_y) / image_x
        else:
            resized_y = self.screen_y
            resized_x = (resized_y * image_x) / image_y
        image = pygame.transform.scale(image, (resized_x, resized_y))
        
        # Center image
        image_rect = image.get_rect()
        image_rect.center = self.screen.get_rect().center
        
        self.screen.blit(image, image_rect)
   
        pygame.display.update()
        
    def run(self):
        
        # Load first picture and start timer
        self.show_picture()
        pygame.time.set_timer(UPDATE_PICTURE_EVENT, PICTURE_DELAY)
        
        # Hide mouse cursor
        pygame.mouse.set_visible(False)
        
        # Clear initial mouse event
        pygame.event.clear()
        
        while True:
            event = pygame.event.poll()
            
            if event.type == UPDATE_PICTURE_EVENT:
                self.show_picture()
                
            elif event.type != pygame.NOEVENT:
                self.quit()
                
            self.fps_clock.tick(FPS)
                
    def quit(self):
        
        # Close screensaver quickly
        pygame.display.quit()
        
        pygame.quit()
        sys.exit()
            
              
if __name__ == "__main__":
    app = Screensaver()