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

        client.call ("ak.wwise.core.undo.beginGroup")

        for soundObj in paths:
            try:
                split = os.path.split(soundObj)
             
                randomArgs = {
                    "object":soundObj,
                    "property" : "Pitch",
                    "enabled": True,
                    "min": -150, 
                    "max" : 150
                    }
              
                client.call("ak.wwise.core.object.setRandomizer", randomArgs)
            except Exception as e: 
                print(e)
                input()

        undoArgs = {"displayName": "Add random pitch to containers"}
        client.call ("ak.wwise.core.undo.endGroup",undoArgs)

except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

