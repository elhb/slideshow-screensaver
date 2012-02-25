#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Slideshow Screensaver',
      version='0.1',
      summary='Slideshow screensaver for Gnome based on Pygame',
      keywords=['slideshow', 'screensaver', 'gnome'],
      author=u'James Adney',
      author_email='jfadney@gmail.com',
      home_page='https://github.com/jamesadney/slideshow-screensaver',
      license='GPL3',
      packages=find_packages(),
      scripts=["watch-idle.py", "screensaver.py"],
      install_requires=["distribute",
                        "pygame",
                        "dbus-python",
                        "pygir-ctypes"])
