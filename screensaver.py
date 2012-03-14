#!/usr/bin/env python

import os
import subprocess

import pyglet
from pyglet.window import key

import Image

from slidesaver import util

PHOTO_APP = 'shotwell'
PICTURE_DIR = os.path.expanduser("~/Pictures")
CROP = True
PICTURE_DELAY = 10

class AppWindow(pyglet.window.Window):

    def __init__(self):

        super(AppWindow, self).__init__(fullscreen=True)

        #Hide mouse cursor
        self.set_mouse_visible(False)

        self.paused = False
        self.pics = util.Pictures(PICTURE_DIR)
        self.screen_x = self.width
        self.screen_y = self.height
        self.screen_ratio = float(self.screen_x) / self.screen_y
        self.center_x = self.screen_x // 2
        self.center_y = self.screen_y // 2
        self.transitioning = False
        self.old_picture = None
        self.picture = None
        self.picture_path = ""
        self.time = 0

        self.load_new_image()

    def increase_opacity(self, dt):
        if self.picture.opacity <= 255 and self.transitioning:
            if self.picture.opacity + 2 > 255:
                self.picture.opacity = 255
                if self.old_picture:
                    self.old_picture.opacity = 0
            else:
                self.picture.opacity += 2
                if self.old_picture:
                    self.old_picture.opacity -= 2
        else:
            self.transitioning = False

    def zoom(self, dt):
        self.picture.scale += .05 * dt
        if self.old_picture:
            self.old_picture.scale += .05 * dt

    def reactivate(self, dt):
        self.activate()

    def load_new_image(self):

        # Window loses focus when automatically maximized.
        # This helps give it focused (though it's not guaranteed to work. It
        # doesn't seem to work at all if called right after/before maximizing.
#        self.activate()

        random_pic = self.pics.get_random()
        temp_image = Image.open(random_pic)

        # Resize image to fit on screen
        image_x, image_y = temp_image.size
        image_ratio = float(image_x) / image_y

        # Crop horizontally-oriented images to fill the screen
        if CROP and image_ratio > 1:
            if image_ratio >= self.screen_ratio:
                resized_y = self.screen_y
                resized_x = (resized_y * image_x) // image_y
            else:
                resized_x = self.screen_x
                resized_y = (resized_x * image_y) // image_x
        else:
            if image_ratio >= self.screen_ratio:
                resized_x = self.screen_x
                resized_y = (resized_x * image_y) // image_x
            else:
                resized_y = self.screen_y
                resized_x = (resized_y * image_x) // image_y

        temp_image = temp_image.resize((resized_x, resized_y))
        raw_image = temp_image.tostring()

        self.image = pyglet.image.ImageData(resized_x,
                                            resized_y,
                                            'RGB',
                                            raw_image,
                                            pitch= -resized_x * 3)

        # Set anchor of sprite to center of image
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        if self.picture:
            self.old_picture = self.picture

        self.picture = pyglet.sprite.Sprite(self.image)
        self.picture_path = random_pic

        # Move sprite to center
        self.picture.set_position(self.center_x, self.center_y)
        self.picture.opacity = 0
        self.transitioning = True

    # Keep track of elapsed time so we can resume where we left off
    def tick_picture_clock(self, dt):
        if self.time <= PICTURE_DELAY:
            self.time += dt
        else:
            self.load_new_image()
            self.time = 0

def start(window):
    pyglet.clock.schedule_interval(window.increase_opacity, 1.0 / 120)
    pyglet.clock.schedule_interval(window.tick_picture_clock, 1.0 / 15)
    window.paused = False


def pause(window):
    pyglet.clock.unschedule(window.tick_picture_clock)
    pyglet.clock.unschedule(window.increase_opacity)
    window.paused = True
    window.set_fullscreen(False)
    window.minimize()
    subprocess.Popen([PHOTO_APP, app.picture_path])


def quit(window):
    window.close()
    pyglet.app.exit()


if __name__ == "__main__":

    app = AppWindow()
    start(app)
#    pyglet.clock.schedule_interval(app.zoom, 1.0 / 30)

    @app.event
    def on_draw():
        app.clear()
        app.picture.draw()
        if app.old_picture:
            app.old_picture.draw()

    @app.event
    def on_activate():
        if app.paused:
            app.set_fullscreen(True)
            start(app)
            pyglet.clock.schedule_once(app.reactivate, 1)
        else:
            pass

    @app.event
    def on_key_press(symbol, modifiers):
        if symbol == key.SPACE:
            if app.paused:
                app.set_fullscreen(True)
                start(app)
                print "space and paused"
            else:
                pause(app)
                print "space and not paused"
        else:
            quit(app)

    @app.event
    def on_mouse_press(x, y, button, modifiers):
        quit(app)

    @app.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        quit(app)

    @app.event
    def on_mouse_motion(x, y, dx, dy):
        quit(app)

    pyglet.app.run()
