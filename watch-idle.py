# Alternative to xautolock, though it's not necessarily better.

import ctypes
import os
import subprocess
from gi.repository import GObject

SCREENSAVER_DELAY = 4000   # milliseconds
CLOCK_TIMEOUT = 5000        # time between checks in milliseconds

class XScreenSaverInfo( ctypes.Structure):
  """ typedef struct { ... } XScreenSaverInfo; """
  _fields_ = [('window', ctypes.c_ulong), # screen saver window
              ('state', ctypes.c_int), # off,on,disabled
              ('kind', ctypes.c_int), # blanked,internal,external
              ('since', ctypes.c_ulong), # milliseconds
              ('idle', ctypes.c_ulong), # milliseconds
              ('event_mask', ctypes.c_ulong)] # events
            
              
def get_idle_time():

    xlib = ctypes.cdll.LoadLibrary('libX11.so')
    display = xlib.XOpenDisplay(os.environ['DISPLAY'])
    xss = ctypes.cdll.LoadLibrary('libXss.so.1')
    xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
    xssinfo = xss.XScreenSaverAllocInfo()
    xss.XScreenSaverQueryInfo(display, xlib.XDefaultRootWindow(display), xssinfo)

    idle_time = xssinfo.contents.idle
    return idle_time
    

def check_idle():
    
    idle_time = get_idle_time()
    print idle_time
    if idle_time >= SCREENSAVER_DELAY:
        subprocess.call(["python2", "/home/james/aptana_workspace/slideshow-screensaver/screensaver.py"])
        
    return True
    
    
if __name__ == "__main__":

    loop = GObject.MainLoop()
    GObject.timeout_add(CLOCK_TIMEOUT, check_idle)
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
    
