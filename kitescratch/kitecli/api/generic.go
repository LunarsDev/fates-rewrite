package api

import (
	"kitecli/auth"
	"kitecli/requests"
	"kitecli/types"
	"strconv"
)

func CheckAuthHeader(a *auth.Auth) types.AuthCheck {
	var ac types.AuthCheck

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/@auth",
		Reason: Reason,
		Auth:   a,
	}, &ac)

	return ac
}

func GetIndex(tgtType types.TargetType) types.Index {
	var index types.Index

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/index?target_type=" + strconv.Itoa(int(tgtType)),
		Reason: Reason,
	}, &index)

	return index

}

func RandomSnippet(tgtType types.TargetType, reroll bool) types.Snippet {
	var snip types.Snippet

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/random?target_type=" + strconv.Itoa(int(tgtType)) + "&reroll=" + strconv.FormatBool(reroll),
		Reason: Reason,
	}, &snip)

	return snip
}

func ResolveVanity(code string) types.Vanity {
	var vanity types.Vanity

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/code/" + code,
		Reason: Reason,
	}, &vanity)

	return vanity
}

func GetMeta() types.ListMeta {
	var meta types.ListMeta

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/meta",
		Reason: Reason,
	}, &meta)

	return meta
}

func GetDiscordUser(userId string) types.DiscordUser {
	var user types.DiscordUser

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/blazefire/" + userId,
		Reason: Reason,
	}, &user)

	return user
}

func GetAllPermissions() types.PermissionList {
	var perms types.PermissionList

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/permissions",
		Reason: Reason,
	}, &perms)

	return perms
}

func GetTask(taskId string) any {
	var task any

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/tasks/" + taskId,
		Reason: Reason,
	}, &task)

	return task
}

type SearchData struct {
	Query      string
	GuildCount types.SearchFilter
	Votes      types.SearchFilter
	BotTags    []string
	ServerTags []string
}

func Search(data SearchData) types.SearchResponse {
	body := map[string]any{
		"query":       data.Query,
		"guild_count": data.GuildCount.Map(),
		"votes":       data.Votes.Map(),
		"tags": map[string][]string{
			"bot":    data.BotTags,
			"server": data.ServerTags,
		},
	}

	var resp types.SearchResponse

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "POST",
		Url:    "/search",
		Reason: Reason,
		Data:   body,
	}, &resp)

	return resp
}
