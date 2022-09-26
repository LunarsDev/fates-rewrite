package api

import (
	"kitescratch/requests"
	"kitescratch/types"
	"strconv"
)

func RandomSnippet(tgtType types.TargetType, reroll bool) types.Snippet {
	var snip types.Snippet

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/random?target_type=" + strconv.Itoa(int(tgtType)) + "&reroll=" + strconv.FormatBool(reroll),
		Reason: Reason,
	}, &snip)

	return snip
}
