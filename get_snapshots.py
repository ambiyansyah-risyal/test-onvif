from onvif import ONVIFCamera
import json
import os
import requests
from requests.auth import HTTPDigestAuth

def get_snapshot(device):
    try:
        camera = ONVIFCamera(device["URL"], device["TCP Port"], device["ONVIF USER NAME"], device["ONVIF PSW"])
        media_service = camera.create_media_service()
        profiles = media_service.GetProfiles()
        token = profiles[0].token
        snapshot_uri = media_service.GetSnapshotUri({'ProfileToken': token}).Uri
        print(f"Snapshot URI for {device['Camera']}: {snapshot_uri}")
        
        # Log the credentials being used
        print(f"Using credentials: {device['ONVIF USER NAME']} / {device['ONVIF PSW']}")
        
        # Download the snapshot and save it to the output directory with digest authentication
        response = requests.get(snapshot_uri, auth=HTTPDigestAuth(device["ONVIF USER NAME"], device["ONVIF PSW"]))
        if response.status_code == 200:
            output_dir = 'output'
            os.makedirs(output_dir, exist_ok=True)
            snapshot_path = os.path.join(output_dir, f"{device['Camera']}_snapshot.jpg")
            with open(snapshot_path, 'wb') as file:
                file.write(response.content)
            print(f"Snapshot saved to {snapshot_path}")
        else:
            print(f"Failed to download snapshot for {device['Camera']}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Failed to get snapshot for {device['Camera']}: {e}")

if __name__ == "__main__":
    with open('connected_devices.json', 'r') as json_file:
        devices = json.load(json_file)
    
    for device in devices:
        get_snapshot(device)
