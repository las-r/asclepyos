from pathlib import Path
import sys

# find: search for files by name
# part of asclepyos
# made by las-r on github

def main():
    if len(sys.argv) < 2:
        print("usage: find <pattern>")
        return
    pattern = sys.argv[1]
    matches = list(Path('.').rglob(pattern))
    if matches:
        print(f"--- Results for '{pattern}' ---")
        for match in matches:
            print(match)
    else:
        print(f"No matches found for '{pattern}'.")

if __name__ == "__main__":
    main()