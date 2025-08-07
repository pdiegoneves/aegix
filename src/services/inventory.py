import getpass
import platform
import socket

import psutil
from getmac import get_mac_address


class Inventory():
    def __init__(self):
        self._hostname = None
        self._username = None
        self._ip_address = None
        self._operational_system = None
        self._processor = None
        self._mac_address = None
        self._disk_space = None
        self._memory = None
        
    def _get_hostname_from_inventory(self) -> str:
        return socket.gethostname()
    
    def _get_username_from_inventory(self) -> str:
        return getpass.getuser()
     
    def _get_ip_address_from_inventory(self) -> str:
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
            
        finally:
            if s is not None:
                s.close()
        return ip

    def _get_operational_system_from_inventory(self) -> str:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        return f"{system} {release} {version}"
    
    def _get_processor_from_inventory(self) -> str:
        processor = platform.processor()    
        return processor
    
    def _get_mac_address_from_inventory(self) -> str:
        mac = get_mac_address().upper()
        return mac

    def _lenght_format(selfm, bytes_val, sufixo='B'):
        for unidade in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(bytes_val) < 1024.0:
                return f"{bytes_val:3.1f} {unidade}{sufixo}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} Y{sufixo}"

    def _get_disk_space_from_inventory(self) -> list:
        partitions = psutil.disk_partitions()
        usage_list = {}
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
        
            usage_dict = {
                'Total': self._lenght_format(usage.total),
                'Used': self._lenght_format(usage.used),
                'Free': self._lenght_format(usage.free),
                'Percent': f"{usage.percent}%"
            }
            
            device = partition.device.removesuffix(':\\')
            usage_list[device] = usage_dict
        
        return usage_list


    def generate_report_by_console(self):
        print(f"Hostname: {self._get_hostname_from_inventory()}")
        print(f"Username: {self._get_username_from_inventory()}")
        print(f"IP Address: {self._get_ip_address_from_inventory()}")
        print(f"Operational System: {self._get_operational_system_from_inventory()}")
        print(f"Processor: {self._get_processor_from_inventory()}")
        print(f"MAC Address: {self._get_mac_address_from_inventory()}")
        print(f"Disk Space: {self._get_disk_space_from_inventory()}")
        
        

    