package main

import (
	"fmt"
	"os"
)

type command struct {
	Func func(progname string, args []string)
	Help string
}

var cmds = map[string]command{
	"newsun": command{
		Func: newsun,
		Help: "Create a new sunbeam route",
	},
}

func cmdList() {
	fmt.Println("Commands:")
	for k, cmd := range cmds {
		fmt.Println(k+":", cmd.Help)
	}
}

func main() {
	progname := os.Args[0]
	args := os.Args[1:]

	if len(args) == 0 {
		fmt.Printf("usage: %s <command> [args]\n\n", progname)
		cmdList()
		os.Exit(1)
	}

	cmd, ok := cmds[args[0]]
	if !ok {
		fmt.Printf("unknown command: %s\n\n", args[0])
		cmdList()
		os.Exit(1)
	}

	cmd.Func(progname, args[1:])
}
