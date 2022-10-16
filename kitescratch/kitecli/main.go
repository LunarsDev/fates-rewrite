package main

import (
	"fmt"
	"kitecli/state"
	"kitecli/ui"
	"net/http"
	"time"
)

var (
	backupCfg state.State
	loginCh   = make(chan iLogin)
)

func init() {
	// Load initial config
	state.StateInit()
	backupCfg = state.GlobalState

	// Load login webserver
	http.HandleFunc("/frostpaw/login", func(w http.ResponseWriter, r *http.Request) {
		code := r.URL.Query().Get("code")
		state := r.URL.Query().Get("state")

		w.Write([]byte("You can now close this window"))

		loginCh <- iLogin{
			code:  code,
			state: state,
		}
	})
}

func _prepend[T any](s []T, v ...T) []T {
	// Prepend v to start of s
	return append(v, s...)
}

func mainMenu() {
	for {
		var exit bool

		var authOpts []*ui.Option
		if state.GlobalState.Auth == nil {
			authOpts = []*ui.Option{
				{
					Char: "L",
					Text: "Login",
					Handler: func() error {
						loginView()
						return nil
					},
				},
			}
		} else {
			authOpts = []*ui.Option{
				{
					Char: "L",
					Text: "Logout [Logged in as " + state.GlobalState.Auth.AuthExt.User.Username + "]",
					Handler: func() error {
						state.GlobalState.Auth = nil
						ui.GreenText("Logged out")
						return nil
					},
				},
				{
					Char: "VA",
					Text: "Verify Auth With API",
					Handler: func() error {
						checkAuthView()
						return nil
					},
				},
				{
					Char: "ADD",
					Text: "Add Bot",
					Handler: func() error {
						addBotView()
						return nil
					},
				},
			}
		}

		choices := []*ui.Option{
			// Spanner for the actual choices
			{
				Spanner:     true,
				SpannerShow: true,
			},
			{
				Text: "View index",
				Char: "I",
				Handler: func() error {
					indexMetaView()
					return nil
				},
			},
			{
				Text: "Resolve a vanity",
				Char: "RV",
				Handler: func() error {
					vanityView()
					return nil
				},
			},
			{
				Text: "Fetch a user's information",
				Char: "FU",
				Handler: func() error {
					viewUserView()
					return nil
				},
			},
			{
				Text: "Check a users permissions",
				Char: "CUP",
				Handler: func() error {
					checkUserPermsView()
					return nil
				},
			},
			{
				Text: "Fetch all list permissions",
				Char: "FLP",
				Handler: func() error {
					listPermsView()
					return nil
				},
			},
			{
				Text: "Fetch a task",
				Char: "FT",
				Handler: func() error {
					viewTaskView()
					return nil
				},
			},
			{
				Text: "Perform a data action",
				Char: "PDA",
				Handler: func() error {
					dataActionView()
					return nil
				},
			},
			{
				Text: "Search List",
				Char: "SL",
				Handler: func() error {
					searchView()
					return nil
				},
			},
			{
				Text: "Fetch a bot",
				Char: "FB",
				Handler: func() error {
					viewBotView()
					return nil
				},
			},
			{
				Text: "Fetch a bot's invite",
				Char: "FBI",
				Handler: func() error {
					viewBotInvView()
					return nil
				},
			},
			{
				Text: "Fetch a bot's secrets",
				Char: "FBS",
				Handler: func() error {
					viewBotSecretsView()
					return nil
				},
			},
			{
				Text: "Fetch a server's invite",
				Char: "FSI",
				Handler: func() error {
					guildInviteView()
					return nil
				},
			},
			{
				Text: "Check config",
				Char: "C",
				Handler: func() error {
					cfgSetup()
					return nil
				},
			},
			{
				Text: "Exit",
				Char: "E",
				Handler: func() error {
					exit = true
					return nil
				},
			},
		}

		choices = _prepend(choices, authOpts...)

		ui.AskOption(&ui.Prompt{
			Question: "What would you like to do?",
			Choices:  choices,
		})

		if exit {
			return
		}

		time.Sleep(1 * time.Second)
	}
}

func main() {
	fmt.Println("Welcome to Kitescratch!")

	// Ask user if they wish to change any config options
	if state.GlobalFlags.ShowConfig {
		cfgSetup()
	}

	mainMenu()
}
