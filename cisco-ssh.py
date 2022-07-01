import getpass
from pexpect import pxssh

devices = {'iosv-1': {'prompt': 'iosv-1#', 'ip': '192.168.70.1'},
           'iosv-2': {'prompt': 'iosv-2#', 'ip': '192.168.70.2'}}
# term len eq zero is a solution to eliminate the "More" prompt I had to work around
# in the telnet program (when output exceeds default of 24 lines) - setting of 0 effectively disables the "More" prompt
commands = ['term length 0', 'show version', 'show run']
username = input('Username: ')
password = getpass.getpass('Password: ')

# Starts the loop for devices
for device in devices.keys():
    outputFileName = f"{device}_output.txt"
    device_prompt = devices[device]['prompt']
    child = pxssh.pxssh()
    # Auto prompt param set to False in order to eliminate incompatibility with forcing PS1 on Cisco devices
    child.login(devices[device]['ip'], username.strip(), password.strip(), auto_prompt_reset=False)

    # Starts the loop for commands and write to output
    with open(outputFileName, 'wb') as f:
        for command in commands:
            child.sendline(command)
            child.expect(device_prompt)
            f.write(child.before) # will output the info between our sendline and expect, in this case,
            # output of 'show vers' and 'show run' foreach device filename
    child.logout()
