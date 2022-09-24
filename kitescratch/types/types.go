package types

type Tag struct {
	ID          string  `json:"id"`
	IconifyData string  `json:"iconify_data"`
	Name        string  `json:"name"`
	OwnerGuild  *string `json:"owner_guild"`
}

type Feature struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	ViewedAs    string `json:"viewed_as"`
	Description string `json:"description"`
}

type BotMeta struct {
	Tags     []Tag     `json:"tags"`
	Features []Feature `json:"features"`
}

type ServerMeta struct {
	Tags []Tag `json:"tags"`
}

type ListMeta struct {
	Bot    BotMeta    `json:"bot"`
	Server ServerMeta `json:"server"`
}
