package ui

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"github.com/fatih/color"
)

var BoldText = color.New(color.Bold).PrintlnFunc()
var BlueText = color.New(color.FgBlue).PrintlnFunc()
var RedText = color.New(color.FgRed).PrintlnFunc()

type OptionHandler = func() error

type Option struct {
	ID      string        // The ID of the Option
	Char    string        // The character to press to select this Option, leave empty to use numbers
	Text    string        // The text to display
	Handler OptionHandler // The function to call when this Option is selected
}

type Prompt struct {
	Question string // The question to ask
	Choices  []*Option
	Timeout  time.Duration // The time to wait for a choice to be made
}

func (p *Prompt) IsOption(ch string) bool {
	for _, option := range p.Choices {
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
				ID:      "yes",
				Char:    "Y",
				Text:    "Yes",
				Handler: f1,
			},
			{
				ID:      "no",
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
	for i, option := range p.Choices {
		if option.Char == "" {
			newChar := strconv.Itoa(i + 1)
			option.Char = newChar
		}

		BoldText(option.Char+".", option.Text)
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
		log.Fatal(scanner.Err())
	}

	for _, option := range p.Choices {
		if option.Char == opt {
			err := option.Handler()

			if err != nil {
				log.Fatal(err)
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
		log.Fatal(scanner.Err())
	}

	return opt
}
