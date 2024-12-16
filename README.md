# Test ONVIF Project

This project is designed to interact with ONVIF-compliant devices using Python. It leverages various libraries such as FastAPI, Zeep, and OpenCV to provide a comprehensive solution for ONVIF device management and video processing.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Running the FastAPI Server

To start the FastAPI server, use the following command:

```bash
uvicorn main:app --reload
```

This will start the server on `http://127.0.0.1:8000`.

### Interacting with ONVIF Devices

You can interact with ONVIF devices using the provided API endpoints. Refer to the FastAPI documentation for detailed information on available endpoints and their usage.

### Scripts

#### `main.py`

This script sets up a FastAPI server to serve video streams from ONVIF devices. It includes endpoints to:

- Serve the main page with a list of available cameras.
- Stream video from a specified camera.

#### `get_snapshots.py`

This script connects to ONVIF devices and retrieves snapshots. It:

- Connects to each device using ONVIF credentials.
- Retrieves the snapshot URI.
- Downloads the snapshot and saves it locally.

#### `get_live_view.py`

This script retrieves the RTSP stream URIs for live viewing from ONVIF devices. It:

- Connects to each device using ONVIF credentials.
- Retrieves the stream URI.
- Formats the URI with the correct credentials and port.
- Saves the URIs to a JSON file.

#### `check_onvif_connection.py`

This script checks the connection to ONVIF devices and retrieves device information. It:

- Connects to each device using ONVIF credentials.
- Checks if the connection is successful.
- Retrieves device information such as manufacturer, model, firmware version, etc.
- Saves the connected devices' information to a JSON file.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
