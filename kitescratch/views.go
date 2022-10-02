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

type iLogin struct {
	code  string
	state string
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

	index := api.GetIndex(types.TargetTypeBot)

	// TODO: Add servers once thats implemented

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

	outputStr += ui.BoldTextS("Bot Index [New]")

	for _, bot := range index.New {
		outputStr += renderers.Snippet(bot)
	}

	outputStr += ui.BoldTextS("Bot Index [Top Voted]")

	for _, bot := range index.TopVoted {
		outputStr += renderers.Snippet(bot)
	}

	outputStr += ui.BoldTextS("Bot Index [Certified]")

	for _, bot := range index.Certified {
		outputStr += renderers.Snippet(bot)
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
		Code: login.code,
	})

	ui.GreenText("\nAuth Done!")
	ui.PurpleText("User ID:", token.User.ID, "\nUsername:", token.User.Username, "\nUser Token:", token.Token)

	ui.BlueText("\nUser Permissions\nIndex:", token.Permissions.Index, "\nRoles:", token.Permissions.Roles, "\nName:", token.Permissions.Name)

	state.GlobalState.Auth = &auth.Auth{
		Token:      token.Token,
		ID:         token.User.ID,
		TargetType: types.AuthTargetTypeUser,
		AuthExt:    token,
	}
}

func checkUserPermsView() {
	// Get user ID
	userId := ui.AskInput("Enter the user ID to check")

	// Get user perms
	api.SetReason("Fetching user perms")
	perms := api.CheckUserPermissions(userId)

	// Output perms
	ui.GreenText("User", userId, "has the following permission:\nName:", perms.Name, "\nRoles:", perms.Roles, "\nIndex (value):", perms.Index)
}

func viewUserView() {
	// Get user ID
	userId := ui.AskInput("Enter the user ID to view")

	// Get user
	api.SetReason("Fetching user")
	user := api.GetDiscordUser(userId)

	// Output user

	/*
		ID            string     `json:"id"`
		Username      string     `json:"username"`
		Discriminator string     `json:"disc"`
		Avatar        string     `json:"avatar"`
		Bot           bool       `json:"bot"`
		System        bool       `json:"system"`
		Status        UserStatus `json:"status"`
		Flags         int        `json:"flags"`

	*/

	ui.GreenText("User", userId, "has the following information:\nUsername:", user.Username+"#"+user.Discriminator, "\nAvatar:", user.Avatar, "\nBot:", user.Bot, "\nSystem:", user.System, "\nStatus:", user.Status, "\nFlags:", user.Flags)
}

func listPermsView() {
	perms := api.GetAllPermissions()

	ui.GreenText("Loaded", len(perms.Perms), "permissions")

	var outputStr string

	for name, perm := range perms.Perms {
		outputStr += ui.BlueTextS(name, "-", perm.Name, " (index:", perm.Index, "\nRoles:", perm.Roles)
	}

	ui.GreenText(outputStr)
}

func viewTaskView() {
	// Get task ID
	taskId := ui.AskInput("Enter the task ID to view")

	// Get task
	api.SetReason("Fetching task")
	task := api.GetTask(taskId)

	ui.BlueText(task)
}
