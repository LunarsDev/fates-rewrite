package main

import (
	"context"
	"fmt"
	"kitescratch/api"
	"kitescratch/auth"
	"kitescratch/renderers"
	"kitescratch/state"
	"kitescratch/types"
	"kitescratch/ui"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"
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
					{
						Text: "Auth",
						Handler: func() error {
							ui.AskOption(ui.YesNoPrompt(
								"Do you have a auth header value already?",
								func() error {
									// Yes, ask for auth header
									authHeader := ui.AskInput("Enter the auth header value")

									authSplit := strings.Split(authHeader, "|")

									if len(authSplit) != 3 {
										return fmt.Errorf("invalid auth header format")
									}

									var tgtType types.AuthTargetType
									switch authSplit[0] {
									case "user":
										tgtType = types.AuthTargetTypeUser
									case "bot":
										tgtType = types.AuthTargetTypeBot
									case "server":
										tgtType = types.AuthTargetTypeServer
									default:
										ui.RedText("invalid auth target type")
										return nil
									}

									state.GlobalState.Auth = &auth.Auth{
										TargetType: tgtType,
										ID:         authSplit[1],
										Token:      authSplit[2],
										AuthExt: types.OauthUser{
											User: types.DiscordUser{
												ID:       authSplit[1],
												Username: authSplit[1] + " (unknown user)",
											},
										},
									}
									return nil
								},
								func() error {
									targetType := ui.AskInput("Enter the auth target type (user, bot, server)")

									var tgtType types.AuthTargetType
									switch targetType {
									case "user":
										tgtType = types.AuthTargetTypeUser
									case "bot":
										tgtType = types.AuthTargetTypeBot
									case "server":
										tgtType = types.AuthTargetTypeServer
									default:
										ui.RedText("invalid auth target type")
										return nil
									}

									targetId := ui.AskInput("Enter the auth target ID")

									token := ui.AskInput("Enter the auth token")

									state.GlobalState.Auth = &auth.Auth{
										TargetType: tgtType,
										ID:         targetId,
										Token:      token,
										AuthExt: types.OauthUser{
											User: types.DiscordUser{
												ID:       targetId,
												Username: targetId + " (unknown user)",
											},
										},
									}

									return nil
								},
							))

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
			ui.NormalText("Loading kitescratch...")
			return nil
		},
	))

	if changedCfg {
		cfgSetup()
	}
}

func indexMetaView() {
	api.SetReason("Loading index metadata")
	meta := api.GetMeta()

	api.SetReason("Fetching random bot snippet")
	snippet := api.RandomSnippet(types.TargetTypeBot, false)

	var outputStr string

	ui.OrangeText("Loaded", len(meta.Bot.Tags), "bot tags,", len(meta.Bot.Features), "bot features and", len(meta.Server.Tags), "server tags")

	outputStr += ui.BoldTextS("Random Bot")

	outputStr += renderers.Snippet(snippet)

	outputStr += ui.BoldTextS("Bot Tags")
	for i, tag := range meta.Bot.Tags {
		outputStr += ui.BlueTextS(strconv.Itoa(i+1)+".", tag.String())
	}

	outputStr += ui.BoldTextS("Bot Features")
	for i, feature := range meta.Bot.Features {
		outputStr += ui.GreenTextS(strconv.Itoa(i+1)+".", feature.String())
	}

	outputStr += ui.BoldTextS("Server Tags")
	for i, tag := range meta.Server.Tags {
		outputStr += ui.PurpleTextS(strconv.Itoa(i+1)+".", tag.String())
	}

	ui.PageOutput(outputStr)
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

	ui.GreenText("Please open the following URL in your browser:\n")
	ui.BoldText(oauth2.String())

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

	ui.GreenText("\nAuth Done!")
	ui.PurpleText("User ID:", token.User.ID, "\nUsername:", token.User.Username, "\nUser Token:", token.Token)

	state.GlobalState.Auth = &auth.Auth{
		Token:      token.Token,
		ID:         token.User.ID,
		TargetType: types.AuthTargetTypeUser,
		AuthExt:    token,
	}
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
