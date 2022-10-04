package api

import (
	"kitecli/requests"
	"kitecli/types"
)

func CheckUserPermissions(userId string) types.Permission {
	var perm types.Permission

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/users/" + userId + "/permissions",
		Reason: Reason,
	}, &perm)

	return perm
}
