#############################################################################################
#                                                                                           #
# 通过启动start_listen函数开始监听，在与客户端取得链接之后，发送两个字符串。客户端需要再转变一次格式  #
# python和Java的字符串长度没有限制，所以可以一次传递。                                           #
#                                                                                           #
#############################################################################################


import socket
import threading


# 向客户端发送csv文件和图片（字符串形式）
def send(client_socket, client_address, json_filename, pic_filename):
    with open(json_filename) as file:
        file_data = file.read()
    client_socket.sendall(file_data)
    with open(pic_filename) as file:
        file_data = file.read()
    client_socket.sendall(file_data)


# 外部调用本函数
def start_listen(ip, port, json_filename, pic_filename):
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print("waiting for connection......\n")
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=send, args=(client_socket, client_address, json_filename, pic_filename))
        thread.start()
    # server_socket.close()


if __name__ == "__main__":
    print(socket.gethostbyname(socket.gethostname()))
    start_listen(socket.gethostbyname(socket.gethostname()), 8080, "*.json", "*.png")
