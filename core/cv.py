import cv2
import numpy as np
import mediapipe as mp
from collections import deque, defaultdict
from typing import Literal, Optional

mp_hands = mp.solutions.hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5,
)

# 1-second buffer (assuming ~2 fps)
history: dict[int, deque[tuple[float, float]]] = defaultdict(lambda: deque(maxlen=4))

Gesture = Optional[Literal["raise", "wave"]]

def detect_gesture(jpeg_bytes: bytes, table_id: int) -> Gesture:
    """Return 'raise', 'wave', or None for this frame."""
    img_array = np.frombuffer(jpeg_bytes, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if frame is None:
        return None                       # corrupt image

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = mp_hands.process(rgb)
    if not res.multi_hand_landmarks:
        return None

    # use the first detected hand
    hand = res.multi_hand_landmarks[0]
    wrist = hand.landmark[mp.solutions.hands.HandLandmark.WRIST]
    index_tip = hand.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

    # normalize 0-1 → pixel coords
    wrist_y = wrist.y * h
    index_y = index_tip.y * h
    index_x = index_tip.x * w

    # -------- Raise logic --------
    # “Hand raised” if index finger above 1/3 from top of image
    if index_y < h * 0.33:
        return "raise"

    # -------- Wave logic --------
    history[table_id].append((index_x, index_y))
    if len(history[table_id]) == history[table_id].maxlen:
        xs = [p[0] for p in history[table_id]]
        # simple heuristic: has x oscillated left ↔ right?
        if max(xs) - min(xs) > w * 0.25:
            history[table_id].clear()
            return "wave"

    return None
