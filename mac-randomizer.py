#!/usr/bin/env python3

import argparse
import random
import subprocess
import re
from os import geteuid

def mac(file):
    with open(file , encoding="utf-8") as file:
        _mac_addr = file.read().splitlines()
    
    return random.choice(_mac_addr)

def interface():
    output = subprocess.check_output("ip link".split() , text=True)
    pattern = re.findall(r": [a-zA-Z0-9]+:" , output)
    print(f"\033[1m{'*'*10} Interfaces Available {'*'*10}\033[0m")
    for i in range(len(pattern)):
        print(f"{i+1}> {pattern[i][2:-1]}")
    choice = int(input("Enter which interface -> "))-1
    try:
        return pattern[choice][2:-1]
    except KeyboardInterrupt:
        print("CTRL+c pressed")
        exit()
    except IndexError:
        print("Error: please choose a valid number ")
        exit()

def change_mac(inter , mac_addr):
    subprocess.check_output(["ifconfig", inter, "down"], text=True)
    subprocess.check_output(["ifconfig", inter, "hw", "ether", mac_addr], text=True)
    subprocess.check_output(["ifconfig", inter, "up"], text=True)
    
    output = subprocess.check_output(f"ifconfig {inter}".split(), text=True)
    pattern = re.findall(r"ether [0-9A-Za-z:]+  " , output)
    return pattern[0][6:-2]

def main(file):
    inter = interface()
    mac_addr = mac(file)
    print(mac_addr)

    output = subprocess.check_output(f"ifconfig {inter}".split(), text=True)
    pattern = re.findall(r"ether [0-9A-Za-z:]+  " , output)
    original_mac_addr = pattern[0][6:-2]
    print(original_mac_addr)
    
    changed_mac_addr = change_mac(inter,mac_addr)

    if changed_mac_addr == original_mac_addr:
        print(f"\033[31m [!] Error Changing the mac address of {inter} \033[0m")
    else:
        print(f"\033[32m [+] Sucess in changing the mac address of {inter} \033[0m")
        print(f"Changed Mac address -> {changed_mac_addr}")

if __name__ == "__main__":
    if geteuid() != 0:
        print(f"\033[31m [!] Please run the script as root \033[0m")
        exit()
    parser = argparse.ArgumentParser(description="*** Script to randomize the mac address *** ")
    parser.add_argument("--file" , type=str , required=True , help="path to the file")

    args = parser.parse_args()
    main(args.file)
