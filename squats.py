import cv2
import numpy as np
import onnxruntime as ort
import argparse

from utils.keypoints import draw_left_skeleton, draw_right_skeleton

from utils.gui import GUI
from utils.progress_bar import angle_to_progress, draw_progress_bar
from utils.squat_counter import SquatCounter
from utils.angle import AngleSmoother, calculate_angle


def main(video_path, model_path, output_path):
    session = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"]
    )
    
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    def preprocess(image, input_size=192):
        img = cv2.resize(image, (input_size, input_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)  # (1, H, W, 3)
        img = np.transpose(img, (0, 3, 1, 2))  # NHWC to NCHW
        
        return img

    def infer(image):
        input_tensor = preprocess(image)
        outputs = session.run([output_name], {input_name: input_tensor})
        return outputs[0]
    
    
    cap = cv2.VideoCapture(video_path)
    gui = GUI(fps_smoothing=0.9)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
    scounter = SquatCounter()
    knee_angle_smoother = AngleSmoother(window_size=10)
    
    while True:
        ret, frame = cap.read()
        h, w, _ = frame.shape
        if not ret:
            break

        keypoints = infer(frame)
        
        hip, knee, ankle, hc, kc, ac = scounter.get_right_leg_points(keypoints, w, h)
        
        # confidence check
        if hc > 0.3 and kc > 0.3 and ac > 0.3:
            raw_knee_angle = calculate_angle(hip, knee, ankle)
            knee_angle = knee_angle_smoother.update(raw_knee_angle)
            count, stage = scounter.update(knee_angle)
            
            progress = angle_to_progress(knee_angle)
            draw_progress_bar(frame, progress)

        frame = draw_left_skeleton(frame, keypoints, threshold=0.25)

        kx, ky = int(knee[0]), int(knee[1])
        cv2.putText(frame,f"{int(knee_angle)} degrees", (kx + 20, ky), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        sx1, sy1 = w - 250, h - 50
        cv2.putText(frame, f"squats: {count}", (sx1, sy1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

        gui.draw_fps(frame, position=(10, 30))
        gui.draw_watermark(frame, "youtube.com/@playatanu", wh=(w,h), margin=10)
        
        cv2.imshow("MoveNet Pose", frame)
        
        if output_path:
            out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a video with MoveNet model")
    parser.add_argument(
        "--video_path",
        "-v",
        type=str,
        default="videos/example.mp4",
        help="Path to the input video file"
    )
    parser.add_argument(
        "--model_path",
        "-m",
        type=str,
        default="model/movenet.onnx",
        help="Path to the ONNX model file"
    )

    parser.add_argument(
        "--output_path",
        "-o",
        type=str,
        default="videos/output.mp4",
        help="Path to save the output video file"
    )
    
    args = parser.parse_args()
    main(args.video_path, args.model_path, args.output_path)