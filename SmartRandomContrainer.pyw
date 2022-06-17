from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint
import os
import re
import sys

try:

    # Connecting to Waapi using default URL

    with WaapiClient() as client:
        paths = sys.argv
        del paths[0]

        prevParentName = ''

        client.call ("ak.wwise.core.undo.beginGroup")

        for soundObj in paths:
            split = os.path.split(soundObj)
            parent = split[0]
            name = split[1]
          
            parentName = re.sub('[0-9]','',name)
            parentName = parentName.rstrip("_")

         
            if parentName != prevParentName:
                randomContainerArgs = {

                    "parent": parent,
                    "type": "RandomSequenceContainer",
                    "name": parentName,  
                    "onNameConflict": "merge"
                }
        
                result = client.call ("ak.wwise.core.object.create", randomContainerArgs)
                prevParentName = parentName


            parentId = result["id"]
       
            reparentingArgs = {

                "object": soundObj,
                "parent": parentId,
                "onNameConflict": "rename"
            }

            client.call ("ak.wwise.core.object.move", reparentingArgs)


        undoArgs = {"displayName": "Add Objects to RandomContainer on matching name"}
        client.call ("ak.wwise.core.undo.endGroup",undoArgs)

except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

