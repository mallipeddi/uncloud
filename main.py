#
#  main.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright Harish Mallipeddi 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import UncloudAppDelegate, UncloudController, BackupController, BackupStatusView, FlippedView

# pass control to AppKit
AppHelper.runEventLoop()
