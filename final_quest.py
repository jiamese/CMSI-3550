import socket
import requests
import threading

# Function to demonstrate HTTP GET request
def http_get_example(url):
    print("Performing HTTP GET request...")
    try:
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text[:200]}...")  # Print first 200 chars
    except Exception as e:
        print(f"HTTP GET request failed: {e}")

# Function to demonstrate a UDP client-server interaction
def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    print("UDP Server is running and waiting for messages...")

    while True:
        message, client_address = server_socket.recvfrom(1024)  # Buffer size 1024 bytes
        print(f"Received message: {message.decode()} from {client_address}")
        server_socket.sendto(b"ACK: " + message, client_address)

def udp_client(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    try:
        print(f"Sending message: {message}")
        client_socket.sendto(message.encode(), server_address)
        response, _ = client_socket.recvfrom(1024)
        print(f"Received response from server: {response.decode()}")
    finally:
        client_socket.close()

# Function to demonstrate a TCP client-server interaction
def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 54321)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("TCP Server is running and waiting for connections...")

    while True:
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection established with {client_address}")
            data = connection.recv(1024)
            print(f"Received data: {data.decode()}")
            connection.sendall(b"ACK: " + data)
        finally:
            connection.close()

def tcp_client(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 54321)
    try:
        client_socket.connect(server_address)
        print(f"Sending message: {message}")
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        print(f"Received response from server: {response.decode()}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("Networking Concepts Demo Program")
    print("1. HTTP GET Request")
    print("2. UDP Server-Client")
    print("3. TCP Server-Client")
    choice = input("Choose an option (1/2/3): ").strip()

    if choice == '1':
        url = input("Enter the URL for HTTP GET request: ").strip()
        http_get_example(url)
    elif choice == '2':
        threading.Thread(target=udp_server, daemon=True).start()
        message = input("Enter a message to send via UDP: ").strip()
        udp_client(message)
    elif choice == '3':
        threading.Thread(target=tcp_server, daemon=True).start()
        message = input("Enter a message to send via TCP: ").strip()
        tcp_client(message)
    else:
        print("Invalid choice. Exiting.")
