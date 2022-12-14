package main

import (
	"fmt"
	"kitehelper/config"
	"kitehelper/migrate"
	"kitehelper/sveltekit"
	"kitehelper/tests"
	"os"
)

type command struct {
	Func func(progname string, args []string)
	Help string
}

var cmds = map[string]command{
	"newsun": {
		Func: sveltekit.Newsun,
		Help: "Create a new sunbeam route",
	},
	"test": {
		Func: tests.Tester,
		Help: "Run tests [Set NO_INTERACTION environment variable to disable all input interaction]",
	},
	"migrate": {
		Func: migrate.Migrate,
		Help: "Run custom migrations",
	},
	"cfgvalidate": {
		Func: config.ValidateConfig,
		Help: "Validate config.yaml",
	},
	"cfgsample": {
		Func: config.GenConfigSample,
		Help: "Generate config_sample.yaml",
	},
	"cfgupdate": {
		Func: config.UpdateConfig,
		Help: "Update config.yaml to the latest version",
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
