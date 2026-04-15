import cv2

EDGES = [
    (0,1),(0,2),(1,3),(2,4),
    (0,5),(0,6),(5,7),(7,9),
    (6,8),(8,10),(5,6),
    (5,11),(6,12),(11,12),
    (11,13),(13,15),(12,14),(14,16)
]

def draw_keypoints(image, keypoints, threshold=0.3):
    img = image.copy()
    h, w, _ = img.shape

    for kp in keypoints[0][0]:
        y, x, conf = kp
        if conf > threshold:
            cx, cy = int(x * w), int(y * h)
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)

    return img

def draw_skeleton(image, keypoints, threshold=0.3):
    img = draw_keypoints(image, keypoints, threshold)
    h, w, _ = image.shape

    for (p1, p2) in EDGES:
        y1, x1, c1 = keypoints[0][0][p1]
        y2, x2, c2 = keypoints[0][0][p2]

        if c1 > threshold and c2 > threshold:
            pt1 = (int(x1*w), int(y1*h))
            pt2 = (int(x2*w), int(y2*h))

            cv2.line(img, pt1, pt2, (255, 255, 255), 2)

    return img


RIGHT_EDGES = [
    (6, 8),    # shoulder → elbow
    (8, 10),   # elbow → wrist
    (6, 12),   # shoulder → hip
    (12, 14),  # hip → knee
    (14, 16)   # knee → foot
]

RIGHT_KP = [6, 8, 10, 12, 14, 16]


def draw_right_keypoints(image, keypoints, threshold=0.3):
    img = image.copy()
    h, w, _ = img.shape

    for idx in RIGHT_KP:
        y, x, conf = keypoints[0][0][idx]

        if conf > threshold:
            cx, cy = int(x * w), int(y * h)
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)

    return img

def draw_right_skeleton(image, keypoints, threshold=0.3):
    img = draw_right_keypoints(image, keypoints, threshold)
    h, w, _ = img.shape

    for (p1, p2) in RIGHT_EDGES:
        y1, x1, c1 = keypoints[0][0][p1]
        y2, x2, c2 = keypoints[0][0][p2]

        if c1 > threshold and c2 > threshold:
            pt1 = (int(x1 * w), int(y1 * h))
            pt2 = (int(x2 * w), int(y2 * h))

            cv2.line(img, pt1, pt2, (255, 255, 255), 2)

    return img


LEFT_EDGES = [
    (5, 7),    # shoulder → elbow
    (7, 9),    # elbow → wrist
    (5, 11),   # shoulder → hip
    (11, 13),  # hip → knee
    (13, 15)   # knee → foot
]

LEFT_KP = [5, 7, 9, 11, 13, 15]


def draw_left_keypoints(image, keypoints, threshold=0.3):
    img = image.copy()
    h, w, _ = img.shape

    for idx in LEFT_KP:
        y, x, conf = keypoints[0][0][idx]

        if conf > threshold:
            cx, cy = int(x * w), int(y * h)
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), -1)
            cv2.circle(img, (cx, cy), 5, (255, 255, 255), -1, 2)

    return img


def draw_left_skeleton(image, keypoints, threshold=0.3):
    img = image.copy()
    h, w, _ = img.shape

    for (p1, p2) in LEFT_EDGES:
        y1, x1, c1 = keypoints[0][0][p1]
        y2, x2, c2 = keypoints[0][0][p2]

        if c1 > threshold and c2 > threshold:
            pt1 = (int(x1 * w), int(y1 * h))
            pt2 = (int(x2 * w), int(y2 * h))

            cv2.line(img, pt1, pt2, (255, 255, 255), 2)

    img = draw_left_keypoints(img, keypoints, threshold)

    return img