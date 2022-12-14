package types

import (
	"time"
)

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

type Oauth2 struct {
	State string `json:"state"`
	Url   string `json:"url"`
}

func (o Oauth2) String() string {
	return o.Url + "&state=" + o.State
}

type UserStatus int

const (
	UserStatusOnline UserStatus = iota
	UserStatusIdle
	UserStatusDnd
	UserStatusOffline
)

func (s UserStatus) String() string {
	switch s {
	case UserStatusOnline:
		return "online"
	case UserStatusIdle:
		return "idle"
	case UserStatusDnd:
		return "dnd"
	case UserStatusOffline:
		return "offline"
	}
	return ""
}

type UserState int

const (
	UserStateNormal UserState = iota
	UserStateGlobalBan
	UserStateProfileEditBan
)

func (s UserState) String() string {
	switch s {
	case UserStateNormal:
		return "normal"
	case UserStateGlobalBan:
		return "globalBan"
	case UserStateProfileEditBan:
		return "profileEditBan"
	}
	return ""
}

type UserExperiment int

const (
	UserExperimentUnknown UserExperiment = iota
	UserExperimentGetRoleSelector
	UserExperimentLynxExperimentRolloutView
	UserExperimentBotReport
	UserExperimentServerAppealCertification
	UserExperimentUserVotePrivacy
	UserExperimentDevPortal
)

func (e UserExperiment) String() string {
	switch e {
	case UserExperimentUnknown:
		return "unknown"
	case UserExperimentGetRoleSelector:
		return "getRoleSelector"
	case UserExperimentLynxExperimentRolloutView:
		return "lynxExperimentRolloutView"
	case UserExperimentBotReport:
		return "botReport"
	case UserExperimentServerAppealCertification:
		return "serverAppealCertification"
	case UserExperimentUserVotePrivacy:
		return "userVotePrivacy"
	case UserExperimentDevPortal:
		return "devPortal"
	}
	return ""
}

type DiscordUser struct {
	ID            string     `json:"id"`
	Username      string     `json:"username"`
	Discriminator string     `json:"disc"`
	Avatar        string     `json:"avatar"`
	Bot           bool       `json:"bot"`
	System        bool       `json:"system"`
	Status        UserStatus `json:"status"`
	Flags         int        `json:"flags"`
}

func (d DiscordUser) String() string {
	return d.Username + "#" + d.Discriminator + " [" + d.ID + "]"
}

type OauthUser struct {
	State           UserState        `json:"state"`
	Token           string           `json:"token"`
	User            DiscordUser      `json:"user"`
	RefreshToken    *string          `json:"refresh_token"`
	SiteLang        string           `json:"site_lang"`
	CSS             string           `json:"css"`
	UserExperiments []UserExperiment `json:"user_experiments"`
	Permissions     Permission       `json:"permissions"`
}

type BotServerFlag int

const (
	BotServerFlagUnlocked BotServerFlag = iota
	BotServerFlagEditLocked
	BotServerFlagStaffLocked
	BotServerFlagStatsLocked
	BotServerFlagVoteLocked
	BotServerFlagSystem
	BotServerFlagWhitelistOnly
	BotServerFlagKeepBannerDecor
	BotServerFlagNSFW
	BotServerFlagLoginRequired
)

func (f BotServerFlag) String() string {
	switch f {
	case BotServerFlagUnlocked:
		return "unlocked"
	case BotServerFlagEditLocked:
		return "editLocked"
	case BotServerFlagStaffLocked:
		return "staffLocked"
	case BotServerFlagStatsLocked:
		return "statsLocked"
	case BotServerFlagVoteLocked:
		return "voteLocked"
	case BotServerFlagSystem:
		return "system"
	case BotServerFlagWhitelistOnly:
		return "whitelistOnly"
	case BotServerFlagKeepBannerDecor:
		return "keepBannerDecor"
	case BotServerFlagNSFW:
		return "nsfw"
	case BotServerFlagLoginRequired:
		return "loginRequired"
	}
	return ""
}

type BotServerState int

const (
	BotServerStateApproved BotServerState = iota
	BotServerStatePending
	BotServerStateDenied
	BotServerStateHidden
	BotServerStateBanned
	BotServerStateUnderReview
	BotServerStateCertified
	BotServerStateArchived
	BotServerStatePrivateViewable
	BotServerStatePrivateStaffOnly
)

type Snippet struct {
	User        DiscordUser     `json:"user"`
	Votes       int             `json:"votes"`
	Description string          `json:"description"`
	Flags       []BotServerFlag `json:"flags"`
	BannerCard  string          `json:"banner_card"`
	State       BotServerState  `json:"state"`
	GuildCount  int             `json:"guild_count"`
}

type ProfileSnippet struct {
	User        DiscordUser `json:"user"`
	Banner      string      `json:"banner"`
	Description string      `json:"description"`
}

/* name: str
   """The pack's name"""

   description: str
   """The pack's description"""

   icon: str
   """The pack's icon"""

   banner: Optional[str] = None
   """The pack's banner"""*/

type ResolvedPackBot struct {
	User        DiscordUser `json:"user"`
	Description string      `json:"description"`
}

type BotPack struct {
	ID           string            `json:"id"`
	Name         string            `json:"name"`
	Description  string            `json:"description"`
	Icon         string            `json:"icon"`
	Banner       string            `json:"banner"`
	ResolvedBots []ResolvedPackBot `json:"resolved_bots"`
	Owner        DiscordUser       `json:"owner"`
	CreatedAt    time.Time         `json:"created_at"`
}

type Index struct {
	New       []Snippet `json:"new"`
	TopVoted  []Snippet `json:"top_voted"`
	Certified []Snippet `json:"certified"`
}

type Permission struct {
	Index int      `json:"index"`
	Roles []string `json:"roles"`
	Name  string   `json:"name"`
}

type PermissionList struct {
	Perms map[string]Permission `json:"perms"`
}

type AuthCheck struct {
	AuthType TargetType `json:"auth_type"`
	TargetID string     `json:"target_id"`
	Token    string     `json:"token"`
	Compat   bool       `json:"compat"`
}

type DataAction string

const (
	DataActionRequest DataAction = "req"
	DataActionDelete  DataAction = "upd"
)

type DataResponse struct {
	TaskID string `json:"task_id"`
}

type Invite struct {
	Invite string `json:"invite"`
}

type BotSecrets struct {
	APIToken      string `json:"api_token"`
	Webhook       string `json:"webhook"`
	WebhookSecret string `json:"webhook_secret"`
}

type SearchResponse struct {
	Bots     []Snippet        `json:"bots"`
	Servers  []Snippet        `json:"servers"`
	Profiles []ProfileSnippet `json:"profiles"`
	Packs    []BotPack        `json:"packs"`
}

type SearchFilter struct {
	From any `json:"from"`
	To   any `json:"to"`
}

func (f SearchFilter) Map() map[string]any {
	return map[string]interface{}{
		"filter_from": f.From,
		"filter_to":   f.To,
	}
}

type BotAddTicket struct {
	Ticket string         `json:"ticket"`
	BotID  string         `json:"bot_id"`
	Data   map[string]any `json:"data"`
}

type LongDescriptionType int

const (
	LongDescriptionTypeHTML LongDescriptionType = iota
	LongDescriptionTypeMarkdown
)

type BotAddFinalize struct {
	Ticket              string              `json:"ticket"`
	Tags                []string            `json:"tags"`
	Features            []string            `json:"features"`
	Prefix              string              `json:"prefix"`
	Invite              string              `json:"invite"`
	Vanity              string              `json:"vanity"`
	Description         string              `json:"description"`
	LongDescriptionType LongDescriptionType `json:"long_description_type"`
	LongDescription     string              `json:"long_description"`
}

type Response struct {
	Done   bool   `json:"done"`
	Reason string `json:"reason"`
	Code   string `json:"code"`
	Data   any    `json:"data"`
}
