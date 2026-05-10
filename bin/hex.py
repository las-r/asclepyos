import os
import sys

# hex: dump raw bytes
# included w/ asclepyos
# made by las-r on github

if len(sys.argv) < 2:
    print("usage: hex <filename>")
    sys.exit()

filename = sys.argv[1]

if os.path.exists(filename):
    with open(filename, "rb") as f:
        offset = 0
        while (chunk := f.read(16)):
            hex_bytes = chunk.hex(" ").upper()
            print(f"{offset:08X}: {hex_bytes:<47}")
            offset += 16
else:
    print("File not found.")
