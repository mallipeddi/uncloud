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

    def initWith_(self, gmailAccount, label_name):
        NSLog(u"trying to load from nib file...")
        if not super(BackupController, self).initWithNibName_bundle_(u"BackupStatus", None):
            return None
        self.statusMsg = u"Initiating backup..."
        self.label_name = label_name
        
        backupTask = BackupTask.alloc().init()
        backupTask.initTask(gmailAccount, label_name)
        backupTask.addObserver_forKeyPath_options_context_(self, u"isFinished", NSKeyValueObservingOptionNew, BACKUPTASKCONTEXT)
        app = NSApplication.sharedApplication()
        opQ = app.delegate().opQ
        opQ.addOperation_(backupTask)

        return self
    
    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        if(keyPath.isEqual_(u"isFinished") and context == BACKUPTASKCONTEXT):
            #change.objectForKey_(NSKeyValueChangeNewKey)
            self.statusMsg = u"Finished downloading."
