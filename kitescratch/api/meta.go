package api

import (
	"kitescratch/requests"
	"kitescratch/types"
)

func GetMeta() types.ListMeta {
	var meta types.ListMeta

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/meta",
		Reason: Reason,
	}, &meta)

	return meta
}
