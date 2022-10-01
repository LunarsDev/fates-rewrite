package api

import (
	"kitescratch/requests"
	"kitescratch/types"
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
	Code                     string `json:"code"`
	Frostpaw                 bool   `json:"frostpaw"`                    // Custom client or not
	FrostpawBlood            string `json:"frostpaw_blood"`              // The custom client's ID
	FrostpawClaw             string `json:"frostpaw_claw"`               // The custom client's secret
	FrostpawClawUnseatheTime int64  `json:"frostpaw_claw_unseathe_time"` // The time the custom client's request was sent, used as a nonce
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
