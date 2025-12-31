#!/usr/bin/env python3
"""
PwnPlug Lite Module: User Discovery
Author: Jeremy Shane Butts (CyberGeekJSB)
"""

import os, json, win32com.client
from datetime import datetime

LOG = "/opt/pwnplug/logs/user_discovery.json"

def log(data):
    os.makedirs("/opt/pwnplug/logs/", exist_ok=True)
    with open(LOG, "a") as f:
        f.write(json.dumps(data) + "\n")


def wmi_query(q):
    return win32com.client.GetObject("winmgmts:").ExecQuery(q)


def get_users():
    q = "SELECT * FROM Win32_UserAccount WHERE LocalAccount = True"
    return [{
        "Name": u.Name,
        "Domain": u.Domain,
        "SID": u.SID,
        "Disabled": u.Disabled
    } for u in wmi_query(q)]


def get_admins():
    comp = os.getenv("COMPUTERNAME")
    q = f"""
    SELECT * FROM Win32_GroupUser
    WHERE GroupComponent="Win32_Group.Domain='{comp}',Name='Administrators'"
    """
    entries = wmi_query(q)
    members = []
    for e in entries:
        if "Win32_UserAccount" in e.PartComponent:
            members.append(e.PartComponent.split("Name=")[1].replace('"', ''))
    return members


def run(silent=False):
    data = {
        "timestamp": str(datetime.utcnow()),
        "hostname": os.getenv("COMPUTERNAME"),
        "users": get_users(),
        "administrators": get_admins()
    }

    log(data)

    if not silent:
        print(json.dumps(data, indent=4))

    return data


if __name__ == "__main__":
    run()


