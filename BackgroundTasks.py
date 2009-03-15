#
#  UncloudTask.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/15/09.
#  Copyright (c) 2009 __MyCompanyName__. All rights reserved.
#

import objc
from Foundation import *
from gmail2amail import Account

class LoginTask(NSOperation):
    def initTask(self, accountEmail, accountPassword):
        self.accountEmail = accountEmail
        self.accountPassword = accountPassword
        self.labels = []
    
    def main(self):
        NSLog("Executing main = %@, %@", self.accountEmail, self.accountPassword)
        gmailAcc = Account(self.accountEmail, self.accountPassword)
        self.labels = gmailAcc.get_labels()
        NSLog("Fetched labels = %@", self.labels)
    
    def get_labels(self):
        return self.labels

    def dealloc(self):
        NSLog("dealloc on task invoked")
        super(LoginTask, self).dealloc()
