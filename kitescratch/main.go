package main

import (
	"fmt"
	"kitescratch/api"
	"kitescratch/state"
	"kitescratch/ui"

	"github.com/sirupsen/logrus"
)

var backupCfg state.State

func init() {
	// Load initial config
	state.StateInit()
	backupCfg = state.GlobalState
}

func cfgSetup() {
	// Ask user if they wish to change any config options
	fmt.Println("\nConfig options currently set:")
	fmt.Println(state.GlobalState.String())

	var changedCfg bool

	ui.AskOption(ui.YesNoPrompt(
		"Do you wish to change any config options?",
		func() error {
			// Yes, ask which option to change

			changedCfg = true

			ui.AskOption(&ui.Prompt{
				Question: "Which option would you like to change?",
				Choices: []*ui.Option{
					{
						ID:   "api-url",
						Text: "API URL",
						Handler: func() error {
							state.GlobalState.BaseURL = ui.AskInput("Enter the new API URL")

							return nil
						},
					},

					// Default choice to restore default config
					{
						ID:   "restore",
						Char: "R",
						Text: "Restore default config",
						Handler: func() error {
							state.GlobalState = backupCfg

							return nil
						},
					},

					// Default choice to do nothing
					{
						ID:   "donothing",
						Char: "E",
						Text: "Return to previous menu",
						Handler: func() error {
							return nil
						},
					},
				},
			})

			return nil
		},
		func() error {
			// No
			logrus.Info("Loading kitescratch...")
			return nil
		},
	))

	if changedCfg {
		cfgSetup()
	}
}

func main() {
	fmt.Println("Welcome to Kitescratch!")

	// Ask user if they wish to change any config options
	if state.GlobalFlags.ShowConfig {
		cfgSetup()
	}

	logrus.SetLevel(logrus.DebugLevel)

	meta := api.GetMeta("Loading index metadata")

	logrus.Info("Loaded ", len(meta.Bot.Tags), " bot tags, ", len(meta.Bot.Features), " bot features and ", len(meta.Server.Tags), " server tags")
}
