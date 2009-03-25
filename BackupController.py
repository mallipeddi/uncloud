#
#  BackupController.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/15/09.
#  Copyright (c) 2009 Harish Mallipeddi. All rights reserved.
#

import objc
from Foundation import *
from BackgroundTasks import BackupTask

BACKUPTASKCONTEXT = 1
BACKUPVIEWFINISHEDDND = 2

class BackupController(NSViewController):
    isFinished = objc.ivar(u"isFinished")
    statusMsg = objc.ivar(u"statusMsg")
    statusMsgFont = objc.ivar(u"statusMsgFont")
    totalEmails = objc.ivar(u"totalEmails")
    fetchedEmails = objc.ivar(u"fetchedEmails")

    def initWith_(self, gmailAccount, label_name):
        if not super(BackupController, self).initWithNibName_bundle_(u"BackupStatus", None):
            return None

        self.statusMsg = u"Initiating backup..."
        self.statusMsgFont = NSFont.messageFontOfSize_(11.0)
        self.label_name = label_name
        self.totalEmails = None
        self.fetchedEmails = None

        app = NSApplication.sharedApplication()        

        # start background task to fetch emails and write to disk
        backupTask = BackupTask.alloc().init()
        self.backupFilePath = app.delegate().pathForFilename("%s.mbox" % label_name)
        backupTask.initTask(gmailAccount, label_name, self.backupFilePath)
        backupTask.addObserver_forKeyPath_options_context_(self, u"isFinished", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)
        backupTask.addObserver_forKeyPath_options_context_(self, u"totalEmails", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)
        backupTask.addObserver_forKeyPath_options_context_(self, u"fetchedEmails", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)

        opQ = app.delegate().opQ
        opQ.addOperation_(backupTask)

        return self
    
    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        # track the progress of the background task by observing the relevant keys
        changedVal = change.objectForKey_(NSKeyValueChangeNewKey)
        if(context == BACKUPTASKCONTEXT):
            if(keyPath.isEqual_(u"isFinished") and changedVal): # if isFinished is True
                if(self.totalEmails is not None and self.fetchedEmails == self.totalEmails):
                    self.statusMsg = u"\"%s\" complete. Drag into desired location in Finder." % self.label_name
                    self.view().addObserver_forKeyPath_options_context_(self, u"performedDnD", NSKeyValueObservingOptionNew, BACKUPVIEWFINISHEDDND)
                    self.view().prepareForDnD(self.backupFilePath)
                else:
                    self.statusMsg = u"Backup failed."
                object.removeObserver_forKeyPath_(self, u"isFinished")
                object.removeObserver_forKeyPath_(self, u"totalEmails")
                object.removeObserver_forKeyPath_(self, u"fetchedEmails")
            elif keyPath.isEqual_(u"totalEmails"):
                self.totalEmails = changedVal
                self.statusMsg = u"Found %s emails in \"%s\"" % (str(self.totalEmails), self.label_name)
            elif keyPath.isEqual_(u"fetchedEmails"):
                self.fetchedEmails = changedVal
                self.statusMsg = u"Fetched %s of %s emails in \"%s\"" % (
                                    str(self.fetchedEmails), str(self.totalEmails), self.label_name)
            else:
                pass
        elif(context == BACKUPVIEWFINISHEDDND):
            self.setValue_forKey_(True, u"isFinished")
        else:
            pass
