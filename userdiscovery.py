#!/usr/bin/env python3
"""
UserDiscovery.py
Author: CyberGeekJSB (Jeremy Shane Butts)
Purpose: Enumerate local Windows user accounts and Administrators group members using WMI.
"""

import json
import win32com.client


def wmi_query(q):
    wmi = win32com.client.GetObject("winmgmts:")
    return wmi.ExecQuery(q)


def get_users():
    q = """
        SELECT * FROM Win32_UserAccount
        WHERE LocalAccount = True
        ORDER BY Name
    """
    results = wmi_query(q)

    users = []
    for u in results:
        users.append({
            "Name": u.Name,
            "Domain": u.Domain,
            "SID": u.SID,
            "Disabled": u.Disabled,
            "Lockout": u.Lockout,
            "PasswordRequired": u.PasswordRequired,
            "PasswordChangeable": u.PasswordChangeable,
            "PasswordExpires": u.PasswordExpires,
            "Description": u.Description
        })
    return users


def get_hostname():
    cs = wmi_query("SELECT * FROM Win32_ComputerSystem")
    for c in cs:
        return c.Name
    return "UNKNOWN"


def get_admin_group():
    comp = get_hostname()
    q = f"""
        SELECT * FROM Win32_GroupUser
        WHERE GroupComponent="Win32_Group.Domain='{comp}',Name='Administrators'"
    """

    entries = wmi_query(q)
    members = []

    for e in entries:
        if "Win32_UserAccount" in e.PartComponent:
            raw = e.PartComponent.split("Name=")[1]
            members.append(raw.replace('"',''))
    return members


def main():
    hostname = get_hostname()
    users = get_users()
    admins = get_admin_group()

    result = {
        "hostname": hostname,
        "users": users,
        "administrators": admins
    }

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
