from netmiko import ConnectHandler

net_connect = ''

def do_login(self,args):
    """Starts an SSH connection to a router"""
    global net_connect
    ip = input("Enter router IP:\n")
    uname = input("Enter Username:\n")
    pw = input("Enter Password:\n")

    ROUTER = {
        'device_type': 'cisco_ios',
        'username': uname,
        'password': pw,
        'ip': ip,
    }
    net_connect = ConnectHandler(**ROUTER)

if __name__ == '__main__':
    main()
