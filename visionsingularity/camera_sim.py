import cv2, requests, time

BACKEND = "http://localhost:8000/frames/"
TABLE_ID = 1            # change to the actual Table.id you want
FPS = 2                 # 2 frames per second

cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Cannot open webcam"

while True:
    ok, frame = cap.read()
    if not ok:
        print("Failed to capture"); break
    _, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    try:
        r = requests.post(
            BACKEND,
            files={"frame": ("f.jpg", buf.tobytes(), "image/jpeg")},
            data={"table_id": str(TABLE_ID)},
            timeout=2,
        )
        print(r.status_code, r.json())
    except Exception as e:
        print("POST error:", e)

    time.sleep(1/FPS)

