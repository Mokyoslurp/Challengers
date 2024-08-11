import socket
from _thread import start_new_thread

# Set here your local ip address
SERVER = "192.168.0.102"
# Set here an unused port
PORT = 5050


def threaded_client(connection: socket.socket):
    connection.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            # Argument is amount of information you want to receive (bits)
            data = connection.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            connection.sendall(str.encode(reply))
        except:  # noqa: E722
            break

    print("Lost connection")
    connection.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((SERVER, PORT))
    except socket.error as e:
        print(e)

    # Argument is the number of client that can connect
    s.listen(2)
    print("Waiting for connection, server started!")

    while True:
        connection, address = s.accept()
        print("Connected to: ", address)

        start_new_thread(threaded_client, (connection,))
