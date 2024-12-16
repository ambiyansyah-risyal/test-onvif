from onvif import ONVIFCamera
import urllib.parse
import json

def get_stream_uri(device):
    try:
        camera = ONVIFCamera(device["URL"], device["TCP Port"], device["ONVIF USER NAME"], device["ONVIF PSW"])
        media_service = camera.create_media_service()
        profiles = media_service.GetProfiles()
        token = profiles[0].token
        stream_uri = media_service.GetStreamUri({'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'RTSP'}, 'ProfileToken': token}).Uri
        # Correctly format the RTSP URL with the custom RTSP port and encoded credentials
        username = urllib.parse.quote(device['ONVIF USER NAME'])
        password = urllib.parse.quote(device['ONVIF PSW'])
        stream_uri = stream_uri.replace("rtsp://", f"rtsp://{username}:{password}@")
        stream_uri = stream_uri.replace(device["URL"], f"{device['URL']}:{device['RTSP Port']}")
        return stream_uri
    except Exception as e:
        print(f"Failed to get stream URI for {device['Camera']}: {e}")
        return None

if __name__ == "__main__":
    with open('connected_devices.json', 'r') as json_file:
        devices = json.load(json_file)
    
    stream_uris = {}
    for device in devices:
        stream_uri = get_stream_uri(device)
        if stream_uri:
            stream_uris[device['Camera']] = stream_uri
            print(f"Live view URI for {device['Camera']}: {stream_uri}")
    
    with open('stream_uris.json', 'w') as json_file:
        json.dump(stream_uris, json_file, indent=4)
        print("Stream URIs saved to stream_uris.json")
