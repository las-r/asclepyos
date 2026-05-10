# AsclepyOS
AsclepyOS is a fantasy disk operating system written in Python.

## Installation
```bash
pip install git+https://github.com/las-r/asclepyos.git
```

## Included Commands
### Internal (shell.py)
#### System
- `help`: View contents of README.md
- `ver`: Display OS version
- `exit`: Exit AsclepyOS

#### Files
- `ld`, `lsdir`: List directory contents
- `cd`, `chdir`: Change working directory
- `md`, `mkdir`: Make a new directory
- `dd`, `dldir`: Delete a directory
- `vw`, `view`: View the contents of a file
- `nw`, `new`: Create a new empty file
- `dl`, `del`: Delete a file
- `mv`, `move`: Move a file into another directory
- `cp`, `copy`: Copy the contents of a file into another

#### Data
- `var`: Set a variable
- `num`: Convert a variable to an integer
- `:<VAR>`: Get the value of a variable
- `+<VAL1>,<VAL2>`: Add
- `-<VAL1>,<VAL2>`: Subtract
- `*<VAL1>,<VAL2>`: Multiply
- `/<VAL1>,<VAL2>`: Divide
- `?<MIN>,<MAX>`: Random integer

#### Control Flow and Logic
- `ife`: Run next command only if two values are equal
- `ifn`: Run next command only if two values aren't equal
- `whe`: Run the next command repeated while two values are equal
- `whn`: Run the next command repeated while two values aren't equal

#### I/O
- `out`: Output text
- `in`: Input value into a variable
- `clr`: Clear the console
- `cont`: Pauses process until enter key pressed

#### Misc.
- `com`: Do nothing (comment)

### External (bin/)
- `calc`: Minimal calculator (w/ Python's eval)
- `tex`: Minimal text editor
- `wait`: Basic execution pauser
- `wc`: Line / word / character counter