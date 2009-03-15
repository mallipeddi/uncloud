#
#  BackupController.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/15/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

import objc
from Foundation import *
from BackgroundTasks import BackupTask

BACKUPTASKCONTEXT = 1

class BackupController(NSViewController):
    statusMsg = objc.ivar(u"statusMsg")
    totalEmails = objc.ivar(u"totalEmails")
    fetchedEmails = objc.ivar(u"fetchedEmails")

    def initWith_(self, gmailAccount, label_name):
        NSLog(u"trying to load from nib file...")
        if not super(BackupController, self).initWithNibName_bundle_(u"BackupStatus", None):
            return None
        self.statusMsg = u"Initiating backup..."
        self.label_name = label_name

        app = NSApplication.sharedApplication()        

        backupTask = BackupTask.alloc().init()
        destPath = app.delegate().pathForFilename("%s.mbox" % label_name)
        NSLog(u"destPath = %@", destPath)
        backupTask.initTask(gmailAccount, label_name, destPath)
        backupTask.addObserver_forKeyPath_options_context_(self, u"isFinished", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)
        backupTask.addObserver_forKeyPath_options_context_(self, u"totalEmails", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)
        backupTask.addObserver_forKeyPath_options_context_(self, u"fetchedEmails", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)

        self.totalEmails = None
        self.fetchedEmails = None

        opQ = app.delegate().opQ
        opQ.addOperation_(backupTask)

        return self
    
    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        changedVal = change.objectForKey_(NSKeyValueChangeNewKey)
        if(context == BACKUPTASKCONTEXT):
            if(keyPath.isEqual_(u"isFinished") and changedVal): # if isFinished is True
                if(self.totalEmails is not None and self.fetchedEmails == self.totalEmails):
                    self.statusMsg = u"Backup complete."
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
