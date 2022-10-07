package api

import (
	"kitecli/requests"
	"kitecli/types"
)

func GetOauth2(frostpawServer string) types.Oauth2 {
	var meta types.Oauth2

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/oauth2",
		Reason: Reason,
		Headers: map[string][]string{
			"Frostpaw-Server": {frostpawServer},
		},
	}, &meta)

	return meta
}

type LoginUserData struct {
	Code string `json:"code"`
}

func LoginUser(frostpawServer string, d LoginUserData) types.OauthUser {
	var ou types.OauthUser

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "POST",
		Url:    "/oauth2",
		Reason: Reason,
		Data:   d,
		Headers: map[string][]string{
			"Frostpaw-Server": {frostpawServer},
		},
	}, &ou)

	return ou
}
