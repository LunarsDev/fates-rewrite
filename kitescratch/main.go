package main

import (
	"context"
	"fmt"
	"kitescratch/api"
	"kitescratch/state"
	"kitescratch/ui"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/sirupsen/logrus"
)

var (
	backupCfg state.State
	loginCh   = make(chan iLogin)
)

type iLogin struct {
	code  string
	state string
}

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
						Text: "API URL",
						Handler: func() error {
							state.GlobalState.BaseURL = ui.AskInput("Enter the new API URL")

							return nil
						},
					},

					// Default choice to restore default config
					{
						Char: "R",
						Text: "Restore default config",
						Handler: func() error {
							state.GlobalState = backupCfg

							return nil
						},
					},

					// Default choice to do nothing
					{
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

func indexView() {
	api.SetReason("Loading index metadata")
	meta := api.GetMeta()

	logrus.Info("Loaded ", len(meta.Bot.Tags), " bot tags, ", len(meta.Bot.Features), " bot features and ", len(meta.Server.Tags), " server tags")

	ui.BoldText("Bot Tags")
	for i, tag := range meta.Bot.Tags {
		ui.YellowText(strconv.Itoa(i+1)+".", tag.String())
	}

	ui.BoldText("Bot Features")
	for i, feature := range meta.Bot.Features {
		ui.PurpleText(strconv.Itoa(i+1)+".", feature.String())
	}

	ui.BoldText("Server Tags")
	for i, tag := range meta.Server.Tags {
		ui.BlueText(strconv.Itoa(i+1)+".", tag.String())
	}
}

func vanityView() {
	code := ui.AskInput("Enter the vanity to resolve")
	api.SetReason("Resolving vanity on user request")
	vanity := api.ResolveVanity(code)

	if vanity.TargetID == "" {
		ui.RedText("Vanity not found")
	} else {
		ui.GreenText("Vanity resolved to", vanity.TargetID, "["+vanity.TargetType.String()+"]")
	}
}

func loginView() {
	// Get oauth2 url
	api.SetReason("Fetching login URL for loginView")
	oauth2 := api.GetOauth2("http://localhost:5001")

	// Open a http server on port 5001
	srv := &http.Server{Addr: ":5001"}

	go func() {
		err := srv.ListenAndServe()
		if err != http.ErrServerClosed {
			log.Fatal(err)
		}
	}()

	fmt.Println("Please open the following URL in your browser:\n\n", oauth2.Url+"&state="+oauth2.State)

	// Wait for login
	login := <-loginCh

	fmt.Println("Got login code", login.code, "with state", login.state)

	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)

	srv.Shutdown(ctx)

	cancel()

	// Exchange code for token via fates api endpoint

	// RN, only do a normal auth, frostpaw auth is *NOT* needed
	api.SetReason("Exchanging login code for token")
	token := api.LoginUser("http://localhost:5001", api.LoginUserData{
		Code:  login.code,
		State: login.state,
	})

	fmt.Println("Got user token", token.Token)
}

func mainMenu() {
	for {
		var exit bool
		ui.AskOption(&ui.Prompt{
			Question: "What would you like to do?",
			Choices: []*ui.Option{
				{
					Text: "View index",
					Char: "I",
					Handler: func() error {
						indexView()
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
					Text: "CMD View",
					Char: "C",
					Handler: func() error {
						cmdView()
						return nil
					},
				},
				{
					Text: "Login",
					Char: "L",
					Handler: func() error {
						loginView()
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
			},
		})

		if exit {
			return
		}
	}
}

func main() {
	fmt.Println("Welcome to Kitescratch!")

	// Ask user if they wish to change any config options
	if state.GlobalFlags.ShowConfig {
		cfgSetup()
	}

	logrus.SetLevel(logrus.DebugLevel)

	mainMenu()
}
