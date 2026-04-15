import cv2
import time


class GUI:
    def __init__(self, fps_smoothing=0.9, default_fps=30):
        self.prev_time = time.time()
        self.fps = default_fps
        self.fps_smoothing = fps_smoothing

    def update_fps(self):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        if dt > 0:
            current_fps = 1 / dt
            # Smooth FPS
            self.fps = self.fps_smoothing * self.fps + (1 - self.fps_smoothing) * current_fps
        self.prev_time = curr_time
        return self.fps

    def draw_fps(self, frame, position=(10,30), color=(255,255,255), scale=1.0, thickness=2):
        self.update_fps()
        text = f"FPS:{int(self.fps)}"
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)
        return frame
    
    def draw_watermark(self, frame, text="youtube.com/@playatanu", wh=(10,30), margin=10, color=(255,255,255), scale=0.6, thickness=1):
        cv2.putText(frame, text, (margin, wh[1] - margin), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)
        return frame