package auth

import "kitescratch/types"

type Auth struct {
	TargetType types.AuthTargetType
	ID         string
	Token      string
}

func (a *Auth) String() string {
	return string(a.TargetType) + "|" + a.ID + "|" + a.Token
}
