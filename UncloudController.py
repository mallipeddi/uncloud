#
#  UncloudController.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright (c) 2009 Harish Mallipeddi. All rights reserved.
#

import objc
from Foundation import *
from AppKit import *
from BackgroundTasks import LoginTask
from BackupController import BackupController as BC
from FlippedView import FlippedView as FV

class UncloudController(NSObject):
    mainWindow = objc.IBOutlet()
    
    # login sheet
    loginSheet = objc.IBOutlet()
    accountEmail = objc.ivar(u"accountEmail")
    accountPassword = objc.ivar(u"accountPassword")
    loginProgressIndicator = objc.IBOutlet()
    loginStatusLabel = objc.IBOutlet()
    
    # backups
    labels = objc.ivar(u"labels")
    selectedLabel = objc.ivar(u"selectedLabel")
    backupsScrollView = objc.IBOutlet()
    
    def displayLoginSheet(self):
        NSLog(u"Displaying login sheet...")

        self.backups = NSMutableArray.alloc().init()
        self.accountEmail = None
        self.accountPassword = None

        self.loginStatusLabel.setHidden_(True)
        self.loginProgressIndicator.setHidden_(True)

        app = NSApplication.sharedApplication()
        app.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(self.loginSheet, self.mainWindow, None, None, None)
        
        self.backupsView = FV.alloc().initWithFrame_(NSMakeRect(0, 0, 510, 0))
        # set a Flipped NSView as the document view for the NSScrollView
        # in order to position the document view at the top-left corner
        self.backupsScrollView.setDocumentView_(self.backupsView)
        self.backupsScrollView.setHasVerticalScroller_(True)
    
    @objc.IBAction
    def doLogin_(self, sender):
        app = NSApplication.sharedApplication()
        
        NSLog(u"Trying to login with %@:%@", self.accountEmail, self.accountPassword)
        self.loginProgressIndicator.startAnimation_(self)
        self.loginProgressIndicator.setHidden_(False)
        self.loginStatusLabel.setTextColor_(NSColor.blackColor())
        self.loginStatusLabel.setStringValue_(u"Logging in...")
        self.loginStatusLabel.setHidden_(False)
        
        # start background task to login and fetch labels
        loginTask = LoginTask.alloc().init()
        loginTask.initTask(self.accountEmail, self.accountPassword)
        loginTask.addObserver_forKeyPath_options_context_(self, u"isFinished", NSKeyValueObservingOptionNew, None)
        opQ = app.delegate().opQ
        opQ.addOperation_(loginTask)

    @objc.IBAction
    def startBackup_(self, sender):
        backupController = BC.alloc().initWith_(self.account, self.selectedLabel)
        
        aView = backupController.view()
        height = aView.frame().size.height
        #aView.setFrameOrigin_(NSMakePoint(0.0, height * self.backups.count()))
        self.backups.addObject_(backupController)
        
        oldWidth = self.backupsView.frame().size.width
        #self.backupsView.setFrameOrigin_(NSMakePoint(0.0, 50.0))
        self.backupsView.setFrameSize_(NSSize(oldWidth, height * self.backups.count()))
        self.backupsView.addSubview_(aView)


    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        if(keyPath.isEqual_(u"isFinished") and change.objectForKey_(NSKeyValueChangeNewKey)):
            self.loginProgressIndicator.stopAnimation_(self)
            
            self.account = object.get_account()
            if self.account and self.account.labels:
                # login succeeded. let's close the login sheet
                NSLog(u"Removing the login sheet...")
                app = NSApplication.sharedApplication()
                app.endSheet_(self.loginSheet)
                self.loginSheet.orderOut_(self)
                self.labels = self.account.labels
            else:
                # login failed
                self.loginStatusLabel.setTextColor_(NSColor.redColor())
                self.loginStatusLabel.setStringValue_(u"Login failed.")

    def dealloc(self):
        NSLog("dealloc called on UncloudController")
        self.backups.release()
        super(UncloudController, self).dealloc()

