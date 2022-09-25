package state

import (
	"flag"
	"kitescratch/auth"
	"os"
)

// Some core global state (to avoid race conditions and millions of parameters)
type State struct {
	BaseURL string
	Auth    *auth.Auth
}

func (s State) String() string {
	authStr := "Not Logged In"
	if s.Auth != nil {
		authStr = s.Auth.String()
	}

	opts := []string{
		"API URL: " + s.BaseURL,
		"Auth: " + authStr,
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
