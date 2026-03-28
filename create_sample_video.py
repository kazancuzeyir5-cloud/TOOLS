import cv2
import numpy as np
import math

output_path = "sample_video.mp4"
width, height = 640, 480
fps = 30
duration = 5  # seconds
total_frames = fps * duration

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

for frame_num in range(total_frames):
    t = frame_num / fps  # time in seconds
    progress = frame_num / total_frames

    # Animated gradient background
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            r = int((math.sin(t + x / 100) * 0.5 + 0.5) * 200)
            g = int((math.sin(t + y / 100 + 2) * 0.5 + 0.5) * 150)
            b = int((math.cos(t + (x + y) / 150) * 0.5 + 0.5) * 255)
            frame[y, x] = [b, g, r]

    # Bouncing circle
    cx = int(width / 2 + math.sin(t * 2) * 150)
    cy = int(height / 2 + math.cos(t * 2) * 100)
    cv2.circle(frame, (cx, cy), 40, (255, 255, 255), -1)
    cv2.circle(frame, (cx, cy), 40, (0, 0, 0), 2)

    # Rotating star / polygon
    num_points = 6
    radius = 30
    star_cx, star_cy = 80, 80
    angle_offset = t * 2
    pts = []
    for i in range(num_points):
        angle = angle_offset + i * (2 * math.pi / num_points)
        px = int(star_cx + radius * math.cos(angle))
        py = int(star_cy + radius * math.sin(angle))
        pts.append([px, py])
    pts = np.array(pts, np.int32).reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], True, (0, 255, 255), 3)
    cv2.fillPoly(frame, [pts], (0, 200, 200))

    # Progress bar
    bar_width = int(progress * (width - 40))
    cv2.rectangle(frame, (20, height - 30), (width - 20, height - 10), (50, 50, 50), -1)
    cv2.rectangle(frame, (20, height - 30), (20 + bar_width, height - 10), (0, 200, 100), -1)

    # Title text
    cv2.putText(frame, "Sample Video - Claude Code", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    # Timer
    cv2.putText(frame, f"{t:.1f}s / {duration}s", (width - 120, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (220, 220, 220), 1, cv2.LINE_AA)

    out.write(frame)
    if frame_num % 30 == 0:
        print(f"Rendering... {frame_num}/{total_frames} frames ({int(progress*100)}%)")

out.release()
print(f"\nVideo saved: {output_path}")
print(f"Resolution: {width}x{height} | FPS: {fps} | Duration: {duration}s")
