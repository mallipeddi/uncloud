#
#  UncloudController.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

import objc
from Foundation import *
from BackgroundTasks import LoginTask

class UncloudController(NSObject):
    loginSheet = objc.IBOutlet()
    accountEmail = objc.ivar(u"accountEmail")
    accountPassword = objc.ivar(u"accountPassword")
    
    @objc.IBAction
    def showLoginSheet_(self, sender):
        self.displayLoginSheet()
    
    @objc.IBAction
    def endLoginSheet_(self, sender):
        NSLog(u"Removing the login sheet...")
        app = NSApplication.sharedApplication()
        app.endSheet_(self.loginSheet)
        self.loginSheet.orderOut_(sender)
        NSLog(u"Creating task to fetch labels for %@:%@", self.accountEmail, self.accountPassword)
        loginTask = LoginTask.alloc().init()
        loginTask.initTask(self.accountEmail, self.accountPassword)
        loginTask.addObserver_forKeyPath_options_context_(self, u"isFinished", NSKeyValueObservingOptionNew, None)
        myQueue = app.delegate().opQ
        myQueue.addOperation_(loginTask)

    def displayLoginSheet(self):
        NSLog(u"Displaying login sheet...")
        self.accountEmail = None
        self.accountPassword = None
        app = NSApplication.sharedApplication()
        app.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(self.loginSheet, app.mainWindow(), None, None, None)

    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        if(keyPath.isEqual_(u"isFinished") and change.objectForKey_(NSKeyValueChangeNewKey)):
            NSLog("%@", object.get_labels())
            #object.release()