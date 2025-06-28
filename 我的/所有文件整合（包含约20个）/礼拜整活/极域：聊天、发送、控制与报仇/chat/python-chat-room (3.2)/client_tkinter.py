import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, filedialog
import os
import time

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("聊天室客户端")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # 设置字体
        self.font = ('SimHei', 10)

        # 连接服务器
        self.server_ip = simpledialog.askstring("服务器连接", "请输入服务器IP地址:", parent=self.root)
        if not self.server_ip:
            self.root.destroy()
            return

        self.chat_port = 9999
        self.file_port = 9998
        self.nickname = simpledialog.askstring("用户信息", "请输入你的昵称:", parent=self.root)
        if not self.nickname:
            self.nickname = "匿名用户"

        # 创建聊天socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server_ip, self.chat_port))
            self.client.send(self.nickname.encode('utf-8'))
        except Exception as e:
            messagebox.showerror("连接错误", f"无法连接到服务器: {e}")
            self.root.destroy()
            return

        # 创建UI
        self.create_widgets()

        # 启动接收消息线程
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 聊天历史显示区域
        self.chat_history = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=self.font)
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_history.config(state=tk.DISABLED)

        # 分隔线
        separator = tk.Frame(main_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)

        # 底部功能区
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        # 文件传输按钮
        self.file_button = tk.Button(bottom_frame, text="发送文件", font=self.font, command=self.send_file)
        self.file_button.pack(side=tk.LEFT, padx=5)

        # 输入区域
        input_frame = tk.Frame(bottom_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.message_entry = tk.Entry(input_frame, font=self.font)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.message_entry.focus_set()
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(input_frame, text="发送", font=self.font, command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message.startswith('FILE:'):
                    # 文件传输通知
                    parts = message.split(':', 3)
                    sender = parts[1]
                    filename = parts[2]
                    filesize = parts[3]

                    # 询问用户是否接收文件
                    answer = messagebox.askyesno("文件传输",
                                                 f"用户 {sender} 想要发送文件: {filename}\n大小: {self.format_size(int(filesize))}\n是否接收?")
                    if answer:
                        # 选择保存位置
                        save_path = filedialog.asksaveasfilename(initialfile=filename, defaultextension="*.*")
                        if save_path:
                            threading.Thread(target=self.receive_file, args=(save_path,)).start()
                elif message.startswith('FILE_DISTRIBUTION:'):
                    # 处理服务器分发的文件
                    parts = message.split(':', 4)
                    filename = parts[1]
                    filesize = int(parts[2])
                    file_port = int(parts[3])

                    # 询问用户是否接收文件
                    answer = messagebox.askyesno("文件分发",
                                                 f"服务器想要分发文件: {filename}\n大小: {self.format_size(filesize)}\n是否接收?")
                    if answer:
                        # 选择保存位置
                        save_path = filedialog.asksaveasfilename(initialfile=os.path.basename(filename), defaultextension="*.*")
                        if save_path:
                            threading.Thread(target=self.receive_distributed_file, args=(save_path, file_port)).start()
                else:
                    # 普通消息
                    self.update_chat_history(message)
            except Exception as e:
                print(f"接收消息错误: {e}")
                self.client.close()
                self.update_chat_history("与服务器的连接已断开")
                break

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client.send(f'{self.nickname}: {message}'.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.update_chat_history(f"发送消息失败: {e}")

    def send_file(self):
        # 选择文件
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)

        # 通知所有用户有文件传输
        self.client.send(f'FILE:{self.nickname}:{filename}:{filesize}'.encode('utf-8'))

        # 等待一段时间让其他用户准备好
        time.sleep(1)

        # 发送文件
        threading.Thread(target=self.transfer_file, args=(file_path,)).start()

    def transfer_file(self, file_path):
        try:
            filename = os.path.basename(file_path)
            filesize = os.path.getsize(file_path)

            # 创建新的文件传输socket，不使用共享的socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_ip, self.file_port))

            # 发送文件名
            s.send(filename.encode('utf-8'))
            response = s.recv(1024)
            if response != b'OK':
                self.update_chat_history("文件传输失败: 服务器拒绝接收文件名")
                s.close()
                return

            # 发送文件大小
            s.send(str(filesize).encode('utf-8'))
            response = s.recv(1024)
            if response != b'OK':
                self.update_chat_history("文件传输失败: 服务器拒绝接收文件大小")
                s.close()
                return

            # 发送文件内容
            with open(file_path, 'rb') as f:
                bytes_sent = 0
                while bytes_sent < filesize:
                    data = f.read(1024)
                    if not data:
                        break
                    s.send(data)
                    bytes_sent += len(data)

            self.update_chat_history(f"文件 {filename} 发送完成")
            s.close()
        except Exception as e:
            self.update_chat_history(f"文件传输错误: {e}")

    def receive_file(self, save_path):
        try:
            # 创建新的socket用于接收文件
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_ip, self.file_port))

            filename = os.path.basename(save_path)

            # 接收文件名
            server_filename = s.recv(1024).decode('utf-8')
            s.send(b'OK')

            # 接收文件大小
            filesize = int(s.recv(1024).decode('utf-8'))
            s.send(b'OK')

            # 接收文件内容
            with open(save_path, 'wb') as f:
                bytes_received = 0
                while bytes_received < filesize:
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)

            self.update_chat_history(f"文件 {filename} 接收完成，已保存至: {save_path}")
            s.close()
        except Exception as e:
            self.update_chat_history(f"接收文件错误: {e}")

    def receive_distributed_file(self, save_path, file_port):
        try:
            # 创建新的socket用于接收分发的文件
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_ip, file_port))

            filename = os.path.basename(save_path)

            # 接收文件名
            server_filename = s.recv(1024).decode('utf-8')
            s.send(b'OK')

            # 接收文件大小
            filesize = int(s.recv(1024).decode('utf-8'))
            s.send(b'OK')

            # 接收文件内容
            with open(save_path, 'wb') as f:
                bytes_received = 0
                while bytes_received < filesize:
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)

            self.update_chat_history(f"文件 {filename} 分发接收完成，已保存至: {save_path}")
            s.close()
        except Exception as e:
            self.update_chat_history(f"接收分发文件错误: {e}")

    def format_size(self, size_bytes):
        """将字节数转换为人类可读的格式"""
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        while size_bytes >= 1024 and unit_index < len(units) - 1:
            size_bytes /= 1024
            unit_index += 1
        return f"{size_bytes:.2f} {units[unit_index]}"

    def update_chat_history(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)

    def on_closing(self):
        if messagebox.askyesno("退出", "确定要退出聊天室吗?"):
            try:
                self.client.send(f'SYSTEM: {self.nickname} 离开了聊天室'.encode('utf-8'))
                self.client.close()
            except:
                pass
            self.root.destroy()


if __name__ == "__main__":
    print("开发：豆包 调试：汪子翔 改进：曾一格/滕泽同")
    print("此程序为稳定版本 v3.2")
    print("@整活三缺一 请勿二次分发！")
    print("\n")
    root = tk.Tk()
    # 确保中文显示正常
    try:
        root.option_add("*Font", "SimHei 10")
    except:
        pass
    app = ChatClient(root)
    root.mainloop()
