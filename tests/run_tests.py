#!/usr/bin/env python3

from calendar import c
from subprocess import Popen
import os

curr_dir = os.getcwd()

class Test:
    def __init__(
        self, 
        name: str, 
        cmd: list[str], 
        *, 
        cwd: str | None = None,
        ignore_errors: str | None = None,
    ):
        self.name = name
        self.cmd = cmd
        self.cwd = cwd or curr_dir
        self.ignore_errors = ignore_errors
    
    def __str__(self):
        return f"Test {self.name} (cmd=\"{' '.join(self.cmd)}\")"
    
    def __repr__(self):
        return self.__str__()

class TestControl:
    def __init__(self):
        self.tests: list[Test] = []
        self.failed = []
    
    def add(self, name: str, cmd: str, *, cwd: str | None = None, ignore_errors: str | None = None):
        self.tests.append(Test(name, cmd, cwd=cwd, ignore_errors=ignore_errors))
    
    def failcode(self) -> int:
        return 1 if len(self.failed) > 0 else 0

    def exit(self):
        if len(self.failed) > 0:
            tests_str = "\n=> " + "\n=> ".join([str(v) for v in self.failed])

            print("Exiting with code", self.failcode(), "\nTests that unexpectedly failed:", tests_str)
        
        exit(self.failcode())

    def run(self):
        i = 1
        for test in self.tests:
            os.chdir(curr_dir)
            print(f"{test.name} [{i}/{len(self.tests)}]")
            os.chdir(test.cwd)

            try:
                code = Popen(test.cmd)
                code = code.wait()
            except (BaseException, Exception) as e:
                print(f"Failed to run test {test.name}: {type(e).__name__} {e}")
                code = 1
            
            if code != 0 and test.ignore_errors is not None:
                print("Ignoring error because:", test.ignore_errors)

            elif code != 0:
                print(f"Test {test.name} failed with code {code}")
                self.failed.append(test)
                continue_test = input("Continue? [y/N] ")
                if continue_test.lower() in ("y", "yes"):
                    i += 1
                    continue
                tester.exit()
            
            i += 1
    
tester = TestControl()

tester.add("kitescratch_routes_impl.py", ["python3", "tests/kitescratch_routes_impl.py"])
tester.add("sunbeam (format)", ["npm", "run", "format"], cwd="sunbeam")
tester.add("sunbeam (lint)", ["npm", "run", "lint-fix"], cwd="sunbeam", ignore_errors="Still initial stages of the rewrite")
tester.add("fates (black)", ["black", "fates"])


tester.run()

tester.exit()
