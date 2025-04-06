#!/usr/bin/env python3

import paramiko
import argparse
import getpass
from datetime import datetime
import os

def run_remote_commands(host, user, password=None, key_file=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_file:
            client.connect(hostname=host, username=user, key_filename=key_file)
        else:
            client.connect(hostname=host, username=user, password=password)

        print(f"\n🔗 Connected to {host}\n")

        # Setup log file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_host = host.replace(":", "_").replace("/", "_")
        log_file = os.path.join("logs", f"{safe_host}_{timestamp}.log")

        log = open(log_file, "w")
        log.write(f"🔗 Connected to {host} at {timestamp}\n")

        # Detect OS type
        stdin, stdout, stderr = client.exec_command("uname")
        os_type = stdout.read().decode().strip().lower()
        print(f"🧠 Detected OS: {os_type}")
        log.write(f"🧠 Detected OS: {os_type}\n")

        # Choose commands based on OS
        if os_type == "linux":
            commands = [
                "hostname",
                "uptime",
                "df -h",
                "free -m",
                "top -b -n 1 | head -20",
                "who"
            ]
        elif os_type == "darwin":
            commands = [
                "hostname",
                "uptime",
                "df -h",
                "vm_stat",
                "top -l 1 | head -20",
                "who"
            ]
        else:
            print("⚠️ Unknown OS type. Running limited commands.")
            log.write("⚠️ Unknown OS type. Running limited commands.\n")
            commands = ["hostname", "uptime"]

        for cmd in commands:
            print(f"\n👉 Running: {cmd}")
            log.write(f"\n👉 Running: {cmd}\n")

            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                print(output)
                log.write(output + "\n")
            if error:
                print(f"⚠️ Error:\n{error}")
                log.write(f"⚠️ Error:\n{error}\n")

        log.write("\n✅ End of log\n")
        log.close()
        print(f"\n📁 Output saved to: {log_file}")
        client.close()

    except Exception as e:
        print(f"❌ Connection to {host} failed: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH into a server and run basic troubleshooting commands.")
    parser.add_argument("host", help="Hostname or IP of the server")
    parser.add_argument("-u", "--user", required=True, help="Username for SSH")
    parser.add_argument("-k", "--key", help="Path to SSH private key")
    parser.add_argument("-p", "--password", action="store_true", help="Prompt for SSH password")
    args = parser.parse_args()

    if args.password:
        password = getpass.getpass("Password: ")
    else:
        password = None

    run_remote_commands(args.host, args.user, password=password, key_file=args.key)

