package state

// Some core global state (to avoid race conditions and millions of parameters)
type State struct {
	BaseURL string
}

var GlobalState State

func init() {
	GlobalState = State{
		BaseURL: "http://localhost:8000", // Default API URL
	}
}
