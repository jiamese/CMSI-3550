import socket

def get_private_ip():
    hostname = socket.gethostname()  # Get  hostname of the computer
    private_ip = socket.gethostbyname(hostname)  # Get  private IP based on hostname
    return private_ip

print("Your private IP address is:", get_private_ip())
