package renderers

import (
	"kitecli/types"
	"kitecli/ui"
)

func BotPack(pack types.BotPack) string {
	var snipText string

	snipText += ui.BoldBlueTextS(pack.Name, "["+pack.ID+"]")

	snipText += ui.NormalTextS(pack.Description)

	snipText += ui.PurpleTextSL("=> ")

	snipText += ui.PurpleTextS("Owner:", pack.Owner.String())

	snipText += ui.BlueTextS("Banner:", pack.Banner, "\nDescription:", pack.Description, "\nIcon:", pack.Icon, "\nCreated At:", pack.CreatedAt.String())

	for _, snip := range pack.ResolvedBots {
		snipText += ui.BlueTextS("\n\nUsername:", snip.User.String(), "\nDescription:", snip.Description)
	}

	return snipText
}
