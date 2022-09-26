package ui

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
	BoldText   = color.New(color.Bold).PrintlnFunc()
	BlueText   = color.New(color.FgBlue).PrintlnFunc()
	RedText    = color.New(color.FgRed).PrintlnFunc()
	YellowText = color.New(color.FgYellow).PrintlnFunc()
	PurpleText = color.New(color.FgMagenta).PrintlnFunc()
	GreenText  = color.New(color.FgGreen).PrintlnFunc()
	NormalText = color.New(color.FgWhite).PrintlnFunc()
	OrangeText = color.New(color.FgHiRed).PrintlnFunc()
	FatalText  = func(a ...any) {
		color.New(color.FgRed, color.Bold).PrintlnFunc()(a...)
		os.Exit(1)
	}
	BoldBlueText = color.New(color.FgBlue, color.Bold).PrintlnFunc()

	// Sprint version of the above
	BoldTextS     = color.New(color.Bold).SprintlnFunc()
	BlueTextS     = color.New(color.FgBlue).SprintlnFunc()
	RedTextS      = color.New(color.FgRed).SprintlnFunc()
	YellowTextS   = color.New(color.FgYellow).SprintlnFunc()
	PurpleTextS   = color.New(color.FgMagenta).SprintlnFunc()
	GreenTextS    = color.New(color.FgGreen).SprintlnFunc()
	NormalTextS   = color.New(color.FgWhite).SprintlnFunc()
	OrangeTextS   = color.New(color.FgHiRed).SprintlnFunc()
	BoldBlueTextS = color.New(color.Bold, color.FgBlue).SprintlnFunc()
)

func RandomColorFunc() func(a ...any) {
	return color.New(color.FgHiBlack + color.Attribute(time.Now().UnixNano()%6)).PrintlnFunc()
}

func RandomColor(a ...any) {
	RandomColorFunc()(a...)
}

type OptionHandler = func() error

type Option struct {
	Char        string        // The character to press to select this Option, leave empty to use numbers
	Text        string        // The text to display
	Handler     OptionHandler // The function to call when this Option is selected
	Spanner     bool          // Whether this option is just a dummy spanner to make a list look nicer
	SpannerShow bool          // Whether to show this spanner or if it should just be a blank line
	SpannerFunc func(...any)  // The function to call for printing the spanner
}

type Prompt struct {
	Question string // The question to ask
	Choices  []*Option
	Timeout  time.Duration // The time to wait for a choice to be made
}

func (p *Prompt) IsOption(ch string) bool {
	for _, option := range p.Choices {
		if option.Spanner {
			continue
		}
		if option.Char == ch {
			return true
		}
	}
	return false
}

func YesNoPrompt(question string, f1 OptionHandler, f2 OptionHandler) *Prompt {
	return &Prompt{
		Question: question,
		Choices: []*Option{
			{
				Char:    "Y",
				Text:    "Yes",
				Handler: f1,
			},
			{
				Char:    "N",
				Text:    "No",
				Handler: f2,
			},
		},
	}
}

// AskOption asks the user to select an option from a list of options
func AskOption(p *Prompt) {
	BlueText(p.Question)

	var prevLen int
	for i, option := range p.Choices {
		if option.Spanner {
			// This is just a spanner to make the list look nicer
			if option.SpannerShow {
				var spFunc = GreenText
				if option.SpannerFunc != nil {
					spFunc = option.SpannerFunc
				}

				spFunc(strings.Repeat("=", prevLen))
				fmt.Println()
			} else {
				fmt.Println()
				fmt.Println()
			}
			continue
		}

		if option.Char == "" {
			newChar := strconv.Itoa(i + 1)
			option.Char = newChar
		}

		BoldText(option.Char+".", option.Text)

		prevLen = len(option.Char) + len(option.Text) + 2
	}

	fmt.Print("Select an option: ")

	// Wait for input
	scanner := bufio.NewScanner(os.Stdin)

	var opt string

	for scanner.Scan() {
		opt = scanner.Text()
		if !p.IsOption(opt) {
			RedText("Invalid option (" + opt + ")")
			fmt.Print("Select an option: ")
		} else {
			break
		}
	}

	if scanner.Err() != nil {
		// Handle error.
		FatalText(scanner.Err())
	}

	for _, option := range p.Choices {
		if option.Char == opt {
			if option.Handler == nil {
				RedText("No handler for option", opt)
				fmt.Println("")
				return
			}

			err := option.Handler()

			if err != nil {
				RedText(err)
				return
			}
			break
		}
	}
}

func AskInput(question string) string {
	fmt.Print(question + ": ")
	scanner := bufio.NewScanner(os.Stdin)

	var opt string

	for scanner.Scan() {
		opt = scanner.Text()
		break
	}

	if scanner.Err() != nil {
		// Handle error.
		FatalText(scanner.Err())
	}

	return opt
}

func PageOutput(text string) {
	// Custom pager using less -r
	text = BoldTextS("") + text

	cmd := exec.Command("less", "-r")
	cmd.Stdin = strings.NewReader(text)
	cmd.Stdout = os.Stdout
	cmd.Run()
}
