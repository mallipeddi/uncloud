#
#  UncloudController.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

import objc
from Foundation import *
from gmail2amail import Account

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
        NSLog(u"%@:%@", self.accountEmail, self.accountPassword)
        gmailAcc = Account(self.accountEmail, self.accountPassword)
        NSLog(u"%@", gmailAcc.get_labels())

    def displayLoginSheet(self):
        NSLog(u"Displaying login sheet...")
        self.accountEmail = None
        self.accountPassword = None
        app = NSApplication.sharedApplication()
        app.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(self.loginSheet, app.mainWindow(), None, None, None)
