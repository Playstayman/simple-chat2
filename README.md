# Simple Chat 2

A simple Python-based chat application that allows users to communicate over a Local Area Network (LAN). The application consists of a server and a client, facilitating real-time messaging.

## Features

- **Real-Time Messaging**: Instant communication between users on the same network.
- **Easy Setup**: Simple to compile and run on any system with Python 3 installed.

## Prerequisites

Ensure you have Python 3 installed on your system. The application requires the following libraries, which are available in the Python Standard Library or can be installed via pip if needed:

- `socket`
- `threading`
- `time`
- `json`
- `requests`
- `ssl`
- `tkinter`
- `queue`

To install any missing libraries, you can run:

```bash
pip install libray_name
```

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Playstayman/simple-chat2.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd simple-chat2
    ```

### Compiling the Files

Before running the application, compile the two Python scripts:

1. **Compile the server script**:
    ```bash
    python -m compileall srvr.py
    ```
2. **Compile the client script**:
    ```bash
    python -m compileall try_both.py
    ```

### Running the Application

1. **Start the Server**:
    - Run the server script first. The server will display the IP address that clients can use to connect:
    ```bash
    python srvr.py
    ```

2. **Connect with the Client**:
    - After the server is running, use the client script to connect to the server's IP address. This will allow users to communicate through the chat app:
    ```bash
    python try_both.py
    ```

### How It Works

- **Server (`srvr.py`)**: 
  - The server listens for incoming connections and facilitates communication between clients. When you run the server, it displays the IP address for clients to connect to.
  
- **Client (`try_both.py`)**:
  - The client connects to the server using the IP address provided by the server. Once connected, users can send and receive messages through a graphical user interface (GUI) created with `tkinter`.
