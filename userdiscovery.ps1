# UserDiscovery.ps1
# Enumerates users + admin members

$users = Get-WmiObject Win32_UserAccount | Where-Object { $_.LocalAccount -eq $true }

$admins = (Get-WmiObject Win32_GroupUser |
    Where-Object { $_.GroupComponent -like "*Administrators*" }).PartComponent |
    ForEach-Object { ($_ -split "Name=")[1].Trim('"') }

$result = [PSCustomObject]@{
    Hostname       = $env:COMPUTERNAME
    Users          = $users
    Administrators = $admins
}

$result | ConvertTo-Json -Depth 6
