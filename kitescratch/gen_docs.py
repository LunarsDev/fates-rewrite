import os, shutil

def get_docstring(l: list[str], start: int) -> tuple[int, str]:
    """
    Gets the docstring for a class or class attribute

    For a class, the docstring is the first line after the class definition
    For a class attribute, the docstring is the first line after the attribute definition

    Args:
        l (list[str]): The lines of the file
        start (int): The line number of the class or attribute definition

    Returns:
        tuple[int, str]: The line number of the docstring and the docstring
    """
    start += 1 # Skip the class or attribute definition
    if l[start].count('"""') == 0:
        return 0, ""
    # Handle same line case
    if l[start].count('"""') == 2:
        s = l[start].split('"""')[1]
        return start, s

    s = ""

    print("DEBUG: two line case")

    for i in range(start, len(l)):
        print(l[i])
        s += l[i] + "\n"
        if i == start:
            # Not possible anyways, go on with continue
            continue
        if '"""' in l[i]:
            return i, s.replace('"""', "").strip()

    return 0, ""

def class_inherits(l: list[str], start: int) -> list[str]:
    """
    Gets the classes that a class inherits from

    Args:
        l (list[str]): The lines of the file
    
    Returns:
        list[str]: The classes that the class inherits from
    """
    if "(" not in l[start]:
        return []

    for i in range(start, len(l)):
        if l[i].startswith("class "):
            p_vals = l[i].split("(")[1].replace("):", "").split(", ")

            vals = []
            for v in p_vals:
                if "#" in v:
                    vals.append(v.split("#")[0].strip())
                    return vals
                vals.append(v)
            return vals

    return []



# Open file ``fates/models.py`` and split it into list
with open("fates/models.py", "r") as f:
    lines = f.read().splitlines()

# Parsing needs a few extra lines free right now
lines.append("")
lines.append("")
lines.append("")

model_docs = """
# Models

This page contains the models used in the API.
"""

got_s = False

# Iterate through the lines
for line in lines:
    if "kitescratch-begin" in line:
        got_s = True
        continue

    if not got_s:
        continue
    # If the line is a class definition
    if line.startswith("class"):
        print(f"gen_docs: adding {line}")
        # Get the immediate class inheritance chain
        classes = "\n".join([f"- [{v}](#{v.lower()})" for v in class_inherits(lines, lines.index(line))])

        # Get the class name
        name = (line.split("(")[0] if "(" in line else line.replace(":", "")).replace("class ", "")

        # Get the docstring
        docstring_line, docstring = get_docstring(lines, lines.index(line))
        print(f"gen_docs: docstring: {docstring} for {name}")

        # Add the class name and docstring to the docs
        model_docs += f"""
## {name}

{docstring}

**Inherits**

{classes}

**Attributes:**
"""

        # Iterate through the lines after the class definition
        skip = 0
        for line in lines[docstring_line + 1 :]:
            if skip:
                skip -= 1
                continue

            # If the line is an attribute definition
            if "kitescratch-end" in line:
                break
            if line.startswith("    \"\"\""):
                print(line)

                docstring_line, docstring = get_docstring(lines, lines.index(line))

                if docstring_line == 0:
                    skip = 0
                    continue

                skip = docstring_line - lines.index(line)
                continue          

            if (line.startswith("    ") or line.startswith("\t")) and ':' in line:
                # Get the attribute name
                attr_name = line

                # Get the docstring
                docstring_line, docstring = get_docstring(lines, lines.index(line))

                # Add the attribute name and docstring to the docs
                model_docs += f"""
**{attr_name.strip()}**

{docstring}
"""

with open("backend_assets/models.kitescratch", "w") as f:
    f.write(model_docs)

#print(model_docs)