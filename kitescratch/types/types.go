package types

type Tag struct {
	ID          string  `json:"id"`
	IconifyData string  `json:"iconify_data"`
	Name        string  `json:"name"`
	OwnerGuild  *string `json:"owner_guild"`
}

func (t Tag) String() string {
	name := t.Name + " (" + t.ID + ")"

	if t.OwnerGuild != nil {
		name += " [owner: " + *t.OwnerGuild + "]"
	}

	return name
}

type Feature struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	ViewedAs    string `json:"viewed_as"`
	Description string `json:"description"`
}

func (f Feature) String() string {
	return f.Name + " (" + f.ID + ") [" + f.ViewedAs + "] => " + f.Description
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

type AuthTargetType string

const (
	AuthTargetTypeUser   AuthTargetType = "user"
	AuthTargetTypeBot    AuthTargetType = "bot"
	AuthTargetTypeServer AuthTargetType = "server"
)

type TargetType int

const (
	TargetTypeBot TargetType = iota
	TargetTypeServer
	TargetTypeUser
)

func (t TargetType) String() string {
	switch t {
	case TargetTypeBot:
		return "bot"
	case TargetTypeServer:
		return "server"
	case TargetTypeUser:
		return "user"
	}
	return ""
}

type Vanity struct {
	TargetID   string     `json:"target_id"`
	TargetType TargetType `json:"target_type"`
	Code       string     `json:"code"`
}
