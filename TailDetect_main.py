import cv2
import time
from BrakeDetecting import *
import numpy as np
from Thresholding import *
from PerspectiveTransformation import *
from LaneLines import *
from yolo_test import *
from ADAS_main import FindLaneLines

# 동영상 파일 열기
cap = cv2.VideoCapture('sample1.avi')

# 전체 루프 FPS 설정 (비디오의 FPS와 동일하게 설정)
video_fps = cap.get(cv2.CAP_PROP_FPS)
video_frame_interval = 1 / video_fps

# 브레이크등 분석을 위한 FPS 설정 (예: 0.2초 간격으로 분석)
brake_analysis_interval = 0.2  # 초 단위로 간격 설정

# 첫 번째 프레임 읽기
ret, prev_frame = cap.read()

# 브레이크등 분석을 위한 타이머 초기화
last_brake_analysis_time = time.time()

while ret:
    start_time = time.time()

    # 다음 프레임 읽기
    ret, current_frame = cap.read()
    if not ret:
        break

    # 전체 루프 내에서 차선 및 전방 차량 감지 수행
    findLaneLines = FindLaneLines()
    lane_img = findLaneLines.forward(current_frame)
    
    # # 브레이크등 분석 간격 확인
    # current_time = time.time()
    # if current_time - last_brake_analysis_time >= brake_analysis_interval:
    #     # 브레이크등 감지 수행 및 결과 표시
    #     brake_light_status = detect_brake_light(current_frame)
    #     cv2.putText(current_frame, f"Brake Light: {brake_light_status}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #     # 이전 프레임과 비교하여 브레이크등 상태 변화 감지
    #     if prev_frame is not None:
    #         prev_brake_light_status = detect_brake_light(prev_frame)
    #         if brake_light_status > prev_brake_light_status:
    #             cv2.putText(current_frame, "Brake Light ON", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    #         elif brake_light_status < prev_brake_light_status:
    #             cv2.putText(current_frame, "Brake Light OFF", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #     # 분석 타이머 갱신 및 이전 프레임 업데이트
    #     last_brake_analysis_time = current_time
    #     prev_frame = current_frame.copy()

    # # 결과를 화면에 표시
    # cv2.imshow('Frame', current_frame)

    # # 루프 실행 시간을 고려하여 전체 루프 FPS를 유지
    # elapsed_time = time.time() - start_time
    # if elapsed_time < video_frame_interval:
    #     time.sleep(video_frame_interval - elapsed_time)

    # ESC키를 누르면 루프 종료
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    
    result = cv2.addWeighted(lane_img, 0.5, current_frame, 0.5, 0)
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

    if cv2.waitKey(10) == 27:
        break

# 모든 작업이 끝난 후, 리소스 해제
cap.release()
cv2.destroyAllWindows()
