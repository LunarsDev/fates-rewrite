package api

import (
	"kitescratch/requests"
	"kitescratch/types"
	"strconv"
)

func GetIndex(tgtType types.TargetType) types.Index {
	var index types.Index

	requests.RequestToStruct(requests.HTTPRequest{
		Method: "GET",
		Url:    "/index?target_type=" + strconv.Itoa(int(tgtType)),
		Reason: Reason,
	}, &index)

	return index

}
