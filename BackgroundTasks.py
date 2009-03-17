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
        self.account = gmail2amail.Account(self.accountEmail, self.accountPassword)
    
    def get_account(self):
        return self.account

class BackupTask(NSOperation):
    totalEmails = objc.ivar(u"totalEmails")
    fetchedEmails = objc.ivar(u"fetchedEmails")

    def initTask(self, gmailAccount, label_name, destPath):
        # convert NSString to python string before sending off to pure Python code
        pyStr = label_name.UTF8String()
        self.label = gmailAccount.get_label(pyStr)
        self.mboxWriter = gmail2amail.MboxrdWriter(destPath)
    
    def main(self):
        NSLog(u"Fetching emails...")
        for email in self.label:
            self.setValue_forKey_(self.label.total, u"totalEmails")
            self.setValue_forKey_(self.label.fetched, u"fetchedEmails")
            self.mboxWriter.append(email)
        NSLog(u"Done fetching emails...")
        self.mboxWriter.close()
        self.label.close()
