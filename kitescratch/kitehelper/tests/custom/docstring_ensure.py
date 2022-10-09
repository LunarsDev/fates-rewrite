"""Ensures that docstrings are present for all functions and classes."""

import os

class State:
    def __init__(self):
        self.will_err = False

state = State()

def ensure_docstrings(path: str, ignore: list[str] = [], ignore_dirs: list[str] = []):
    for root, _, files in os.walk(path):
        if root in ignore_dirs:
            continue
        for file in files:
            if file.endswith(".py") and file not in ignore:
                with open(os.path.join(root, file), "r") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        line = line.strip().replace("\t", "").replace("    ", "")
                        if (
                            line.startswith("async def") or line.startswith("def ") or line.startswith("class ")
                        ) and not line.startswith("def __init__") and not line.endswith("--ignore-docstrings"):
                            j = 0

                            while True:
                                if lines[i + j].split("#")[0].strip().endswith(":"):
                                    j += 1
                                    break
                                else:
                                    j += 1

                            next_line = lines[i + j].strip().replace("\t", "").replace("    ", "")
                            if not next_line.startswith('"""') and not next_line.endswith("--ignore-docstrings"):
                                print("Missing docstring for {} in {}".format(line.strip(), file))
                                state.will_err = True


ensure_docstrings("fates", ["tables.py"], ["fates/piccolo_migrations"])
ensure_docstrings("silverpelt")

if state.will_err:
    exit(1)