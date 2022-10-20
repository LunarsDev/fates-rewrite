package config

import (
	"fmt"
	"io"
	"kitehelper/common"
	"os"

	"github.com/fatih/color"
	"gopkg.in/yaml.v3"
)

var statusBold = color.New(color.Bold, color.FgWhite).PrintlnFunc()

func ValidateConfig(progname string, args []string) {
	os.Chdir(common.GetRepoRoot())

	// Open config.yaml
	f, err := os.Open("config.yaml")

	if err != nil {
		panic(err)
	}

	// Validate using yaml
	fileBytes, err := io.ReadAll(f)

	if err != nil {
		panic(err)
	}

	var t Config
	err = yaml.Unmarshal(fileBytes, &t)

	if err != nil {
		panic(err)
	}

	t.Validate()

	statusBold("Config validation successful")
}

func GenConfigSample(progname string, args []string) {
	var cfg Config = Config{
		Misc: Misc{
			RestrictedVanity: []string{"api", "docs", "add-bot", "admin"},
		},
		Perms: map[string]Perm{
			"sudo": {
				Index: 10,
			},
			"head_admin": {
				Index: 9,
			},
		},
	}

	syp := simpleYamlParser{}

	fmt.Println(syp.parse(cfg))
}
