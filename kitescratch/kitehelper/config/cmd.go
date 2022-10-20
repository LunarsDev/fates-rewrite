package config

import (
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
	var cfg Config

	f, err := os.Create("config_sample.yaml")

	if err != nil {
		panic(err)
	}

	cfg.Perms = map[string]Perm{
		"sample_perm_1": {
			Roles: []uint64{123456, 192929},
		},
	}

	cfg.Misc = Misc{
		RestrictedVanity: []string{"api", "docs", "add-bot", "admin"},
	}

	defer f.Close()

	enc := yaml.NewEncoder(f)

	err = enc.Encode(cfg)

	if err != nil {
		panic(err)
	}

	statusBold("Config sample generated")
}
