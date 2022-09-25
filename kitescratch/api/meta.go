package api

import (
	"kitescratch/requests"
	"kitescratch/types"
)

func GetMeta(reason string) types.ListMeta {
	var meta types.ListMeta

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/meta",
		Reason: reason,
	}, &meta)

	return meta
}
