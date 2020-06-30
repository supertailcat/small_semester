#############################################################################################
#                                                                                           #
# 通过启动start_listen函数开始监听，在与客户端取得链接之后，发送两个字符串。客户端需要再转变一次格式  #
# python和Java的字符串长度没有限制，所以可以一次传递。                                           #
#                                                                                           #
#############################################################################################


import socket
import threading


# 向客户端发送csv文件和图片（字符串形式）
def send(client_socket, client_address, csv_filename, pic_filename):
    with open(csv_filename) as file:
        file_data = file.read()
    client_socket.sendall(file_data)
    with open(pic_filename) as file:
        file_data = file.read()
    client_socket.sendall(file_data)

    # BUFSIZE = 1024
    # print('Waiting for the connection：', client_address)
    # data = client_socket.recv(BUFSIZE).decode()
    # filename = data.split()[1]
    # filename = filename[1:]
    #
    # '''当网络质量差没有收到浏览器的访问数据时执行'''
    # if filename == "":
    #     client_socket.close()
    #     print("请输入要访问的文件")
    #
    # base_dir = os.getcwd()
    # file_dir = os.path.join(base_dir, filename)
    #
    # '''当访问的文件在本地服务器存在时执行'''
    # if os.path.exists(file_dir):
    #     f = open(file_dir, encoding='utf-8')
    #     SUCCESS_PAGE = "HTTP/1.1 200 OK\r\n\r\n" + f.read()
    #     print(SUCCESS_PAGE)
    #     client_socket.sendall(SUCCESS_PAGE.encode())
    #     client_socket.close()
    # else:
    #     FAIL_PAGE = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(base_dir, "fail.html"),
    #                                                        encoding="utf-8").read()
    #     print(FAIL_PAGE)
    #     client_socket.sendall(FAIL_PAGE.encode())
    #     client_socket.close()


# 外部调用本函数
def start_listen(ip, port, csv_filename, pic_filename):
    server_socket = socket.socket()
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print("waiting for connection......\n")
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=send, args=(client_socket, client_address, csv_filename, pic_filename))
        thread.start()
    # server_socket.close()


if __name__ == "__main__":
    print(socket.gethostbyname(socket.gethostname()))
    start_listen(socket.gethostbyname(socket.gethostname()), 8080, "*.csv", "*.png")
