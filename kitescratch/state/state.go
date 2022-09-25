package state

import (
	"flag"
	"os"
)

// Some core global state (to avoid race conditions and millions of parameters)
type State struct {
	BaseURL string
}

func (s State) String() string {
	opts := []string{
		"API URL: " + s.BaseURL,
	}

	var res string
	for _, opt := range opts {
		res += "=> " + opt + "\n"
	}

	return res
}

type Flags struct {
	ShowConfig bool
}

var GlobalFlags Flags
var GlobalState State

func StateInit() {
	GlobalState = State{
		BaseURL: "http://localhost:8000", // Default API URL
	}

	var helpMenu bool

	flag.BoolVar(&GlobalFlags.ShowConfig, "cfg", false, "Allow modifying config options")
	flag.BoolVar(&helpMenu, "help", false, "Show this help menu")
	flag.Parse()

	if helpMenu {
		flag.Usage()
		os.Exit(-1)
	}
}
