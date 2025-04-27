import gradio as gr
import cv2
import numpy as np
import tempfile

def track_video(video_path, algorithm_type):
    cap = cv2.VideoCapture(video_path)
    ret, first_frame = cap.read()

    if not ret:
        return None

    # 打开打标窗口
    # 缩小显示比例
    scale = 0.5
    resized = cv2.resize(first_frame, None, fx=scale, fy=scale)

    # 在缩小图上打标
    roi_resized = cv2.selectROI("在第一帧选择追踪目标（按 Enter 确认）", resized, fromCenter=False)
    cv2.destroyAllWindows()

    # 将 ROI 映射回原始尺寸
    x, y, w, h = roi_resized
    roi = (int(x / scale), int(y / scale), int(w / scale), int(h / scale))

    height, width = first_frame.shape[:2]
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None or fps < 1:
        fps = 30  # 默认30fps

    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    if algorithm_type == "CSRT追踪器":
        tracker = cv2.TrackerCSRT_create()
        tracker.init(first_frame, roi)
    elif algorithm_type == "KCF追踪器":
        tracker = cv2.TrackerKCF_create()
        tracker.init(first_frame, roi)
    elif algorithm_type == "MOSSE追踪器":
        tracker = cv2.legacy.TrackerMOSSE_create()
        tracker.init(first_frame, roi)
    else:
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if algorithm_type in ["CSRT追踪器", "KCF追踪器", "MOSSE追踪器"]:
            success, box = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Tracking failed", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        out.write(frame)

    cap.release()
    out.release()

    return output_path

def main():
    algorithm_options = [
        "CSRT追踪器", 
        "KCF追踪器", 
        "MOSSE追踪器"
    ]

    with gr.Blocks(
        title="视频处理与追踪应用",
        css="""html, body, .gradio-container {
            height: 100%;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #FF6347, #FF4500, #FFD700, #9ACD32, #00BFFF, #8A2BE2);
            background-size: 600% 600%;
            animation: gradientAnimation 10s ease infinite;
        }

        @keyframes gradientAnimation {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        """,
    ) as demo:
        gr.Markdown("## 🎯 视频处理与追踪应用")
        gr.Markdown("上传视频，选择算法（含目标追踪），打标后查看输出结果")

        with gr.Row():
            video_input = gr.Video(label="上传视频", height=480)

        with gr.Row():
            algorithm_type = gr.Dropdown(
                choices=algorithm_options,
                label="选择算法类型",
                value="CSRT追踪器"
            )
            process_btn = gr.Button("处理视频")

        with gr.Row():
            video_output = gr.Video(label="处理结果", height=480)

        def unified_process(video_path, algorithm_type):
            return track_video(video_path, algorithm_type)

        process_btn.click(
            fn=unified_process,
            inputs=[video_input, algorithm_type],
            outputs=video_output
        )

    demo.launch(share=True)


# 原有灰度/边缘/模糊处理函数保留
def process_video(video_path, algorithm_type):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None or fps < 1:
        fps = 30
    output_path = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if algorithm_type == "灰度转换":
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
        elif algorithm_type == "边缘检测":
            processed_frame = cv2.Canny(frame, 100, 200)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
        elif algorithm_type == "高斯模糊":
            processed_frame = cv2.GaussianBlur(frame, (15, 15), 0)
        else:
            processed_frame = frame
        out.write(processed_frame)

    cap.release()
    out.release()
    return output_path

if __name__ == "__main__":
    main()
