from netmiko import ConnectHandler
import os

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
        return False

def do_get_wan_int():
    global net_connect
    route = "none"
    hop = "none"
    wan_interface = "none"

    if os.path.exists("showcefoutput.txt"):
        os.remove("showcefoutput.txt")

    output = net_connect.send_command('show ip cef')
    outputfile = open("showcefoutput.txt", "x")
    outputfile.write(output)
    outputfile.close()

    with open ("showcefoutput.txt", "r") as f:
        for line in f:
            line = line.strip()

            pair = line.split()

            if len(pair) >1:
                route = pair[0]
                hop = pair[1]

            if len(pair)>2:
                interface = pair[2]

            if route == "0.0.0.0/0":
                wan_interface = interface
    if os.path.exists("showcefoutput.txt"):
        os.remove("showcefoutput.txt")
    else:
        print("The file does not exist")

    return wan_interface

# Adds Tacacs to a router.
def do_add_tacacs(int):
    global net_connect
    source_int = "ip tacacs source-interface " + int

    if os.path.exists("newtacacs.txt"):
        os.remove("newtacacs.txt")

    outputfile = open("newtacacs.txt", "x")
    outputfile.close()

    with open("newtacacs.txt", "a") as a:
        with open("tacacs_temp.txt", "r") as f:
            for line in f:
                a.write(line)
            a.write(source_int)

            print("Adding Tacacs...")

    outputfile = open("newtacacs.txt", "r")
    output = net_connect.send_config_set(outputfile)
    outputfile.close()

    if os.path.exists("newtacacs.txt"):
        os.remove("newtacacs.txt")

def do_save_config():
    global net_connect
    net_connect.save_config(confirm = True)
    print("config saved")

#Main loop of program
def main():

    if os.path.exists("results.txt"):
        os.remove("results.txt")

    with open("router_list.txt", "r") as f:
        with open("results.txt", "w") as a:
            for line in f:
                line = line.strip()
                pair = line.split()
                host = pair[0]
                ip = pair[1]
                #print("HOST IS: " + host + " IP IS: " + ip)

                if do_check_tacacs(ip) == False:
                    int = do_get_wan_int()
                    do_add_tacacs(int)
                    do_save_config()
                    a.write(host + " " + ip + " success")
                else:
                    a.write(host + " " + ip + " failure")


if __name__ == '__main__':
    main()
