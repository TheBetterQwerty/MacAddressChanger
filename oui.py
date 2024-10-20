import re
import sys
import random

chars = [chr(i) for i in range(65,71)]
chars += [chr(i) for i in range(97,103)]
chars += [chr(i) for i in range(48,58)]

with open(sys.argv[1] , encoding="utf-8") as file:
	a=file.read()

patterns = re.findall(r'[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}', a)

with open (sys.argv[2] , "a") as file:
    for pattern in patterns:
        NIC = ""
        for i in range(3):
            NIC += ":"
            NIC += random.choice(chars)
            NIC += random.choice(chars)
        pattern = ":".join(pattern.split("-"))
        mac = pattern+NIC
        print(mac)
        file.write(mac+"\n")

print("** done **")
