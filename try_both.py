import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
import queue
import json


class ChatApp:
    def __init__(self, master):
        self.nickname = "whatever"
        self.master = master
        self.master.title("Private room")
        self.stop_event = threading.Event()
        self.chat_history = scrolledtext.ScrolledText(master, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_history.pack(expand=True, fill=tk.BOTH)

        self.input_field = tk.Entry(master)
        self.input_field.pack(expand=True, fill=tk.X)
        self.input_field.bind("<Return>", self.send_message_enter)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        self.send_message_func = None

        self.message_queue = queue.Queue()

        self.master.after(100, self.update_chat)

        self.master.protocol("WM_DELETE_WINDOW", self.exit_app)

    def exit_app(self):
        self.stop_event.set()
        self.schedule_heartbeat(1)
        self.send_message(message=" ", is_down=True)
        self.master.destroy()

        print("done")

    def schedule_heartbeat(self, interval_ms=5000):
        if True:
            self.send_message(is_heartbeat=True, message=" ")
            self.master.after(interval_ms, self.schedule_heartbeat)

    def send_message(self, is_heartbeat=False, message=None, is_down=None):
        if not message:
            message = self.input_field.get()
        if message:
            if is_heartbeat:
                message = "[HEARTBEAT] " + message
            elif is_down:
                message = "[DOWN] " + message
            else:
                self.chat_history.configure(state=tk.NORMAL)
                self.chat_history.insert(tk.END, f"You: {message}\n")
                self.chat_history.configure(state=tk.DISABLED)
                self.input_field.delete(0, tk.END)
                message_data = {"username": self.nickname, "message": message}
                message = json.dumps(message_data)
            self.send_message_func(message)

    def send_message_enter(self, event):
        self.send_message()

    def update_chat(self):
        while not self.message_queue.empty():
            user, message = self.message_queue.get()
            self.chat_history.configure(state=tk.NORMAL)
            self.chat_history.insert(tk.END, f"{user}: {message}\n")
            self.chat_history.configure(state=tk.DISABLED)

        self.master.after(100, self.update_chat)


def receive_messages(client_socket, chat_app):
    while not chat_app.stop_event.is_set():
        try:
            print("got something")
            message = client_socket.recv(1024).decode('utf-8')
            data_package = json.loads(message)
            chat_app.message_queue.put((data_package["username"], data_package["message"]))
        except (OSError, ConnectionResetError, json.decoder.JSONDecodeError):
            break


def main():
    root = tk.Tk()
    chat_app = ChatApp(root)
    chat_app.send_message_func = lambda message: client_socket.send(message.encode('utf-8'))
    root.geometry("400x800")
    chat_app.nickname = simpledialog.askstring("your username", "Enter your nick")
    server_ip = simpledialog.askstring("Server IP", "Enter the server IP address:")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5555))
    chat_app.schedule_heartbeat()
    receive_threat = threading.Thread(target=receive_messages, args=(client_socket, chat_app))
    receive_threat.start()
    root.mainloop()
    receive_threat.join()


# NIIIIICE


if __name__ == "__main__":
    main()
