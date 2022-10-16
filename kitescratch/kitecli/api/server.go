package api

import (
	"kitecli/requests"
	"kitecli/state"
	"kitecli/types"
)

func GetGuildInvite(guildId string) types.Invite {
	var invite types.Invite

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/guilds/" + guildId + "/invite",
		Reason: Reason,
		Auth:   state.GlobalState.Auth,
	}, &invite)

	return invite
}
