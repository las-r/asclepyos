import os
import sys

# tex: text editor
# included w/ asclepyos
# made by las-r on github

if len(sys.argv) < 2:
    print("usage: tex <filename>")
    sys.exit()

filename = sys.argv[1]

print(f"--- Tex Editor: {filename} ---")
print("Commands: :s = save and exit, :q = quit without saving")
print("-" * (26 + len(filename)))

lines = []

if os.path.exists(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line.rstrip())

while True:
    try:
        userinput = input(f"{len(lines) + 1}: ")

        if userinput == ":s":
            with open(filename, 'w') as f:
                f.writelines(lines)

            print(f"Saved {len(lines)} lines to {filename}.")
            break

        elif userinput == ":q":
            print("Exited without saving.")
            break

        else:
            lines.append(userinput + "\n")

    except EOFError:
        break