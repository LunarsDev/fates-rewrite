package api

import (
	"kitescratch/requests"
	"kitescratch/state"
	"kitescratch/types"
)

func GetBot(botId string) map[string]any {
	var bot map[string]any

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/bots/" + botId,
		Reason: Reason,
	}, &bot)

	return bot
}

func GetBotInvite(botId string) types.Invite {
	var invite types.Invite

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/bots/" + botId + "/invite",
		Reason: Reason,
	}, &invite)

	return invite
}

func GetBotSecrets(botId string) types.BotSecrets {
	var secrets types.BotSecrets

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/bots/" + botId + "/secrets",
		Reason: Reason,
		Auth:   state.GlobalState.Auth,
	}, &secrets)

	return secrets
}
