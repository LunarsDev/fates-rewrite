package api

import (
	"kitecli/requests"
	"kitecli/state"
	"kitecli/types"
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

func VerifyClientId(clientId string) types.BotAddTicket {
	var ticket types.BotAddTicket

	requests.RequestToStruct(requests.HTTPRequest{
		Method:                     "POST",
		Url:                        "/bots/add/verify-client-id?client_id=" + clientId,
		Reason:                     Reason,
		StructMarshalErrorContinue: true,
		Auth:                       state.GlobalState.Auth,
	}, &ticket)

	return ticket
}

func FinalizeBotAdd(data types.BotAddFinalize) types.Response {
	var response types.Response

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "POST",
		Url:    "/bots/add/finalize",
		Reason: Reason,
		Auth:   state.GlobalState.Auth,
		Data:   data,
	}, &response)

	return response
}
