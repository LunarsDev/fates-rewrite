package renderers

import "kitescratch/ui"

func RenderMap(a map[string]any) string {
	s := ""
	for k, v := range a {
		s += ui.PurpleTextSL(k)
		s += ui.PurpleTextSL(" => ")
		s += ui.PurpleTextS(v)
	}
	return s
}
