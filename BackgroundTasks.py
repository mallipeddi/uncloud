#
#  UncloudTask.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/15/09.
#  Copyright (c) 2009 Harish Mallipeddi. All rights reserved.
#

import objc
from Foundation import *
import gmail2amail

class LoginTask(NSOperation):
    def initTask(self, accountEmail, accountPassword):
        self.accountEmail = accountEmail
        self.accountPassword = accountPassword
        self.account = None
    
    def main(self):
        NSLog("Executing main = %@, %@", self.accountEmail, self.accountPassword)
        self.account = gmail2amail.Account(self.accountEmail, self.accountPassword)
        NSLog("Fetched labels = %@", self.account.labels)
    
    def get_account(self):
        return self.account

    def dealloc(self):
        NSLog("dealloc on task invoked")
        super(LoginTask, self).dealloc()

class BackupTask(NSOperation):
    def initTask(self, gmailAccount, label_name):
        self.label = gmailAccount.get_label(label_name)
        self.mboxWriter = gmail2amail.MboxrdWriter(u"/Users/harish/Code/%s.mbox" % label_name)
    
    def main(self):
        NSLog(u"Fetching emails...")
        for email in self.label:
            self.mboxWriter.append(email)
        NSLog(u"Done fetching emails...")
        self.mboxWriter.close()
        self.label.close()

        