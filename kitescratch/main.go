package main

import (
	"encoding/json"
	"kitescratch/requests"
	"kitescratch/types"

	"github.com/sirupsen/logrus"
)

func main() {
	logrus.SetLevel(logrus.DebugLevel)

	output, err := requests.Request(requests.HTTPRequest{
		Method: "GET",
		Url:    "/meta",
	})

	if err != nil {
		logrus.Fatal(err)
	}

	var meta types.ListMeta

	err = json.Unmarshal(output, &meta)

	if err != nil {
		logrus.Fatal(err)
	}

	logrus.Info("Loaded ", len(meta.Bot.Tags), " bot tags, ", len(meta.Bot.Features), " bot features and ", len(meta.Server.Tags), " server tags")
}
