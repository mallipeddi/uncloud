#
#  main.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/14/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import UncloudAppDelegate
import UncloudController
import BackupController
import BackupCollectionView

# pass control to AppKit
AppHelper.runEventLoop()
