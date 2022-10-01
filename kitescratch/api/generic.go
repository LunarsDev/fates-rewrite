package api

import (
	"kitescratch/auth"
	"kitescratch/requests"
	"kitescratch/types"
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
