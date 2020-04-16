from netmiko import ConnectHandler
import os

net_connect = ''

#Starts an SSH connection to a router
def do_login(ip):
    global net_connect
    uname = "user"
    pw = "cisco"

    ROUTER = {
        'device_type': 'cisco_ios',
        'username': uname,
        'password': pw,
        'ip': ip,
        'secret': 'testpass',
    }
    net_connect = ConnectHandler(**ROUTER)
    print("Connected to " + ip)

def main():
    do_login("192.168.31.136")
    print(net_connect.enable())
    print(net_connect.send_config_set("logging buffered 10000"))

if __name__ == '__main__':
    main()
