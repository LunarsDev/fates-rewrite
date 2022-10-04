// Contains the list of tests
package tests

import (
	"embed"
)

//go:embed custom
var customTests embed.FS

var testList = testset{
	Tests: []test{
		{
			name:       "kitescratch_impl.py",
			cmd:        []string{"python3"},
			customTest: "kitescratch_impl.py",
		},
		{
			name: "sunbeam (format)",
			cmd:  []string{"npm", "run", "format"},
			cwd:  "sunbeam",
		},
		{
			name: "sunbeam (lint)",
			cmd:  []string{"npm", "run", "lint-fix"},
			cwd:  "sunbeam",
			//ignoreErrors: "Still initial stages of the rewrite",
		},
		{
			name: "fates (black)",
			cmd:  []string{"black", "fates"},
		},
		{
			name: "silverpelt (black)",
			cmd:  []string{"black", "silverpelt"},
		},
	},
}
