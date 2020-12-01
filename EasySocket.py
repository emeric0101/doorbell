import pickle
import socket
import struct
import threading


class EasySocketServer(threading.Thread):

    def __init__(self, local_ip, port, action_data_received):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected_clients = []

        threading.Thread.__init__(self)
        self.action_data_received = action_data_received
        # create an INET, STREAMing socket
        # bind the socket to a public host, and a well-known port
        print("Opening server " + local_ip + " : " + str(port))
        self.server_socket.bind((local_ip, port))
        # become a server socket
        self.server_socket.listen(5)

    def action_connection_closed(self, easy_socket):
        print("Client disconnected")
        self.connected_clients.remove(easy_socket)

    def on_client_connected(self, socket, address):
        print("Client connected")
        easy_socket_client = EasySocketClient(socket,
                                              lambda data: self.action_data_received(easy_socket_client, address, data),
                                              self.action_connection_closed)
        self.connected_clients.append(easy_socket_client)
        easy_socket_client.start()

    def send_to_all(self, payload):
        for t in self.connected_clients:
            t.send_to_server(payload)

    def run(self):
        while True:
            # accept connections from outside
            (s, address) = self.server_socket.accept()
            self.on_client_connected(s, address)


class EasySocketClient(threading.Thread):

    # Socket must be provided, or create
    def __init__(self, i_socket, action_data_received, action_on_disconnected):
        threading.Thread.__init__(self)
        self.client_socket = i_socket
        self.action_data_received = action_data_received
        self.action_on_disconnected = action_on_disconnected

    def create_socket(self, server_ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, port))

    def close(self):
        self.client_socket.close()

    def send_to_server(self, payload):
        data = pickle.dumps(payload)
        self.client_socket.sendall(struct.pack("L", len(data)) + data)

    def run(self):
        data = b''
        payload_size = struct.calcsize("L")
        while True:
            while len(data) < payload_size:
                try:
                    data_received = self.client_socket.recv(4096)
                except ConnectionResetError:
                    self.action_on_disconnected(self)
                    return
                except ConnectionAbortedError:
                    return
                data += data_received
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                try:
                    buffer = self.client_socket.recv(4096)
                except:
                    self.action_on_disconnected(self)
                    return
                data += buffer
            frame_data = data[:msg_size]
            data = data[msg_size:]
            ###

            result = pickle.loads(frame_data)
            if self.action_data_received is not None:
                self.action_data_received(result)

    def close(self):
        self.client_socket.close();
