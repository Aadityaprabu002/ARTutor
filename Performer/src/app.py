import time

import cv2
import mediapipe as mp
import json
import websockets
import asyncio


class App:
    def __init__(self, port=8080, ip_address='127.0.0.1'):
        self.video_capture = None
        self.mp_drawing = None
        self.mp_pose = None
        self.server_port = port
        self.server_ip_address = ip_address

    def __setup_pose_estimator(self):
        self.video_capture = cv2.VideoCapture(0)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        print('Pose Estimator setup Finished')

    async def __capture_and_transmit_pose(self, client_websocket):
        print('Capture Started')

        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            self.__is_capturing = True
            i = 0
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
                    landmarks = results.pose_landmarks.landmark
                    keypoints = dict()
                    for pose_landmark in self.mp_pose.PoseLandmark:
                        extracted_pose_landmark = landmarks[pose_landmark.value]
                        if pose_landmark.value in [23, 24]:
                            keypoints[pose_landmark.value] = {
                                'x': extracted_pose_landmark.x,
                                'y': extracted_pose_landmark.y,
                                'z': extracted_pose_landmark.z,
                                # 'visibility': extracted_pose_landmark.visibility
                            }
                        else:
                            keypoints[pose_landmark.value] = {
                                'x': extracted_pose_landmark.x,
                                'y': extracted_pose_landmark.y,
                                # 'z': extracted_pose_landmark.z,
                                # 'visibility': extracted_pose_landmark.visibility
                            }

                    keypoints = json.dumps(keypoints)
                    print(keypoints)
                    chunk_index = 0
                    chunk_size = len(keypoints) // 1
                    try:
                        while chunk_index < len(keypoints):
                            await client_websocket.send(
                                keypoints[
                                chunk_index:(chunk_index + chunk_size + 1)
                                ].encode()
                            )
                            chunk_index += chunk_size

                    except Exception as e:
                        print('Failed to send key points to server')
                        print(f'Error: {str(e)}')
                        pass

                except Exception as e:
                    print('Error with open cv')
                    print(f'Error: {e}')
                    pass

                # Render detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                # Project image with pose landmark lines
                cv2.imshow('Camera Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    self.__is_capturing = False
                    self.__is_running = False
                    break

        print('Capture Ended')

    async def __connect_server(self):
        server_websocket_url = f'ws://{self.server_ip_address}:{self.server_port}'

        try:
            async with websockets.connect(server_websocket_url) as client_websocket:
                print(f'Connected to WebSocket server at {server_websocket_url}')
                await self.__capture_and_transmit_pose(client_websocket)


        except Exception as e:
            print(f'Failed to connect to WebSocket server at {server_websocket_url}')
            print(f'Error: {e}')

    def setup(self):
        print('Setup Started')
        self.__setup_pose_estimator()
        print('Setup Finished')

    def start(self):
        print('App Started')
        asyncio.get_event_loop().run_until_complete(self.__connect_server())

    def stop(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
        print('App Ended')
