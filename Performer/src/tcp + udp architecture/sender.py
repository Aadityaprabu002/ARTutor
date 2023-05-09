import socket


def main():
    MCAST_GRP = '224.1.1.1'
    MCAST_PORT = 5007

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    per_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    per_sock.bind(('127.0.0.1', 10000))

    while True:
        data, addr = per_sock.recvfrom(1024 * 5)
        print(data.decode()[:10])
        sock.sendto(data, (MCAST_GRP, MCAST_PORT))


if __name__ == '__main__':
    main()
