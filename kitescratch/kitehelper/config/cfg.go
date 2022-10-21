package config

type Config struct {
	Secrets  Secrets  `yaml:"secrets"`
	Storage  Storage  `yaml:"storage"`
	Servers  Servers  `yaml:"servers"`
	Deploy   Deploy   `yaml:"deploy"`
	Perms    PermList `yaml:"perms"`
	Channels Channels `yaml:"channels"`
	Misc     Misc     `yaml:"misc"`
}

type Secrets struct {
	Token        string `yaml:"token" comment:"Discord main bot token"`
	ClientID     string `yaml:"client_id" default:"1031535884539023370" comment:"Discord Client ID"`
	ClientSecret string `yaml:"client_secret"`
	JApi         string `yaml:"japi_key" comment:"Get this from https://key.japi.rest"`
}

type Storage struct {
	Postgres Postgres `yaml:"postgres"`
	Redis    Redis    `yaml:"redis"`
}

type Postgres struct {
	Host     string `yaml:"host" comment:"Hostname, defaults to PGHOST" required:"false"`
	Port     uint16 `yaml:"port" default:"5432" comment:"Port, defaults to PGPORT" required:"false"`
	User     string `yaml:"user" comment:"Username, defaults to PGUSER" required:"false"`
	Password string `yaml:"password" comment:"Password, defaults to PGPASSWORD" required:"false"`
	Database string `yaml:"database" comment:"Database name"`
}

type Redis struct {
	Host     string `yaml:"host" default:"127.0.0.1" comment:"Hostname, defaults to REDIS_HOST" required:"false"`
	Port     uint16 `yaml:"port" default:"6379" comment:"Port, defaults to REDIS_PORT" required:"false"`
	Password string `yaml:"password" comment:"Password, defaults to REDIS_PASSWORD" required:"false"`
	Database uint32 `yaml:"database" default:"0" comment:"Database, defaults to REDIS_DB" required:"false"`
}

type Deploy struct {
	Sunbeam string `yaml:"sunbeam" default:"http://localhost:5001" comment:"Sunbeam URL"`
}

type Servers struct {
	Main uint64 `yaml:"main" default:"789934742128558080" comment:"Main server ID"`
}

type PermList struct {
	// Sudo -> The highest permission level, can do anything
	Sudo Perm `yaml:"sudo"`

	// HeadAdmin -> Can do most things (other than owner-only actions)
	HeadAdmin Perm `yaml:"head_admin"`

	// Admin -> Can do some actions on the list such as banning users from the API and uncertifying bots
	Admin Perm `yaml:"admin"`

	// Moderator -> Can only do moderation actions on the list such as reviewing bots and requeing+unverifying them
	Moderator Perm `yaml:"moderator"`
}

type Perm struct {
	RoleComments []string `yaml:"role_comments" default:"dev,overseer,owner" comment:"Comments for the roles above corresponding to index"`
	Roles        []uint64 `yaml:"roles" default:"976891305336655903 # role A, 836326299223195738 # role B etc."`
	Index        uint8    `yaml:"index"`
}

type Channels struct {
	BotLogs uint64 `yaml:"bot_logs"`
}

type Misc struct {
	RestrictedVanity []string `yaml:"restricted_vanity" default:"api,docs,add-bot,admin"`
}

func (c *Config) Fixup() {
	// Fixup: Perms
	c.Perms.Sudo.Index = 10
	c.Perms.HeadAdmin.Index = 9
	c.Perms.Admin.Index = 8
	c.Perms.Moderator.Index = 7

	// Apply correct comments to c.Perms.*.RoleComments if not set
	if len(c.Perms.HeadAdmin.RoleComments) == 0 {
		c.Perms.HeadAdmin.RoleComments = []string{"head_admin"}
	}
	if len(c.Perms.Admin.RoleComments) == 0 {
		c.Perms.Admin.RoleComments = []string{"admin"}
	}
	if len(c.Perms.Moderator.RoleComments) == 0 {
		c.Perms.Moderator.RoleComments = []string{"moderator"}
	}
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
