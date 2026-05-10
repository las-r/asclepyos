from pathlib import Path
from runpy import run_path
import os
import subprocess
import sys
import time

# asclepyos main
# made by las-r on github

# helpers
def checkargs(args, alen):
    if len(args) != alen:
        return True
    return False

def formatsize(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:6.2f} {unit}"
        size /= 1024
    return f"{size:6.2f} TB"

# internal commands
def iver(args):
    print("AsclepyOS v2026.1")

def iexit(args):
    sys.exit(0)

def ilsdir(args):
    path = args[0] if args else "."
    try:
        print(f"{'TYPE':<10} {'SIZE':<12} {'NAME'}")
        print("-" * 40)
        with os.scandir(path) as entries:
            for entry in entries:
                info = entry.stat()
                if entry.is_dir():
                    ftype = "<DIR>"
                    fsize = ""
                else:
                    ftype = "FILE"
                    fsize = formatsize(info.st_size)
                print(f"{ftype:<10} {fsize:<12} {entry.name}")
    except FileNotFoundError:
        print("Path not found.")

# constants
VER = "v2026.1"
BIN = "bin/"
CFG = "cfg/"
CMDS = {
    "ver": iver,
    "exit": iexit,
    "ld": ilsdir, "lsdir": ilsdir,
    
}

def main():
    # env
    cdir = "./"
    
    # shell loop
    try:
        while True:
            cmds = input(f"~{cdir}> ").split(";")
            for cmd in cmds:
                cmd = cmd.strip()
                if not cmd: continue
                
                # split command
                cmda = cmd.split(" ")
                name = cmda[0].lower()
                args = cmda[1:]

                # internal
                if name in CMDS:
                    CMDS[name](args)
                    
                # external
                else:
                    localpy = Path(cdir) / f"{name}.py"
                    localexe = Path(cdir) / f"{name}.exe"
                    
                    # local
                    if localpy.is_file():
                        subprocess.run([sys.executable, str(localpy)] + args)
                    elif localexe.is_file():
                        subprocess.run([str(localexe)] + args)
                        
                    # bin
                    else:
                        binpy = Path(BIN) / f"{name}.py"
                        if binpy.is_file():
                            subprocess.run([sys.executable, str(binpy)] + args)
                        else:
                            print(f"Bad command or file: {name}")
                            
    # ctrl c
    except KeyboardInterrupt:
        print("Use 'exit' to quit AsclepyOS")

if __name__ == "__main__":
    main()