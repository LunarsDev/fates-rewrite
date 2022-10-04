from subprocess import Popen
class Test:
    def __init__(self, name: str, cmd: list[str]):
        self.name = name
        self.cmd = cmd

class TestControl:
    def __init__(self):
        self.tests: list[Test] = []
    
    def add(self, name: str, cmd: str):
        self.tests.append(Test(name, cmd))
    
    def run(self):
        i = 1
        for test in self.tests:
            print(f"{test.name} [{i}/{len(self.tests)}]")
            code = Popen(test.cmd)

            code = code.wait()

            if code != 0:
                print(f"Test {test.name} failed with code {code}")
                exit(code)
            
            i += 1
    
tester = TestControl()

tester.add("kitescratch_routes_impl.py", ["python3", "tests/kitescratch_routes_impl.py"])

tester.run()