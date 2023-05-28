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
                # Render detections

                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                cv2.imshow('Camera Feed', image)

                try:
                    normalized_pose_landmarks = results.pose_landmarks.landmark
                    keypoints = dict()
                    for pose_landmark in self.mp_pose.PoseLandmark:
                        extracted_pose_landmark = normalized_pose_landmarks[pose_landmark.value]
                        unity_x = (extracted_pose_landmark.x - 0.5) * 2
                        unity_y = (extracted_pose_landmark.y - 0.5) * -2
                        unity_z = extracted_pose_landmark.z

                        keypoints[pose_landmark.value] = {
                            'x': unity_x,
                            'y': unity_y,
                            'z': unity_z
                        }

                    print(keypoints)

                    keypoints = json.dumps(keypoints)
                    max_payload_size = len(keypoints) // 2

                    self.server_socket.sendto("START".encode(), (self.server_ip_address, self.server_port))

                    self.server_socket.sendto(keypoints[:max_payload_size].encode(),
                                              (self.server_ip_address, self.server_port))
                    self.server_socket.sendto(keypoints[max_payload_size:].encode(),
                                              (self.server_ip_address, self.server_port))
                    self.server_socket.sendto("END".encode(), (self.server_ip_address, self.server_port))



                except:
                    print('Error in decoding landmarks or broadcasting landmarks!')
                    pass

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            self.video_capture.release()
            cv2.destroyAllWindows()

    def close_server(self):
        self.server_socket.close()
