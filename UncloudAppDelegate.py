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
    opQ = objc.ivar(u"opQ")
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        self.opQ = NSOperationQueue.alloc().init()
        self.mainController.displayLoginSheet()

    def applicationDidBecomeActive_(self, sender):
        NSLog("Application did become active.")

    def applicationWillTerminate_(self, sender):
        self.opQ.release()
