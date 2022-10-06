# In this test, `lint code` refers to the translations within sunbeam src/lib/strings.ts

import sys
sys.path.append(".")

import json
from fates import models

# Open src/lib/strings.ts

with open('sunbeam/src/lib/strings.ts') as f:
    lines = f.readlines()

# Capture all lines from kitescratch-lint-start to kitescratch-lint-end

lint_lines = []

for i, line in enumerate(lines):
    if line.startswith('// kitescratch-lint-start'):
        for j in range(i + 1, len(lines)):
            if lines[j].startswith('// kitescratch-lint-end'):
                break
            lint_lines.append(lines[j])

# Remove all comments just in case

lint_lines = [line for line in lint_lines if not line.startswith('//')]

# Remove all before the equal to sign of first line

lint_lines[0] = lint_lines[0].split('=')[1].replace(" ", "")

# Load the yaml

lint_dict: dict[str, dict[str, str]] = json.loads(''.join(lint_lines))

string_codes = [v for v in list(lint_dict.keys()) if lint_dict[v].get("__ignorable") != "true"]

rc_values = [v.value for v in list(models.ResponseCode)]

for lint_code in string_codes:
    if lint_code.lower() != lint_code:
        raise Exception(f"Lint code {lint_code} is not lowercase")

if rc_values == string_codes:
    # We are golden, exit early
    exit(0)

# string_codes is the source of truth here, all response codes must be in strings.ts

print("For this lint to succeed, the following response codes must be added to models.ResponseCode (replacing already present entities):")

for lint_code in string_codes:
    print(lint_code.upper().replace(".", "_") + " = '" + lint_code + "'")

print("\n\nOr alternatively, add the following keys to strings.ts:")

for lint_code in rc_values:
    if lint_code not in string_codes:
        print("=>",lint_code)

exit(1)