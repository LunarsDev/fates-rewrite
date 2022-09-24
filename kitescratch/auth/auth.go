package auth

type AuthTargetType string

const (
	AuthTargetTypeUser   AuthTargetType = "user"
	AuthTargetTypeBot    AuthTargetType = "bot"
	AuthTargetTypeServer AuthTargetType = "server"
)

type Auth struct {
	TargetType AuthTargetType
	ID         string
	Token      string
}
