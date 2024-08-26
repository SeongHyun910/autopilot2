"""
ADAS projects by Autopilot

Functions :
    Lane Detection
    Object Detection by Yolo
    ...
"""

import numpy as np
import cv2
from Thresholding import *
from PerspectiveTransformation import *
from LaneLines import *
from Yolo_v8 import *
import time
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def check_time(start_time, end_time):
    """
        time = time.perf_counter_ns()
    """
    frame_time_ns = end_time - start_time
    frame_time_ms = frame_time_ns / 1_000_000
    return frame_time_ms

class FindLaneLines :
    def __init__(self):
        """ Init Application """
        self.thresholding = Thresholding()
        self.transform = PerspectiveTransformation()
        self.lanelines = LaneLines()

    def forward(self, img):
        out_img = np.copy(img)
        # print(f"out_img: {out_img}")
        cv2.imshow("out_img",out_img)
        time1 = time.perf_counter_ns()
        img = self.transform.forward(img)
        cv2.imshow("self.transform.forward(img)", img)
        # print(f"self.transform.forward(img): {self.transform.forward(img)}")
        time2 = time.perf_counter_ns()
        img = self.thresholding.forward(img)
        # print(f"self.thresholding.forward(img):{self.thresholding.forward(img).shape}")
        time3 = time.perf_counter_ns()
        img = self.lanelines.forward(img)
        time4 = time.perf_counter_ns()
        img = self.transform.backward(img)
        time5 = time.perf_counter_ns()
        out_img = cv2.addWeighted(out_img, 1, img, 0.6, 0)
        # print(f"time1: {check_time(time1, time2)}ms, time2: {check_time(time2, time3)}ms, time3: {check_time(time3, time4)}ms, time4: {check_time(time4, time5)}ms")
        return out_img

    def process_image(self, img_path):
        cap = cv2.VideoCapture(img_path)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        if not cap.isOpened():
            print(f"Error: Failed to open video from {'sample1.avi'}")
            exit(1)

        yolo = YOLOv8CarDetector('yolov8n.pt')
        while cap.isOpened():
            ret, frame = cap.read()
            # 프레임 시작 시간 기록
            start_time = time.perf_counter_ns()
            frame = cv2.resize(frame, (640, 360))
            if not ret:
                print("--------Video Ended---------")
                break
            lane_img = np.copy(frame)
            time1 = time.perf_counter_ns()
            """ -------Yolo process------- """
            yolo_img = yolo.detect_and_draw(frame)
            """ --------------------------- """
            time2 = time.perf_counter_ns()
            lane_img = self.forward(lane_img)
            time3 = time.perf_counter_ns()
            result = cv2.addWeighted(lane_img, 0.5, yolo_img, 0.5, 0)
            # 프레임 종료 시간 기록
            end_time = time.perf_counter_ns()
            # 프레임 당 소요 시간 계산
            frame_time_ns = end_time - start_time
            frame_time_ms = frame_time_ns / 1_000_000
            # 프레임 시간 출력
            # print(f"Frame time: {frame_time_ms:.2f} ms")
            cv2.putText(result, f"Frame time: {frame_time_ms:.2f} ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 255, 255), 2)
            cv2.imshow("result", result)
            print(f"time1: {check_time(time1, time2)}ms, time2: {check_time(time2, time3)}ms")
            if cv2.waitKey(10) == 27:
                break

def main():
    img_path = "sample1.avi"

    findLaneLines = FindLaneLines()
    findLaneLines.process_image(img_path)

if __name__ == "__main__":
    main()