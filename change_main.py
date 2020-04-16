from netmiko import ConnectHandler
import os

net_connect = ''

#Starts an SSH connection to a router
def do_login(ip):
    global net_connect

    TROUTER = {
        'device_type': 'cisco_ios',
        'username': "test",
        'password': "test",
        'ip': ip,
    }
    NOCROUTER  = {
        'device_type': 'cisco_ios',
        'username': "user",
        'password': "pass",
        'ip': ip,
        'secret': 'Granite1!'
    }
    CLOUD  = {
        'device_type': 'cisco_ios',
        'username': "base",
        'password': "pass",
        'ip': ip,
        'secret': 'cisco'
    }
    while True:
        try:
            net_connect = ConnectHandler(**TROUTER)
            print("Connected to " + ip)
            break
        except:
            print("Failed to login with tacacs")
            pass

        try:
            net_connect = ConnectHandler(**NOCROUTER)
            print("Connected to " + ip)
            break
        except:
            print("Failed to login with noc creds")
            pass

        try:
            net_connect = ConnectHandler(**CLOUD)
            print("Connected to " + ip)
            break
        except:
            print("Failed to login with cloud creds")
            pass


#Checks if tacacs is already enabled.
def do_check_tacacs(ip):
    global net_connect
    FAIL = "FAIL"
    try:
        do_login(ip)
        output = net_connect.send_command('show tacacs')
        if len(output) > 0:
            print ("Tacacs is enabled")
            return True
        else:
            return False
    except:
        return FAIL

#Get the internet facing interface, as shown by show ip cef
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

    #Looping through output of show ip cef, looking for the default route's next hop interface
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

    #Creates a new temp text file to store new tacacs config, deleting the file if it already exists
    if os.path.exists("newtacacs.txt"):
        os.remove("newtacacs.txt")

    outputfile = open("newtacacs.txt", "x")
    outputfile.close()

    #Copies tacacs template into new file, then adds proper wan interface to end
    with open("newtacacs.txt", "a") as a:
        with open("tacacs_temp.txt", "r") as f:
            for line in f:
                a.write(line)
            a.write(source_int)

            print("Adding Tacacs...")

    print(net_connect.enable())
    outputfile = open("newtacacs.txt", "r")
    output = net_connect.send_config_set(outputfile)
    outputfile.close()

    #Deletes temp tacacs config file
    if os.path.exists("newtacacs.txt"):
        os.remove("newtacacs.txt")

#Save config of the router
def do_save_config():
    global net_connect
    #net_connect.save_config(confirm = True)
    print("config saved")

#Main loop of program, output is a results.txt file in format [hostname ip success/failure]
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

                result = do_check_tacacs(ip)
                if  result == False:
                    int = do_get_wan_int()
                    do_add_tacacs(int)
                    do_save_config()
                    a.write(host + " " + ip + " tacacs enabled\n")
                elif result ++ True:
                    a.write(host + " " + ip + " tacacs already enabled\n")
                else:
                    a.write(host + " " + ip + " unreachable\n")

if __name__ == '__main__':
    main()
