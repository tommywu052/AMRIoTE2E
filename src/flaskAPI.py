# -*- coding: UTF-8 -*-
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult

app = Flask(__name__)
CORS(app)

IOTHUB_CONNECTION_STRING = "YourIoTHubConnectionString"
iothub_registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

@app.route('/')
def index():
    return 'hello!!'

@app.route('/getDevices', methods=['GET'])
def postInput():
    # 取得前端傳過來的數值
    print(request.args['filterValue'])
    #insertValues = request.get_json()
    #x1=insertValues['filterValue']
    #print(insertValues)
    
    query_spec = QuerySpecification(query="SELECT * FROM devices")
    query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 10)
    #print([twin for twin in query_result.items])
    #print("Devices List: {}".format(', '.join([twin.device_id+','+twin.connection_state for twin in query_result.items])))
    
    result = "{}".format(', '.join([twin.device_id+':'+twin.connection_state for twin in query_result.items]))

    return jsonify({'return': str(result)})

@app.route('/createDevice', methods=['POST'])
def postCreateDevice():
     # Create a device
    record = json.loads(request.data)
    device_id = record['deviceid']

    primary_key = "aaabbbcccdddeeefffggghhhiiijjjkkklllmmmnnnoo"
    secondary_key = "111222333444555666777888999000aaabbbcccdddee"
    device_state = "enabled"
    new_device = iothub_registry_manager.create_device_with_sas(
        device_id, primary_key, secondary_key, device_state
    )
    print("device_id                      = {0}".format(new_device.device_id))
    #print_device_info("create_device", new_device)
    return "success"

@app.route('/deleteDevice', methods=['POST'])
def postDeleteDevice():
    
    record = json.loads(request.data)
    device_id = record['deviceid']
    print(device_id)
     # Delete the device
    iothub_registry_manager.delete_device(device_id)

    return "success"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31000, debug=True)