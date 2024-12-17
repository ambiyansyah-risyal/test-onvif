from onvif import ONVIFCamera
import json

# Load devices from JSON file
with open('connected_devices.json', 'r') as file:
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

def get_recording_information(device):
    try:
        camera = ONVIFCamera(device["URL"], device["TCP Port"], device["ONVIF USER NAME"], device["ONVIF PSW"])
        services = camera.devicemgmt.GetServices(False)
        
        if 'http://www.onvif.org/ver10/recording/wsdl' not in [service.Namespace for service in services]:
            print(f"Device {device['Camera']} does not support recording service.")
            return None
        
        # Manually set the xaddr for the recording service
        camera.xaddrs['http://www.onvif.org/ver10/recording/wsdl'] = f"http://{device['URL']}:{device['TCP Port']}/onvif/services"
        
        # Ensure credentials are passed correctly
        recording_service = camera.create_recording_service()
        
        # List available methods and their descriptions
        print(f"Available methods for recording service on {device['Camera']}:")
        for method in dir(recording_service):
            if not method.startswith('_'):
                print(f"Method: {method}")
                try:
                    doc = getattr(recording_service, method).__doc__
                    if doc:
                        print(f"Description: {doc}")
                except AttributeError:
                    pass
                print()
        
        # Fetch recordings
        recordings = recording_service.GetRecordings()
        
        if not recordings:
            print(f"No recordings found for {device['Camera']}.")
        
        return {
            "Camera": device['Camera'],
            "Recordings": recordings
        }
    except Exception as e:
        print(f"Failed to get recording information for {device['Camera']}: {e}")
        return None

if __name__ == "__main__":
    recording_info_list = []
    for device in devices:
        if check_connection(device):
            recording_info = get_recording_information(device)
            if recording_info:
                recording_info_list.append(recording_info)
    
    # Print recording information to console
    for info in recording_info_list:
        print(json.dumps(info, indent=4))
