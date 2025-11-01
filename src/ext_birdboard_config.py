import socket

class BirdBoard :

    def __init__(self,ownerComp):
        self.ownerComp = ownerComp
        pass


    def GetAllIPAddresses(self):
        ip_table = op.config.op('my_IPs')
        ip_table.clear()
        ip_table.appendRow(['Local IPs'])  # Header row

        hostname = socket.gethostname()
        try:
            # This gets the primary IP only
            primary_ip = socket.gethostbyname(hostname)
            ip_table.appendRow([primary_ip])
        except Exception as e:
            ip_table.appendRow([f"Error: {e}"])
            return

        # Attempt to find additional IPs using getaddrinfo (more complete)
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            seen = set([primary_ip])  # Avoid duplicates
            for entry in addr_info:
                ip = entry[4][0]
                if '.' in ip and ip not in seen and not ip.startswith('127.'):
                    ip_table.appendRow([ip])
                    seen.add(ip)
        except Exception as e:
            ip_table.appendRow([f"Extra Error: {e}"])

        return



