#!/usr/bin/env python3

import os
import time
import re
import requests
from dotenv import load_dotenv

# load enviornment variables
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LOGFILE = "/var/log/auth.log"

# Ensure discord webhook url is set
if not DISCORD_WEBHOOK_URL:
    raise RuntimeError("DISCORD_WEBHOOK_URL is not set")

# Function to send message to Discord webhook
def send_discord_message(message: str):
    payload = {"content": message}
    try:
        requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
    except requests.RequestException:
        pass

def follow(file_path):
    """Mimics tail -F (supports log rotation)."""
    with open(file_path, "r") as f:
        f.seek(0, os.SEEK_END)
        inode = os.fstat(f.fileno()).st_ino

        while True:
            line = f.readline()
            if line:
                yield line
            else:
                try:
                    if os.stat(file_path).st_ino != inode:
                        f.close()
                        f = open(file_path, "r")
                        inode = os.fstat(f.fileno()).st_ino
                except FileNotFoundError:
                    pass
                time.sleep(0.5)

failed_re = re.compile(r"Failed password for (invalid user )?(\S+)")
invalid_re = re.compile(r"Invalid user (\S+)")
accepted_re = re.compile(r"Accepted .* for (\S+)")
ip_re = re.compile(r"from (\S+) port")

for line in follow(LOGFILE):

    # FAILED LOGIN
    if "Failed password" in line:
        user_match = failed_re.search(line)
        ip_match = ip_re.search(line)

        if user_match and ip_match:
            user = user_match.group(2)
            ip = ip_match.group(1)
            send_discord_message(
                f"❌ **SSH Failed Login**\nUser: `{user}`\nIP: `{ip}`"
            )

    # INVALID USER
    elif "Invalid user" in line:
        user_match = invalid_re.search(line)
        ip_match = ip_re.search(line)

        if user_match and ip_match:
            user = user_match.group(1)
            ip = ip_match.group(1)
            send_discord_message(
                f"⚠️ **SSH Invalid User Attempt**\nUser: `{user}`\nIP: `{ip}`"
            )

    # SUCCESSFUL LOGIN
    elif "Accepted" in line:
        user_match = accepted_re.search(line)
        ip_match = ip_re.search(line)

        if user_match and ip_match:
            user = user_match.group(1)
            ip = ip_match.group(1)
            send_discord_message(
                f"✅ **SSH Login Success**\nUser: `{user}`\nIP: `{ip}`"
            )
