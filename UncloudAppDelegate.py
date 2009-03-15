#
#  UncloudAppDelegate.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

import objc
from Foundation import *
from AppKit import *

class UncloudAppDelegate(NSObject):
    mainController = objc.IBOutlet()
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

    def applicationDidBecomeActive_(self, sender):
        NSLog("Application did become active.")
        self.mainController.displayLoginSheet()
