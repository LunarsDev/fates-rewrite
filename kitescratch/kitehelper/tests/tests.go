package tests

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"

	"github.com/fatih/color"
)

var (
	statusGood       = color.New(color.Bold, color.FgCyan).PrintlnFunc()
	statusSuccess    = color.New(color.Bold, color.FgGreen).PrintlnFunc()
	statusBoldYellow = color.New(color.Bold, color.FgYellow).PrintlnFunc()
	statusBoldErr    = color.New(color.Bold, color.FgRed).PrintlnFunc()
	statusBoldBlue   = color.New(color.Bold, color.FgBlue).PrintlnFunc()
	statusBoldBlueS  = color.New(color.Bold, color.FgBlue).SprintFunc()
	fatal            = func(a ...any) {
		color.New(color.FgRed, color.Bold).PrintlnFunc()(a...)
		os.Exit(1)
	}
)

type test struct {
	name         string
	cmd          []string
	cwd          string
	ignoreErrors string
	customTest   string
}

type testset struct {
	Tests []test
}

func getRepoRoot() string {
	// Use git rev-parse --show-toplevel to get the root of the repo
	out, err := exec.Command("git", "rev-parse", "--show-toplevel").Output()

	if err != nil {
		panic(err)
	}

	return strings.ReplaceAll(string(out), "\n", "")
}

func askInput(question string) string {
	fmt.Print(question)
	scanner := bufio.NewScanner(os.Stdin)

	var opt string

	for scanner.Scan() {
		opt = scanner.Text()
		break
	}

	if scanner.Err() != nil {
		// Handle error.
		fatal(scanner.Err())
	}

	return opt
}

func pageOutput(text string) {
	// Custom pager using less -r
	text = "\n" + text

	cmd := exec.Command("less", "-r")
	cmd.Stdin = strings.NewReader(text)
	cmd.Stdout = os.Stdout
	cmd.Run()
}

func (ts testset) Run() {
	failed := []test{}
	success := []test{}
	outputs := []string{}

	os.Setenv("PATH", os.Getenv("PATH")+":.")
	os.Setenv("FORCE_COLOR", "1")

	for i, t := range ts.Tests {
		err := os.Chdir(getRepoRoot())
		if err != nil {
			panic(err)
		}
		if t.cwd != "" {
			os.Chdir(t.cwd)
		}

		currDir, err := os.Getwd()

		if err != nil {
			panic(err)
		}

		statusGood(t.name, "["+strconv.Itoa(i+1)+"/"+strconv.Itoa(len(ts.Tests))+"] (in", currDir+")")
		if t.customTest != "" {
			// Unpack custom test
			testFile, err := customTests.ReadFile("custom/" + t.customTest)

			if err != nil {
				panic(err)
			}

			os.Mkdir("tmp", 0755)
			os.WriteFile("tmp/"+t.customTest, testFile, 0600)

			t.cmd = append(t.cmd, "tmp/"+t.customTest)
		}

		// Run test here
		cmd := exec.Command(t.cmd[0], t.cmd[1:]...)

		cmd.Env = os.Environ()

		outp, cmdErr := cmd.CombinedOutput()

		outputs = append(outputs, string(outp))

		// Cleanup
		err = os.RemoveAll("tmp")

		if err != nil {
			panic(err)
		}

		if cmdErr != nil {
			if t.ignoreErrors != "" {
				statusBoldErr("Test failed, but ignoring error:", t.ignoreErrors)
				time.Sleep(1 * time.Second)
				success = append(success, t)
				continue
			}
			failed = append(failed, t)

			// Print last 10 lines of output
			lines := strings.Split(string(outp), "\n")

			if len(lines) > 10 {
				lines = lines[len(lines)-10:]
			}

			for _, line := range lines {
				fmt.Println(line)
			}

			statusBoldYellow("Test", t.name, "has failed!")

			var inp string
			if os.Getenv("NO_INTERACTION") == "" {
				inp = askInput("Continue (y/N): ")
			}
			if inp == "y" || inp == "Y" {
				continue
			} else {
				break
			}
		} else {
			success = append(success, t)
		}
	}

	fmt.Println("")

	if len(success) > 0 {
		fmt.Println("")
		statusSuccess("Successful tests:")
		for _, t := range success {
			statusSuccess(t.name, "["+strings.Join(t.cmd, " ")+"]")
		}
	}

	if len(failed) > 0 {
		fmt.Println("")
		statusBoldErr("Failed tests:")
		for _, t := range failed {
			statusBoldErr(t.name, "["+strings.Join(t.cmd, " ")+"]")
		}
	}

	if os.Getenv("NO_INTERACTION") == "" {
		statusBoldBlue("List of all tests:")
		for i, t := range ts.Tests {
			fmt.Println(strconv.Itoa(i+1) + ": " + t.name + " [" + strings.Join(t.cmd, " ") + "]")
		}

		for {
			userOut := askInput(statusBoldBlueS("Which test number would you like to see the output of (hit ENTER to exit): "))

			if userOut != "" {
				num, err := strconv.Atoi(userOut)

				if err != nil {
					statusBoldErr("Invalid input")
					continue
				}

				pageOutput(outputs[num-1])
			} else {
				break
			}
		}
	}
}

func Tester(progname string, args []string) {
	testList.Run()
}
