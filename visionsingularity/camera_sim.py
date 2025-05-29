import cv2, requests, time

camera = cv2.VideoCapture(0)
url = "http://localhost:8000/frames/"
table_id = 1
fps = 2  # sends 2 images per second

while True:
    ret, frame = camera.read()
    if not ret:
        break
    _, jpeg = cv2.imencode(".jpg", frame)
    requests.post(
        url,
        files={"frame": ("frame.jpg", jpeg.tobytes(), "image/jpeg")},
        data={"table_id": table_id}
    )
    time.sleep(1/fps)
