import socket
import os
import json
import time

print('listening...')
ip_addr = ("172.31.13.198", 3000)

server = socket.socket()
server.bind(ip_addr)
server.listen(5)

while True:
    try:
        conn, addr = server.accept()
        file_msg = conn.recv(2048)

        msg_data = json.loads(file_msg.decode('utf-8'))

        if msg_data.get("action") == "put":
            file_name = msg_data.get("name")
            file_size = msg_data.get("size")
            recv_size = 0
            with open(file_name, "wb") as f:
                while recv_size != file_size:
                    data = conn.recv(2048)
                    f.write(data)
                    recv_size += len(data)
                    print("file size: %s sent size: %s" % (file_size, recv_size))
                print("file %s transferred successfully..." % file_size)
            bool = 0
            break
    except:
        pass
