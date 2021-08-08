import ipaddress


def constructUrl(ip: ipaddress.IPv4Address, port: int, proto: str = "http") -> str:
    return f"{proto}{'://' if proto.strip() else ''}{ip.__str__()}:{port}"
    