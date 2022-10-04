package api

import (
	"kitecli/requests"
	"kitecli/state"
	"kitecli/types"
)

func PerformDataAction(userId string, mode types.DataAction) types.DataResponse {
	var dr types.DataResponse

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "POST",
		Url:    "/data?user_id=" + userId + "&mode=" + string(mode),
		Reason: Reason,
		Data:   mode,
		Auth:   state.GlobalState.Auth,
	}, &dr)

	return dr
}
