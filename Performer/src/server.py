import socket
import json
import time

broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
socket.socket(socket.AF_INET,socket.SOCK_STREAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.settimeout(0.2)


def estimate_pose():
    a = []
    i = -1
    while True:
        i+=1
        a.append(i)
        yield a


def capture_pose():
    estimated_pose = estimate_pose()
    while True:
        landmarks = next(estimated_pose)
        landmarks = json.dumps(landmarks).encode()
        broadcast_socket.sendto(landmarks, ('<broadcast>', 8080))
        print('Pose Updated!')
        time.sleep(1)

capture_pose()