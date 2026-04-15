import cv2

def angle_to_progress(angle, min_angle=80, max_angle=170):
    # clamp
    angle = max(min(angle, max_angle), min_angle)

    # invert (because lower angle = deeper squat)
    progress = (max_angle - angle) / (max_angle - min_angle)

    return int(progress * 100)

def draw_progress_bar(image, progress):
    h, w, _ = image.shape

    # bar position
    x1, y1 = w - 60, 50
    x2, y2 = w - 30, h - 50

    # background
    cv2.rectangle(image, (x1, y1), (x2, y2), (255,255,255), 2)

    # filled height
    fill_height = int((y2 - y1) * (progress / 100))

    # fill (bottom to up)
    cv2.rectangle(image, (x1, y2 - fill_height), (x2, y2),(0,0,255), -1)

    # text
    cv2.putText(image, f"{progress}%", (x2 - 25, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)

    return image