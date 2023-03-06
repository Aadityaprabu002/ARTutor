import time

import cv2
import mediapipe as mp
import socket
import json


class App:
    def __init__(self, port=8080, ip_address='<broadcast>'):
        self.video_capture = None
        self.mp_drawing = None
        self.mp_pose = None
        self.server_socket = None
        self.server_port = port
        self.server_ip_address = ip_address

    def setup_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_socket.settimeout(0.2)

    def setup_pose_estimator(self):
        self.video_capture = cv2.VideoCapture(0)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

    def capture_and_broadcast_pose(self):
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.video_capture.isOpened():
                ret, frame = self.video_capture.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = list(results.pose_landmarks.landmark)
                    keypoints = dict()
                    for pose_landmark in self.mp_pose.PoseLandmark:
                        extracted_pose_landmark = landmarks[pose_landmark.value]
                        keypoints[pose_landmark.name] = {
                                'x': extracted_pose_landmark.x,
                                'y': extracted_pose_landmark.y,
                                'z': extracted_pose_landmark.z,
                                'visibility': extracted_pose_landmark.visibility
                        }


                    print(keypoints)
                    keypoints = json.dumps(keypoints)
                    self.server_socket.sendto(keypoints.encode(), (self.server_ip_address, self.server_port))
                except:
                    print('Error in decoding landmarks or broadcasting landmarks!')
                    pass

                # Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                # Project image with pose landmark lines
                cv2.imshow('Feed', image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            self.video_capture.release()
            cv2.destroyAllWindows()

    def close_server(self):
        self.server_socket.close()
