package renderers

import (
	"kitescratch/types"
	"kitescratch/ui"
	"reflect"
)

// Renders a snippet
func Snippet(snip types.Snippet) string {
	var snipStr string

	// Username
	snipStr += ui.BoldBlueTextS(snip.User.Username + " [" + snip.User.ID + "]")

	// Description
	snipStr += ui.NormalTextS(snip.Description)

	// Use reflect to add all other fields
	v := reflect.ValueOf(snip)

	snipStr += "\n"
	for i := 0; i < v.NumField(); i++ {
		field := v.Field(i)
		fieldName := v.Type().Field(i).Name

		// Skip fields that are already rendered
		if fieldName == "User" || fieldName == "Description" {
			continue
		}

		snipStr += "=> "
		snipStr += ui.PurpleTextS(fieldName+":", field.Interface())
	}

	snipStr += "\n"

	return snipStr
}
