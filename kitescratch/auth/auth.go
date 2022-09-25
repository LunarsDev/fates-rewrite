package auth

import "kitescratch/types"

type Auth struct {
	TargetType types.AuthTargetType
	ID         string
	Token      string
}
