import socket
import threading
import queue
import json

q = queue.Queue(maxsize=100)


def fun():
    global q
    l = ''
    while True:
        while not q.empty():
            chunk = q.get()
            if chunk == 'START':
                l = ''
            elif chunk == 'END':
                try:
                    j = json.loads(l)
                    print(j['2']['x'])
                except:
                    print('Couldnt  parse')
            else:
                l += chunk


receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
receiver_socket.bind(('', 8080))
landmarks = ''

t = threading.Thread(target=fun)
t.start()
while True:
    chunk, addr = receiver_socket.recvfrom(1024 * 5)
    payload = chunk.decode()
    q.put(payload)
