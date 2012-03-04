import os
import pyglet

from slidesaver import util

PICTURE_DIR = os.path.expanduser("~/Pictures")

class AppWindow(pyglet.window.Window):

    def __init__(self):

        super(AppWindow, self).__init__(fullscreen=True)
        self.pics = util.Pictures(PICTURE_DIR)
        self.screen_x = self.width
        self.screen_y = self.height
        self.screen_ratio = float(self.screen_x) / self.screen_y
        self.center_x = self.screen_x // 2
        self.center_y = self.screen_y // 2

        self.load_new_image()

    def load_new_image(self, dt=None):
        import time
        t1 = time.time()

        random_pic = self.pics.get_random()

        #TODO: More efficient way to load and resize large images? PIL?
        self.image = pyglet.image.load(random_pic)

        # Set anchor of sprite to center of image
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        self.picture = pyglet.sprite.Sprite(self.image)

        # Resize image to fit on screen
        image_x, image_y = self.picture.width, self.picture.height
        image_ratio = float(image_x) / image_y

        if image_ratio >= self.screen_ratio:
            scale = float(self.screen_x) / image_x
        else:
            scale = float(self.screen_y) / image_y

        self.picture.scale = scale

        # Move sprite to center
        self.picture.set_position(self.center_x, self.center_y)
        t2 = time.time()
        print t2 - t1


if __name__ == "__main__":

    app = AppWindow()
    pyglet.clock.schedule_interval(app.load_new_image, 10)

    @app.event
    def on_draw():
        app.clear()
        app.picture.draw()

    pyglet.app.run()
