#
#  UncloudAppDelegate.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright Harish Mallipeddi 2009. All rights reserved.
#

import objc
from Foundation import *
from AppKit import *
import os, string

class UncloudAppDelegate(NSObject):
    mainController = objc.IBOutlet()
    opQ = objc.ivar(u"opQ")
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
        self.opQ = NSOperationQueue.alloc().init()
        self.mainController.displayLoginSheet()

    def applicationSupportFolder(self):
        paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,NSUserDomainMask,True)
        basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
        fullPath = basePath.stringByAppendingPathComponent_("Uncloud")
        if not os.path.exists(fullPath):
            os.mkdir(fullPath)
        return fullPath
    
    def pathForFilename(self,filename):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in filename if c in valid_chars)
        return self.applicationSupportFolder().stringByAppendingPathComponent_(filename)
