#!/usr/bin/env python

# Small script to allow switching of desktops

# Usage
# -----
# 1. MAKE SURE YOUR /home/$USER/Desktop DIRECTORY IS EMPTY
# 2. Double check number 1
# 3. Delete your desktop directory
# 4. Create a configuration directory like /home/$USER/.desktops and point 
#    AVAILABLE_DESKTOPS to this directory
# 5. cd to AVAILABLE_DESKTOPS and create symlinks to your desired desktops
# 6. Set DESKTOP_DIR to point to your deskop (/home/$USER/Desktop)
#
# Add This script as startup script and enjoy
import sys
import os
import gtk
import appindicator
import pynotify

pynotify.init("Desktop Notification")

DESKTOP_DIR = '/home/your_user/Desktop'
AVAILABLE_DESKTOPS = '/home/your_user/.desktops/'

class DesktopSwitcher:
    def __init__(self):
        # other icons can be found in /usr/share/icons/ubuntu-mono-light/status/16
        # This one looked cool, but is not really appropriate, set to "" in order
        # to remove it
        self.ind = appindicator.Indicator("desktop-change-menu",
                                          "weather-fog",
                                          appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)        
        self.menu = gtk.Menu()
        self.add_desktops()
        self.ind.set_menu(self.menu)                
        
        # now find current desktop link and name it
        if os.path.exists(DESKTOP_DIR):
            current = [d for d in self.desktops if d.get('path') == os.readlink(DESKTOP_DIR)][0]
            self.ind.set_label(current.get('name'))
        else:
            self.ind.set_label('Select Desktop...')
        
    def add_desktops(self):
        sym_links = os.listdir(AVAILABLE_DESKTOPS)
        self.desktops = map(lambda n: { 
          'name': n, 
          'path': os.readlink(AVAILABLE_DESKTOPS + n) 
        }, sym_links)
        for desktop in self.desktops:
          self.add_desktop(desktop.get('name'), desktop.get('path'))

    def add_desktop(self, name, path):
        item = gtk.MenuItem(name)
        item.connect("activate", self.change_desktop, name, path)
        item.show()
        self.menu.append(item)
    
    def change_desktop(self, widget, name, path):
        # there must be something wrong - this will throw on OSError if no link is provided
        if os.path.exists(DESKTOP_DIR) and not os.readlink(DESKTOP_DIR):
          return
          
        # remove old link
        if os.path.exists(DESKTOP_DIR):
          os.remove(DESKTOP_DIR)
          
        # create new link (could not find a -force flag for os.symlink)
        os.symlink(path, DESKTOP_DIR)
        pynotify.Notification(name, "Changed Desktop to " + path + ".\n Please refresh by pressing F5").show()
        self.ind.set_label(name)
    
    def quit(self, widget):
         sys.exit(0)

if __name__ == "__main__":
     indicator = DesktopSwitcher()
     gtk.main()
