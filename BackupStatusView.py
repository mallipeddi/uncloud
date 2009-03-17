#
#  BackupStatusView.py
#  Uncloud
#
#  Created by Harish Mallipeddi on 3/17/09.
#  Copyright (c) 2009 Harish Mallipeddi. All rights reserved.
#

import objc
from Foundation import *
from AppKit import *

class BackupStatusView(NSView):
    performedDnD = objc.ivar(u"performedDnD")

    def initWithFrame_(self, frame):
        self = super(BackupStatusView, self).initWithFrame_(frame)
        if self:
            self.enableDnD = False
        return self

    def prepareForDnD(self, backupFilePath):
        self.enableDnD = True
        self.backupFilePath = backupFilePath
        self.setValue_forKey_(False, u"performedDnd")

    def draggingSourceOperationMaskForLocal_(self, isLocal):
        return NSDragOperationMove

    def mouseDragged_(self, event):
        if self.enableDnD:            
            # write data to pasteboard
            filelist = NSArray.arrayWithObject_(self.backupFilePath)
            pboard = NSPasteboard.pasteboardWithName_(NSDragPboard)
            pboard.declareTypes_owner_(NSArray.arrayWithObject_(NSFilenamesPboardType), None)
            pboard.setPropertyList_forType_(filelist, NSFilenamesPboardType)
            
            # start drag operation
            dragImage = NSWorkspace.sharedWorkspace().iconForFile_(self.backupFilePath)
            dragPosition = self.convertPoint_fromView_(event.locationInWindow(), None)
            self.dragImage_at_offset_event_pasteboard_source_slideBack_(
                dragImage, dragPosition, NSZeroSize, event, pboard, self, objc.YES)
    
    def draggedImage_endedAt_operation_(self, image, screenPoint, operationPerformed):
        NSLog(u"DnD operation (%@) performed successfully", operationPerformed)
        self.setValue_forKey_(True, u"performedDnd")
        self.removeFromSuperview()
