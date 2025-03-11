import socket


class IpAddress:

    @classmethod
    def local(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = 'localhost'
        finally:
            s.close()
        return IP
