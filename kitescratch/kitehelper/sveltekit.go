package main

import (
	"fmt"
	"os"
)

const (
	loadDef = `
/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
}	
	`
)

func newsun(progname string, args []string) {
	// Do smth
	if len(args) == 0 {
		fmt.Printf("usage: %s newsun <sunbeam route name>\n", progname)
		os.Exit(1)
	}

	os.Mkdir(args[0], 0755)

	os.WriteFile(args[0]+"/+page.js", []byte(loadDef), 0600)
	os.WriteFile(args[0]+"/+page.svelte", []byte(""), 0600)
}
