import os
import sys

# shred: securely deletes a file
# included w/ asclepyos
# made by las-r on github

if len(sys.argv) < 2:
    print("usage: shred <filename>")
    sys.exit()

filename = sys.argv[1]

if os.path.exists(filename):
    size = os.path.getsize(filename)
    try:
        with open(filename, "wb") as f:
            f.write(os.urandom(size))
        os.remove(filename)
        print(f"Successfully shredded {filename} ({size} bytes).")
    except Exception as e:
        print(f"Error during shredding: {e}")
else:
    print("File not found.")
