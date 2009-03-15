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
import os

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

    def applicationSupportFolder(self):
        paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,NSUserDomainMask,True)
        basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
        fullPath = basePath.stringByAppendingPathComponent_("Uncloud")
        if not os.path.exists(fullPath):
            os.mkdir(fullPath)
        return fullPath
    
    def pathForFilename(self,filename):
        return self.applicationSupportFolder().stringByAppendingPathComponent_(filename)
