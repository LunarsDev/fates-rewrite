package config

type Config struct {
	Secrets  Secrets         `yaml:"secrets"`
	Storage  Storage         `yaml:"storage"`
	Servers  Servers         `yaml:"servers"`
	Perms    map[string]Perm `yaml:"perms"`
	Channels Channels        `yaml:"channels"`
	Misc     Misc            `yaml:"misc"`
}

type Secrets struct {
	Token        string `yaml:"token"`
	JApi         string `yaml:"japi_key"`
	ClientID     string `yaml:"client_id"`
	ClientSecret string `yaml:"client_secret"`
}

type Storage struct {
	Postgres Postgres `yaml:"postgres"`
	Redis    Redis    `yaml:"redis"`
}

type Postgres struct {
	Host     string `yaml:"host"`
	Port     uint16 `yaml:"port"`
	User     string `yaml:"user"`
	Password string `yaml:"password"`
	Database string `yaml:"database"`
}

type Redis struct {
	Host     string `yaml:"host"`
	Port     uint16 `yaml:"port"`
	Password string `yaml:"password"`
	Database uint32 `yaml:"database"`
}

type Servers struct {
	Main uint64 `yaml:"main"`
}

type Perm struct {
	Roles []uint64 `yaml:"roles"`
	Index uint8    `yaml:"index"`
}

type Channels struct {
	BotLogs uint64 `yaml:"bot_logs"`
}

type Misc struct {
	RestrictedVanity []string `yaml:"restricted_vanity"`
}

func (c Config) Validate() {
	if c.Secrets.Token == "" {
		panic("Token is required")
	}
	if c.Secrets.ClientID == "" {
		panic("Client ID is required")
	}
	if c.Secrets.ClientSecret == "" {
		panic("Client secret is required")
	}
	if c.Secrets.JApi == "" {
		panic("JApi key is required")
	}
	if c.Storage.Postgres.Database == "" {
		panic("Postgres database is required")
	}
	if c.Servers.Main == 0 {
		panic("Main server is required")
	}
	if c.Channels.BotLogs == 0 {
		panic("Bot logs channel is required")
	}
	if len(c.Misc.RestrictedVanity) == 0 {
		panic("Restricted vanity is required")
	}
}
