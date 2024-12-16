from fastapi import FastAPI, Response
import cv2
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import json
from starlette.responses import StreamingResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get(request: Request):
    with open('stream_uris.json') as f:
        rtsp_urls = json.load(f)
    camera_ids = list(rtsp_urls.keys())
    return templates.TemplateResponse("index.html", {"request": request, "camera_ids": camera_ids})

def generate_video_stream(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame to reduce the size
        frame = cv2.resize(frame, (640, 480))  # Adjust the resolution as needed
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/video/{camera_id}")
async def video_feed(camera_id: str):
    with open('stream_uris.json') as f:
        rtsp_urls = json.load(f)
    rtsp_url = rtsp_urls.get(camera_id)
    if not rtsp_url:
        return Response(status_code=404)
    return StreamingResponse(generate_video_stream(rtsp_url), media_type='multipart/x-mixed-replace; boundary=frame')
