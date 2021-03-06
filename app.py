from flask import Flask, jsonify, request, Response
from collections import OrderedDict
import json
from azure.eventhub import EventHubProducerClient, EventData
import datetime

EVENTHUBCONNECTIONSTRING = "Endpoint=sb://sensor-partner-eh-namespace-63et4.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=xCqkPnpUo2wyuahem2jHnacc/cPkGlm0Ptu4+wnyFwg="
EVENTHUBNAME = "sensor-partner-eh-00"
client = EventHubProducerClient.from_connection_string(EVENTHUBCONNECTIONSTRING, eventhub_name=EVENTHUBNAME)

app = Flask(__name__)


@app.route('/senml/api/v1.0/send', methods=['POST'])
def post_senml_message():
    converted_message_dict = OrderedDict()
    senml_message = request.get_json()
    print(senml_message)
    sensor_header = senml_message[0]
    base_version = sensor_header['bver']
    base_number = sensor_header['bn'][12:].split('_')
    sensor_serial_number = base_number[0]
    mac_address_deveui = base_number[1]
    radio_signal_type = sensor_header['u']
    radio_signal_strength = sensor_header['v']
    basetime = senml_message[0]['bt']
    converted_message_dict['base_version'] = base_version
    converted_message_dict['sensor_serial_number'] = sensor_serial_number
    converted_message_dict['mac_address_DevEUI'] = mac_address_deveui
    converted_message_dict[radio_signal_type] = radio_signal_strength
    converted_message_dict['reading_timestamp'] = basetime

    device_location_latitude = senml_message[1]['v']
    device_location_longitude = senml_message[2]['v']
    converted_message_dict['location'] = OrderedDict()
    converted_message_dict['location']['latitude'] = device_location_latitude
    converted_message_dict['location']['longitude'] = device_location_longitude

    battery_energy_level = senml_message[3]['v']
    converted_message_dict['battery_energy_level'] = battery_energy_level

    sensor_reading = senml_message[4]
    converted_message_dict['measurement'] = OrderedDict()
    converted_message_dict['measurement']['soil_moisture_content'] = sensor_reading['v']
    converted_message_dict['measurement']['soil_depth'] = sensor_reading['depth']
    converted_message_dict['measurement']['soil_type'] = sensor_reading['soil']
    current_time_iso = datetime.datetime.now().isoformat()
    telemetry = {
        "deviceid": "500244ee-2fd0-40eb-bb80-10ff19c4aeea",
        "timestamp": current_time_iso,
        "version": "1",
        "sensors": [
            {
                "id": "8555eeb3-a550-4e75-a1b3-f77602842330",
                "sensordata": [
                    {
                        "timestamp": current_time_iso,
                        "Volumetric Water Content (%)": converted_message_dict['measurement']['soil_moisture_content']
                    }
                ]
            }
        ]
    }
    event_data_batch = client.create_batch()
    try:
        event_data = EventData(json.dumps(telemetry))
        print(event_data)
        event_data_batch.add(event_data)
    except:  # EventDataBatch object reaches max_size.
        Response(json.dumps({"message": "Error with eventhub"}, default=str), status=500, mimetype='application/json')
    client.send_batch(event_data_batch)

    return Response(json.dumps(converted_message_dict, default=str), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
