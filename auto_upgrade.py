#!/usr/bin/env python3

import os

file = os.popen("pip3 list --outdated --trusted-host mirrors.cloud.aliyuncs.com")
namelist = []
for line in file:
    data = line.split()
    namelist.append(data[0])
namelist = namelist[2:]
print("Available Packages:")
print(namelist)

for name in namelist:
    command = "pip3 install --upgrade " + name
    print(command)
    os.system(command)
print("PIP3 Upgrade Successfully")