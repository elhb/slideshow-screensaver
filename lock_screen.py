#TODO: Expand to work with xscreensaver, KDE, ...

import dbus

def activated():
    session_bus = dbus.SessionBus()
    dbus_object  = session_bus.get_object("org.gnome.ScreenSaver","/")
    status = dbus_object.GetActive(dbus_interface="org.gnome.ScreenSaver")
    
    if status == 0:
        return False
    else:
        return True
