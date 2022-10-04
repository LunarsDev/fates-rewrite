package renderers

import (
	"kitecli/types"
	"kitecli/ui"
	"strconv"
)

func AskSearchFilter(name string) types.SearchFilter {
	var filter types.SearchFilter = types.SearchFilter{}

	from := ui.AskInput(name + " from (leave blank for any)")
	to := ui.AskInput(name + " to (leave blank for any)")

	var fromV int
	var toV int
	var err error
	if from != "" {
		fromV, err = strconv.Atoi(from)
		if err != nil {
			ui.RedText("Invalid number for from")
			return AskSearchFilter(name)
		}

		filter.From = fromV
	} else {
		filter.From = 0
	}

	if to != "" {
		toV, err = strconv.Atoi(to)
		if err != nil {
			ui.RedText("Invalid number for to")
			return AskSearchFilter(name)
		}

		filter.To = toV
	} else {
		filter.To = -1
	}

	return filter
}
