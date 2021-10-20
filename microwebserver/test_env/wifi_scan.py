import wifi


for network in wifi.radio.start_scanning_networks():
    print(f'[{network.ssid}] channel: {network.channel}, rssi: {network.rssi}')
