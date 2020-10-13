from flask import Flask, jsonify, request, Response
from collections import OrderedDict
import json

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

    return Response(json.dumps(converted_message_dict, default=str), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
