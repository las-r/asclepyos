from pathlib import Path
import os
import random
import re
import shlex
import shutil
import subprocess
import sys

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

def substvars(cmd, var):
    for v, val in var.items():
        cmd = cmd.replace(f":{v}", str(val))
    return cmd

def calc(match):
    op, v1, v2 = match.groups()
    v1, v2 = int(v1), int(v2)
    if op == "+": return str(v1 + v2)
    if op == "-": return str(v1 - v2)
    if op == "*": return str(v1 * v2)
    if op == "/": return str(v1 // v2) if v2 != 0 else "ERR"
    if op == "?": return random.randint(v1, v1)
    return "0"

def solve(cmd, var):
    cmd = substvars(cmd, var)
    pattern = r'([+\-*/])(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)'
    while re.search(pattern, cmd):
        cmd = re.sub(pattern, calc, cmd) #type:ignore
    return cmd

# internal command functions
def ilsdir(args, vdir, _):
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

def ichdir(args, vdir, _):
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

def imkdir(args, vdir, _):
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

def idldir(args, vdir, _):
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

def iview(args, vdir, _):
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

def inew(args, vdir, _):
    if len(args) < 1:
        print("usage: view <FILENAME>")
        return
    fname = resvpath(vdir, args[0])
    if fname and not fname.is_file():
        open(fname, "x").close()
    else:
        print("Bad filename or file already exists.")

def idel(args, vdir, _):
    if len(args) < 1:
        print("usage: del <FILENAME>")
        return
    fname = resvpath(vdir, args[0])
    if fname and fname.is_file():
        os.remove(fname)
    else:
        print("Bad filename.")

def imove(args, vdir, _):
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

def icopy(args, vdir, _):
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

def inum(args, _, var):
    if len(args) < 1:
        print("usage: num <VAR>")
        return
    try:
        var[args[0]] = int(var.get(args[0], 0))
    except ValueError:
        var[args[0]] = 0

# exec functions
def execcmd(cmds, vdir, var):
    skip = False
    idx = 0
    while idx < len(cmds):
        cmd = solve(cmds[idx].strip(), var)
        if not cmd or skip:
            skip = False
            idx += 1
            continue
                
        # split command
        cmda = shlex.split(cmd)
        name = cmda[0].lower()
        args = cmda[1:]
        
        # internal
        if name == "help":
            iview(["~/README.md"], vdir, var)
        elif name == "wle":
            body = cmds[idx + 1:]
            while substvars(args[0], var) == substvars(args[1], var):
                vdir = execcmd(body, vdir, var)
            return vdir
        elif name == "wln":
            body = cmds[idx + 1:]
            while substvars(args[0], var) != substvars(args[1], var):
                vdir = execcmd(body, vdir, var)
            return vdir
        elif name == "ife":
            if substvars(args[0], var) != substvars(args[1], var):
                return execcmd(cmds[idx + 1:], vdir, var)
            return vdir
        elif name == "ifn":
            if substvars(args[0], var) == substvars(args[1], var):
                return execcmd(cmds[idx + 1:], vdir, var)
            return vdir
        elif name in ["cd", "chdir"]:
            vdir = ichdir(args, vdir, var)
        elif name in CMDS:
            CMDS[name](args, vdir, var)
                    
        # external
        else:
            rdir = resvpath(vdir, ".")
            localash = rdir / f"{name}.ash" #type:ignore
            localpy = rdir / f"{name}.py" #type:ignore
            localexe = rdir / f"{name}.exe" #type:ignore
                    
            # local
            if localash.is_file():
                vdir = runash([str(localash)], vdir, var)
            elif localpy.is_file():
                subprocess.run([sys.executable, str(localpy)] + args)
            elif localexe.is_file():
                subprocess.run([str(localexe)] + args)
                        
            # bin
            else:
                binash = Path(BIN) / f"{name}.ash" #type:ignore
                binpy = Path(BIN) / f"{name}.py" #type:ignore
                binexe = Path(BIN) / f"{name}.exe" #type:ignore
                if binash.is_file():
                    vdir = runash([str(binash)], vdir, var)
                elif binpy.is_file():
                    subprocess.run([sys.executable, str(binpy)] + args)
                elif binexe.is_file():
                    subprocess.run([str(binexe)] + args)
                else:
                    print(f"Bad command or file: {name}")
        idx += 1
    return vdir

# ash script
def runash(args, vdir, var):
    if len(args) < 1:
        print("usage: ash <SCRIPT.ASH>")
        return vdir
    scriptpath = resvpath(vdir, args[0])
    if scriptpath and scriptpath.is_file():
        with open(scriptpath, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            return execcmd(lines, vdir, var)
    else:
        print("Script not found.")
        return vdir

# constants
VER = "v2026.1b"
BIN = "bin/"
CFG = "cfg/"
ROOT = Path(__file__).parent.resolve()
CMDS = {
    "ver": lambda _, __, ___: print("AsclepyOS v2026.1"),
    "exit": lambda _, __, ___: sys.exit(0),
    "ld": ilsdir, "lsdir": ilsdir,
    "md": imkdir, "mkdir": imkdir,
    "dd": idldir, "dldir": idldir,
    "vw": iview, "view": iview,
    "nw": inew, "new": inew,
    "dl": idel, "del": idel,
    "mv": imove, "move": imove,
    "cp": icopy, "copy": icopy,
    "var": lambda args, _, var: var.update({args[0]: args[1]}),
    "num": inum,
    "out": lambda args, _, __: print(args[0]),
    "in": lambda args, _, var: var.update({args[0]: input(args[1])}),
    "clr": lambda _, __, ___: os.system("cls" if os.name == "nt" else "clear"),
    "cont": lambda _, __, ___: input("\nPress enter to continue... "),
    "com": lambda _, __, ___: True
}

def main():
    # env
    vdir = "/"
    var = {}
    
    # shell loop
    try:
        while True:
            cmds = input(f"~{vdir}> ").split(";")
            vdir = execcmd(cmds, vdir, var)
                                
    # ctrl c
    except KeyboardInterrupt:
        print("Use 'exit' to quit AsclepyOS")

if __name__ == "__main__":
    main()