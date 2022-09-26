package api

import (
	"kitescratch/requests"
	"kitescratch/types"
)

func GuppyTest(userId string) types.Permission {
	var perm types.Permission

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/guppy?user_id=" + userId,
		Reason: Reason,
	}, &perm)

	return perm
}
