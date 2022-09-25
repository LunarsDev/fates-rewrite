package api

import (
	"kitescratch/requests"
	"kitescratch/types"
)

func ResolveVanity(code string) types.Vanity {
	var vanity types.Vanity

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/code/" + code,
		Reason: Reason,
	}, &vanity)

	return vanity
}
