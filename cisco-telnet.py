import pexpect, os, subprocess

# create a nested dict to store Cisco router prompts and IP's
devices = {
    "iosv-1": {"prompt": "iosv-1#", "ip": "192.168.70.1"},
    "iosv-2": {"prompt": "iosv-2#", "ip": "192.168.70.2"},
}
username = "cisco"
password = "cisco"
more = " --More-- "

filename = "results.txt"
file_exists = os.path.exists("results.txt")
if file_exists:
    print("\nWill now erase exisiting file contents\nto store fresh router data on this run..")
    with open(filename, 'w') as f:  # just open and close it in 'w' mode to overwrite past contents without reacreating
        # a file each time (overhead considerations??)
        f.close()
else:
    print("Creating new file. Data will be added to it during the telnet connection to Cisco network.")
    with open(filename, 'x') as f:  # 'x' is exclusively for creation
        f.close()
# iterate over each object in the dict - do - foreach device
for device in devices.keys():
    dev_prompt = devices[device]["prompt"]  # the value of "prompt" key
    child = pexpect.spawn(
        f"telnet {devices[device]['ip']}")  # shorthand formatting for var injection to open telnet sesh
    child.expect("Username:")
    child.sendline(username)
    child.expect("Password:")
    child.sendline(password)
    child.expect(dev_prompt)
    child.sendline("show version | include V")
    child.expect(dev_prompt)
    child.sendline("show run | begin interface")
    child.expect(more)  # because the actual output goes beyond screen bounds
    child.sendcontrol('z')  # equivalent to CNTRL-Z
    data = child.before
    s = data.decode().split("\n")  # DEEBEES :) convert bytes to str first

    for i in range(len(s)):
        if i == 0:  # exclude the echoed 'sendline'
            continue
        output = f"{s[i].lstrip()}\n"
        with open(filename, 'a') as f:
            f.writelines(output)
    child.sendline("exit")

interfaces = subprocess.run(["grep -iEA5 --color=always 'g[a-z]{10,}0\/0' %s" %filename], stdout=subprocess.PIPE, text=True, shell=True)
print(f"\n{interfaces.stdout}")
