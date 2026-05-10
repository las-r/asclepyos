from pathlib import Path
import os
import shlex
import shutil
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

def resvpath(vdir, target):
    if target.startswith("~/"):
        fpath = (ROOT / target[2:]).resolve()
    elif target.startswith("/"):
        fpath = (ROOT / target.lstrip("/")).resolve()
    else:
        fpath = (ROOT / vdir.lstrip("/")).joinpath(target).resolve()
    if ROOT in fpath.parents or fpath == ROOT:
        return fpath
    else:
        return None

# internal command functions
def ilsdir(args, vdir):
    targetv = args[0] if args else "."
    path = resvpath(vdir, targetv)
    try:
        print(f"{'TYPE':<10} {'SIZE':<12} {'NAME'}")
        print("-" * 40)
        with os.scandir(path) as entries:
            for entry in entries:
                info = entry.stat()
                ftype = "<DIR>" if entry.is_dir() else "FILE"
                fsize = "" if entry.is_dir() else formatsize(info.st_size)
                print(f"{ftype:<10} {fsize:<12} {entry.name}")
    except (FileNotFoundError, TypeError):
        print("Path not found or access denied.")

def ichdir(args, vdir):
    if not args or args[0] == "~":
        return "/"
    target = args[0]
    nrpath = resvpath(vdir, target)
    if nrpath and nrpath.is_dir():
        if nrpath == ROOT:
            return "/"
        vpath = "/" + str(nrpath.relative_to(ROOT)).replace("\\", "/")
        return vpath.replace("//", "/")
    else:
        print("Bad directory.")
        return vdir

def imkdir(args, vdir):
    if len(args) < 1:
        print("usage: md <DIRNAME>")
        return
    path = resvpath(vdir, args[0])
    if path:
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory: {e}")
    else:
        print("Invalid path.")

def idldir(args, vdir):
    if len(args) < 1:
        print("usage: dd <DIRNAME>")
        return
    path = resvpath(vdir, args[0])
    if path and path.is_dir() and path != ROOT:
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"Error deleting directory: {e}")
    else:
        print("Bad directory or access denied.")

def iview(args, vdir):
    if len(args) < 1:
        print("usage: view <FILENAME>")
        return
    fname = resvpath(vdir, args[0])
    if fname and fname.is_file():
        with open(str(fname)) as f:
            for line in f:
                print(line.rstrip())
    else:
        print("Bad filename.")

def idel(args, vdir):
    if len(args) < 1:
        print("usage: del <FILENAME>")
        return
    fname = resvpath(vdir, args[0])
    if fname and fname.is_file():
        os.remove(fname)
    else:
        print("Bad filename.")

def imove(args, vdir):
    if len(args) < 2:
        print("usage: mv <SOURCE> <DEST>")
        return
    src = resvpath(vdir, args[0])
    dst = resvpath(vdir, args[1])
    if src and dst and src.exists():
        try:
            shutil.move(str(src), str(dst))
        except Exception as e:
            print(f"Error moving file: {e}")
    else:
        print("Invalid source or destination.")

def icopy(args, vdir):
    if len(args) < 2:
        print("usage: cp <SOURCE> <DEST>")
        return
    src = resvpath(vdir, args[0])
    dst = resvpath(vdir, args[1])
    if src and dst and src.is_file():
        try:
            shutil.copy2(str(src), str(dst))
        except Exception as e:
            print(f"Error copying file: {e}")
    else:
        print("Invalid source or destination.")

# exec functions
def execCmd(cmds, vdir):
    for cmd in cmds:
        cmd = cmd.strip()
        if not cmd: continue
                
        # split command
        cmda = shlex.split(cmd)
        name = cmda[0].lower()
        args = cmda[1:]

        # internal
        if name in ["cd", "chdir"]:
            vdir = ichdir(args, vdir)
        elif name in CMDS:
            CMDS[name](args, vdir)
                    
        # external
        else:
            rdir = resvpath(vdir, ".")
            localpy = rdir / f"{name}.py" #type:ignore
            localexe = rdir / f"{name}.exe" #type:ignore
                    
            # local
            if localpy.is_file():
                subprocess.run([sys.executable, str(localpy)] + args)
            elif localexe.is_file():
                subprocess.run([str(localexe)] + args)
                        
            # bin
            else:
                binpy = Path(BIN) / f"{name}.py" #type:ignore
                binexe = Path(BIN) / f"{name}.exe" #type:ignore
                if binpy.is_file():
                    subprocess.run([sys.executable, str(binpy)] + args)
                elif binexe.is_file():
                    subprocess.run([str(binexe)] + args)
                else:
                    print(f"Bad command or file: {name}")

# constants
VER = "v2026.1b"
BIN = "bin/"
CFG = "cfg/"
ROOT = Path(__file__).parent.resolve()
CMDS = {
    "ver": lambda args, vdir: print("AsclepyOS v2026.1"),
    "exit": lambda args, vdir: sys.exit(0),
    "ld": ilsdir, "lsdir": ilsdir,
    "md": imkdir, "mkdir": imkdir,
    "dd": idldir, "dldir": idldir,
    "vw": iview, "view": iview,
    "dl": idel, "del": idel,
    "mv": imove, "move": imove,
    "cp": icopy, "copy": idel,
    "out": lambda args, vdir: print(args[0]),
    "clr": lambda args, vdir: os.system("cls" if os.name == "nt" else "clear"),
    "cont": lambda args, vdir: input("Press enter to continue.")
}

def main():
    # env
    vdir = "/"
    
    # shell loop
    try:
        while True:
            cmds = input(f"~{vdir}> ").split(";")
            execCmd(cmds, vdir)
                            
    # ctrl c
    except KeyboardInterrupt:
        print("Use 'exit' to quit AsclepyOS")

if __name__ == "__main__":
    main()