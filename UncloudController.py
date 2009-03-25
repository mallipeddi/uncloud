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

LOGINTASKFINISHED = 1
BACKUPSTATUSVIEWFINISHED = 1

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

        # create and set the content view for the scroll view
        # this content view is a flipped view which contains multiple BackupStatusViews (one-per-backup-initiated).
        scrollFrameSize = self.backupsScrollView.frame().size
        contentFrameSize = NSScrollView.contentSizeForFrameSize_hasHorizontalScroller_hasVerticalScroller_borderType_(
                                            scrollFrameSize, False, True, NSBezelBorder)
        self.backupsView = FV.alloc().initWithFrame_(NSMakeRect(0, 0, contentFrameSize.width, 0))
        self.backupsScrollView.setDocumentView_(self.backupsView)
        self.backupsScrollView.setHasVerticalScroller_(True)
        self.backupsScrollView.setBorderType_(NSBezelBorder)
        self.backupsScrollView.setBackgroundColor_(NSColor.windowBackgroundColor())

        app = NSApplication.sharedApplication()
        app.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(self.loginSheet, self.mainWindow, None, None, None)
    
    @objc.IBAction
    def doLogin_(self, sender):
        app = NSApplication.sharedApplication()
        
        self.loginProgressIndicator.startAnimation_(self)
        self.loginProgressIndicator.setHidden_(False)
        self.loginStatusLabel.setTextColor_(NSColor.blackColor())
        self.loginStatusLabel.setStringValue_(u"Logging in...")
        self.loginStatusLabel.setHidden_(False)
        
        # start background task to login and fetch labels
        loginTask = LoginTask.alloc().init()
        loginTask.initTask(self.accountEmail, self.accountPassword)
        loginTask.addObserver_forKeyPath_options_context_(self, u"isFinished", NSKeyValueObservingOptionNew, LOGINTASKFINISHED)
        opQ = app.delegate().opQ
        opQ.addOperation_(loginTask)

    @objc.IBAction
    def doLoginCancel_(self, sender):
        app = NSApplication.sharedApplication()
        app.endSheet_(self.loginSheet)
        self.loginSheet.orderOut_(self)
        app.terminate_(self)

    @objc.IBAction
    def startBackup_(self, sender):
        "start an instance of a BackupController and add it's view as a subView of the container view"
        
        if self.selectedLabel:
            backupController = BC.alloc().initWith_(self.account, self.selectedLabel)
            self.backups.addObject_(backupController)
            backupsCount = self.backups.count()

            aView = backupController.view()
            height = aView.frame().size.height        
            oldWidth = self.backupsView.frame().size.width
            altColors = NSColor.controlAlternatingRowBackgroundColors()
            aView.drawWithWidth_fillColor_(oldWidth, altColors.objectAtIndex_(backupsCount % altColors.count()))
            
            self.backupsView.setFrameSize_(NSSize(oldWidth, height * backupsCount))
            self.backupsView.addSubview_(aView)

    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        if(keyPath.isEqual_(u"isFinished") and change.objectForKey_(NSKeyValueChangeNewKey)):
            if(context == LOGINTASKFINISHED):
                self.loginProgressIndicator.stopAnimation_(self)
                
                self.account = object.get_account()
                if self.account and self.account.labels:
                    # login succeeded. let's close the login sheet
                    app = NSApplication.sharedApplication()
                    app.endSheet_(self.loginSheet)
                    self.loginSheet.orderOut_(self)
                    self.labels = self.account.labels
                else:
                    # login failed
                    self.loginStatusLabel.setTextColor_(NSColor.redColor())
                    self.loginStatusLabel.setStringValue_(u"Login failed.")
            elif(context == BACKUPSTATUSVIEWFINISHED):
                # BackupStatusViewController has finished. Let's remove it from the controllers list.
                self.backups.removeObject_(object)
