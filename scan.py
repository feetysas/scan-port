import socket
import time

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            service = get_service_name(port)
            return f"[{port}] [OPEN] [{service}]"
        else:
            return f"[{port}] [CLOSED]"
    except:
        return f"[{port}] [ERROR]"

def get_service_name(port):
    
    services = {
        21: "FTP",
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        3306: "MySQL"
    }
    return services.get(port, "UNKNOWN")

def main():
    print("\n\033[1;36m" + "="*40 + "\033[0m")
    print("\033[1;36Discord : 5wrr \033[0m")
    print("\033[1;36m" + "="*40 + "\033[0m\n")
    
    target = input("Enter target IP or domain: ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))
    
    print(f"\nScanning {target}...\n")
    
    for port in range(start_port, end_port + 1):
        result = scan_port(target, port)
        print(result)
        time.sleep(0.1) 
    
    print("\nScan completed!")

if __name__ == "__main__":
    main()
