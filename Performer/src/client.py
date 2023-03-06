import socket
import json
import time

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
receiver_socket.bind(('', 8080))

while True:
    print('Receiving...')
    data, addr = receiver_socket.recvfrom(1024 * 5)
    landmarks = data.decode()
    landmarks = json.loads(landmarks)
    print(f"Landmark is:{landmarks}")
    time.sleep(1)
