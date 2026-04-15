from collections import deque
import numpy as np


class AngleSmoother:
    def __init__(self, window_size=5):
        self.window = deque(maxlen=window_size)

    def update(self, angle):
        self.window.append(angle)
        return np.mean(self.window)


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine))

    return angle