from onvif import ONVIFCamera
import pandas as pd
import json

# Load devices from JSON file
with open('tested_devices.json', 'r') as file:
    devices = json.load(file)

def check_connection(device):
    try:
        camera = ONVIFCamera(device["URL"], device["TCP Port"], device["ONVIF USER NAME"], device["ONVIF PSW"])
        camera.devicemgmt.GetHostname()
        print(f"Connection to {device['Camera']} successful.")
        return True
    except Exception as e:
        print(f"Failed to connect to {device['Camera']}: {e}")
        return False

def get_device_information(device):
    try:
        camera = ONVIFCamera(device["URL"], device["TCP Port"], device["ONVIF USER NAME"], device["ONVIF PSW"])
        device_info = camera.devicemgmt.GetDeviceInformation()
        return {
            "Camera": device['Camera'],
            "Manufacturer": device_info.Manufacturer,
            "Model": device_info.Model,
            "Firmware Version": device_info.FirmwareVersion,
            "Serial Number": device_info.SerialNumber,
            "Hardware ID": device_info.HardwareId
        }
    except Exception as e:
        print(f"Failed to get device information for {device['Camera']}: {e}")
        return None

if __name__ == "__main__":
    device_info_list = []
    for device in devices:
        if check_connection(device):
            info = get_device_information(device)
            if info:
                print(info)
            device_info_list.append(device)
    
    df = pd.DataFrame(device_info_list)
    print(df.to_string(index=False))
    
    # Save to JSON file
    with open('connected_devices.json', 'w') as json_file:
        json.dump(device_info_list, json_file, indent=4)
