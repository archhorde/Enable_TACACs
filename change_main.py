from netmiko import ConnectHandler

net_connect = ''

def do_login():
    #Starts an SSH connection to a router
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

def do_check_tacacs(file):
    #Checks if tacacs is already enabled
    global net_connect
    #output = net_connect.send_command('show run')
    #print(output)

def do_add_tacacs(ip):
    #Change the speed and duplex of a router"""
    global net_connect

    #output = net_connect.send_config_set(config_commands)


#Main loop of program
def main():

    f = open("router_list.txt", "r")
    #print(f.read())
    for line in f:
        line = f.readline()



if __name__ == '__main__':
    main()
