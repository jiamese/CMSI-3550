import socket
# install dnslib
from dnslib import DNSRecord, RR, QTYPE, A

HOST = '0.0.0.0'  
PORT = 53  
DOMAIN_MAPPING = {
    "example.com": "192.168.1.10",
    "test.com": "192.168.1.20",
    "google.com": "8.8.8.8"
}

def dns_response(data):
    request = DNSRecord.parse(data)
    reply = DNSRecord(request.header) 

    print(f"Received query for: {request.q.qname}")

    qname = str(request.q.qname).strip('.')
    if qname in DOMAIN_MAPPING:
        ip_address = DOMAIN_MAPPING[qname]
        print(f"Responding with IP: {ip_address}")
        reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(ip_address), ttl=60))
    else:
        print(f"No mapping found for {qname}. Sending NXDOMAIN.")
    
    return reply.pack()

def start_dns_server():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"DNS server started on {HOST}:{PORT}")

        while True:
            try:
                data, addr = sock.recvfrom(512)
                print(f"Request from {addr}")

                response = dns_response(data)

                sock.sendto(response, addr)
            except KeyboardInterrupt:
                print("DNS server shutting down.")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    start_dns_server()

