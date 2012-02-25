# Alternative to xautolock

import subprocess
from gi.repository import GObject
import checklock
import checkidle


class System():

    def __init__(self):

        self.SCREENSAVER_DELAY = 60000   # milliseconds
        self.CLOCK_TIMEOUT = 5000        # time between checks in milliseconds
        self.idle = False
        self.screensaver_on = False
        self.screensaver = None
        self.locked = False

    def check_idle(self, delay):
        self.idle = checkidle.is_idle(delay)
        return self.idle

    def check_locked(self):
        self.locked = checklock.is_locked()
        return self.locked

    def _check_screensaver(self):

        try:
            retcode = self.screensaver.poll()
            if retcode is not None:
                self.screensaver_on = False
            else:
                self.screensaver_on = True
        except AttributeError:
            print "Screensaver not started yet"
            self.screensaver_on = False

    def start_screensaver(self):
        print "Starting screensaver"
        process = subprocess.Popen(["screensaver.py"])

        return process

    def manage_screensaver(self):

        # Use decorators to call these when attributes are read?
        self.check_idle(self.SCREENSAVER_DELAY)
        self.check_locked()

        # TODO: Have screensaver emit dbus signal when it dies, or use
        #       idle time to determine this?
        #
        # Know if screensaver killed itself
        self._check_screensaver()

        print "Screensaver callback"
        if self.screensaver_on and not self.locked:
            return True

        elif self.screensaver_on and self.locked:
            print "Killing screensaver"
            self.screensaver.terminate()
            self.screensaver_on = False

        elif self.idle and not self.locked:
            self.screensaver = self.start_screensaver()
            self.screensaver_on = True

        return True


if __name__ == "__main__":

    system = System()
    loop = GObject.MainLoop()
    GObject.timeout_add(system.CLOCK_TIMEOUT, system.manage_screensaver)
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
