"""
Simple SSH Shell Client
-----------------------
A lightweight Python SSH client using Paramiko that allows remote command execution.

Author: Kofu (GitHub: @kofudev)
Note: Make sure not to hardcode sensitive credentials.
"""


import paramiko
import socket

#-------------------------
# SSH Connection Information
#-------------------------------
HOST = "your_server_ip"# Replace with your server IP
PORT = 22# SSH port (default 22)
USER = "your_username"# Replace with your username
PASSWORD = "your_password"# Replace with your password or use getpass

#-------------------------------
#Create SSH Client
#-------------------------------
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    #Connect to the server
    client.connect(HOST, port=PORT, username=USER, password=PASSWORD)

    #Function to execute a command and return output
    def run(cmd):
        stdin, stdout, stderr = client.exec_command(cmd)
        return stdout.read().decode().strip()

    #Initial info for prompt
    hostname = run("hostname")
    cwd = run("pwd")

    #---------------------------
    #Main Shell Loop
    #------------------------------
    while True:
        try:
            cmd = input(f"{USER}@{hostname}:{cwd}$ ")

            #Exit the shell
            if cmd in ["exit", "quit", "logout"]:
                break

            #Execute command
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()

            if out:
                print(out, end="")
            if err:
                print(err, end="")

            #Update current working directory
            cwd = run("pwd")

        except (socket.error, paramiko.SSHException):
            print("\n❌ Connection lost due to network or server error.")
            break

except paramiko.AuthenticationException:
    print("❌ Authentication failed (invalid username or password).")

except Exception as e:
    print(f"❌ Connection closed due to: {e}")
     
finally:
    client.close()
    print("\n✅ SSH session closed. Script by Kofu .")
