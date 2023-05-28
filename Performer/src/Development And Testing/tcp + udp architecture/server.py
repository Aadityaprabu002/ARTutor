import socket


class Room:
    def __init__(self, in_ip_address, in_port, out_ip_address, out_port, out_ttl, buffer_size):
        self.in_address = (in_ip_address, in_port)
        self.out_address = (out_ip_address, out_port)

        self.in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.in_socket.bind(self.in_address)

        self.out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.out_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, out_ttl)

        self.buffer_size = buffer_size

    def listen(self):
        while True:
            performer_data, performer_address = self.in_socket.recvfrom(self.buffer_size)


class Server:
    def __init__(self, ):
        None
