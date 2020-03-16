from netmiko import ConnectHandler

net_connect = ''

#Starts an SSH connection to a router
def do_login(ip):
    global net_connect
    uname = "admin"
    pw = "labadmin8"

    ROUTER = {
        'device_type': 'cisco_ios',
        'username': uname,
        'password': pw,
        'ip': ip,
    }
    net_connect = ConnectHandler(**ROUTER)
    print("Connected to " + ip)

#Checks if tacacs is already enabled.
def do_check_tacacs(ip):
    global net_connect
    do_login(ip)
    output = net_connect.send_command('show tacacs')
    if len(output) > 0:
        print ("Tacacs is enabled")
        return True
    else:
        do_add_tacacs(ip)

def do_get_wan_int():
    global net_connect
    output = net_connect.send_command('show ip cef')

# Adds Tacacs to a router.
def do_add_tacacs():
    global net_connect
    with open("tacacs_temp.txt", "r") as f:
        print("Adding Tacacs...")
        output = net_connect.send_config_set(f)


#Main loop of program
def main():

    with open("router_list.txt", "r") as f:
        for line in f:
            line = line.strip()
            pair = line.split()
            host = pair[0]
            ip = pair[1]
            print("HOST IS: " + host + " IP IS: " + ip)

            if do_check_tacacs(ip) == False:
                do_add_tacacs(ip)
                print("Added tacacs for IP " + ip)


if __name__ == '__main__':
    main()
