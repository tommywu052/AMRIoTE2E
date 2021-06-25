# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
import datetime

import asyncio
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult
from random import randint
import json
import asyncio
import websockets


# Fetch the connection string from an enviornment variable
conn_str = "HostName=a9dmhub.azure-devices.net;DeviceId=mydevice01;SharedAccessKey=" #os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

# Create instance of the device client using the connection string
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# Connect the device client.
device_client.connect()
# set the twin patch handler on the client


async def sendWssMsg(uri,iotmsg):
    async with websockets.connect(uri) as websocket:
        await websocket.send(iotmsg)
        print(f"(client) send to server: "+str(iotmsg))
        



# define behavior for receiving a twin patch
def twin_patch_handler(patch):
    #print(type(patch))
    print("the data in the desired properties patch was: {}".format(patch))
    #reported_properties = {"demotwin": patch['demotwin']  }
    #obj = json.dumps(patch)
    #print(patch['demotwin'])
    #device_client.patch_twin_reported_properties(reported_properties)

def sendMessage():
    
    temperature =  str(randint(20, 40))
    humidity = str(randint(40, 90))
    # Send a single message    
    msgbody = { 'temperature': temperature, 'humidity': humidity }
    print("Sending message..."+ str(msgbody))
    msg = Message(json.dumps(msgbody))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"

    device_client.send_message(msg)
    print("Message successfully sent!")
    wssdata = {"IotData":{"temperature":temperature,"humidity":humidity},"MessageDate":datetime.datetime.now().isoformat(),"DeviceId":"mydevice01"}
    asyncio.get_event_loop().run_until_complete(
    sendWssMsg('ws://localhost:13000',str(wssdata)))
    print(str(wssdata))
    time.sleep(10)

    # Finally, shut down the client
    #await device_client.shutdown()
device_client.on_twin_desired_properties_patch_received = twin_patch_handler


# get the twin
twin = device_client.get_twin()
print("Twin document:")
print("{}".format(twin))

while True:
    sendMessage()
#    selection = input("Press Q to quit\n")
#    if selection == "Q" or selection == "q":
#        print("Quitting...")
#        break
    #sendMessage()
#if __name__ == "__main__":

#    loop = asyncio.get_event_loop()
#    while True :
#      loop.run_until_complete(main())
      #print("Send Event")
#      time.sleep(2)
    #asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
