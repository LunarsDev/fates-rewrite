package auth

import "kitecli/types"

type Auth struct {
	TargetType types.AuthTargetType
	ID         string
	Token      string
	AuthExt    types.OauthUser // Not actually part of the Auth header, but it's useful to have here
}

func (a *Auth) String() string {
	return string(a.TargetType) + "|" + a.ID + "|" + a.Token
}
