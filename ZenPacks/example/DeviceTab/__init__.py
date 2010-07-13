
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from copy import copy
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW

# Get a copy of the device tab definitions.
custom_actions = []
custom_actions.extend(Device.factory_type_information[0]['actions'])

# Add our custom "MyTab" in position 4. This is right before Events.
custom_actions.insert(4, dict(
    id="myTabDetail",
    name="MyTab",
    action="myTabDetail",
    permissions=(ZEN_VIEW,),
    ))

# Set the device tab definitions to our custom set.
Device.factory_type_information[0]['actions'] = custom_actions


# Make a copy of the original method so we can augment it.
original_zentinelTabs = copy(Device.zentinelTabs)

# Create a new zentinelTabs method that filters out our tab for non-servers.
def new_zentinelTabs(self, templateName):
    tabs = super(Device, self).zentinelTabs(templateName)
    if self.getDeviceClassName().startswith('/Server'):
        return tabs
    else:
        return [ t for t in tabs if t['name'] != 'MyTab' ]

# Replace the zentinelTabs method with our own.
Device.zentinelTabs = new_zentinelTabs
