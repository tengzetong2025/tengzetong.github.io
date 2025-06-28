import socket
import threading
import os

# 获取本地IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return '127.0.0.1'

# 服务器配置
HOST = get_local_ip()
PORT = 9999
FILE_PORT = 9998
print("开发：豆包 调试：汪子翔 改进：曾一格/腾泽同")
print("此程序为稳定版本 v3.3")
print("@整活三缺一 请勿二次分发！")
print("\n")
print(f"服务器IP地址: {HOST}")
print(f"聊天端口: {PORT}")
print(f"文件传输端口: {FILE_PORT}")

# 创建聊天socket
chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server.bind((HOST, PORT))
chat_server.listen()

# 创建文件传输socket
file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file_server.bind((HOST, FILE_PORT))
file_server.listen()

# 存储客户端和对应的昵称
clients = []
nicknames = []

# 广播消息给所有客户端
def broadcast(message):
    for client in clients:
        client.send(message)

# 处理客户端连接
def handle(client):
    while True:
        try:
            # 接收客户端消息
            message = client.recv(1024)
            if message.startswith(b'FILE:'):
                # 文件传输通知
                broadcast(message)
            else:
                # 普通消息
                broadcast(message)
        except:
            # 处理客户端断开连接的情况
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'SYSTEM: {nickname} 离开了聊天室'.encode('utf-8'))
            break

# 接收客户端连接
def receive():
    while True:
        client, address = chat_server.accept()
        print(f'聊天连接地址: {str(address)}')

        # 获取客户端昵称
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'用户 {nickname} 已连接!')
        broadcast(f'SYSTEM: {nickname} 加入了聊天室'.encode('utf-8'))
        client.send('连接成功!'.encode('utf-8'))

        # 为每个客户端创建一个线程来处理消息
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# 处理文件接收
def handle_file_receive(conn, addr):
    print(f'文件传输连接地址: {str(addr)}')

    try:
        # 接收文件名
        filename = conn.recv(1024).decode('utf-8')
        conn.send(b'OK')

        # 接收文件大小
        filesize = int(conn.recv(1024).decode('utf-8'))
        conn.send(b'OK')

        # 生成唯一的文件名，避免覆盖
        unique_filename = filename
        counter = 1
        while os.path.exists(unique_filename):
            name, ext = os.path.splitext(filename)
            unique_filename = f"{name}_{counter}{ext}"
            counter += 1

        # 接收文件内容
        with open(unique_filename, 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)

        print(f'文件 {unique_filename} 接收完成')
        
        # 在新线程中分发文件，不阻塞当前线程
        threading.Thread(target=distribute_file, args=(unique_filename, filesize)).start()
    except Exception as e:
        print(f"接收文件错误: {e}")
    finally:
        conn.close()

# 处理文件传输
def handle_file_transfer():
    while True:
        conn, addr = file_server.accept()
        # 为每个文件传输创建新线程
        thread = threading.Thread(target=handle_file_receive, args=(conn, addr))
        thread.start()

# 分发文件给所有客户端
def distribute_file(filename, filesize):
    for client in clients.copy():  # 使用副本避免迭代时修改列表
        try:
            # 创建新的文件传输socket
            file_distribution_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            file_distribution_socket.bind(('0.0.0.0', 0))  # 自动选择一个可用端口
            file_distribution_port = file_distribution_socket.getsockname()[1]
            client.send(f'FILE_DISTRIBUTION:{filename}:{filesize}:{file_distribution_port}'.encode('utf-8'))
            file_distribution_socket.listen(1)

            # 等待客户端连接
            conn, addr = file_distribution_socket.accept()

            # 发送文件名
            conn.send(os.path.basename(filename).encode('utf-8'))
            response = conn.recv(1024)
            if response != b'OK':
                print("文件分发失败: 客户端拒绝接收文件名")
                conn.close()
                continue

            # 发送文件大小
            conn.send(str(filesize).encode('utf-8'))
            response = conn.recv(1024)
            if response != b'OK':
                print("文件分发失败: 客户端拒绝接收文件大小")
                conn.close()
                continue

            # 发送文件内容
            with open(filename, 'rb') as f:
                bytes_sent = 0
                while bytes_sent < filesize:
                    data = f.read(1024)
                    if not data:
                        break
                    conn.send(data)
                    bytes_sent += len(data)

            print(f'文件 {filename} 已分发给客户端 {addr}')
            conn.close()
        except Exception as e:
            print(f"文件分发错误: {e}")

# 启动聊天和文件传输线程
print("服务器正在监听...")
chat_thread = threading.Thread(target=receive)
chat_thread.start()

file_thread = threading.Thread(target=handle_file_transfer)
file_thread.start()
