import sys

# wc: word counter
# included w/ asclepyos
# made by las-r on github

if len(sys.argv) < 2:
    print("usage: wc <filename>")
    sys.exit()
    
filename = sys.argv[1]
try:
    with open(filename, "r") as f:
        lines = f.readlines()
        
    lc = len(lines)
    wc = sum(len(line.split()) for line in lines)
    cc = sum(len(line) for line in lines)
        
    print(f"Lines: {lc}")
    print(f"Words: {wc}")
    print(f"Characters: {cc}")
except FileNotFoundError:
    print("File not found.")