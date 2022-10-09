package migrate

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/jackc/pgtype"
)

// Contains the list of migrations

var migs = []migration{
	{
		name: "bot_library renamed to library",
		function: func() {
			if colExists("bots", "library") {
				alrMigrated()
				return
			}

			_, err := pgpool.Exec(ctx, "ALTER TABLE bots RENAME COLUMN bot_library TO library")

			if err != nil {
				panic(err)
			}
		},
	},
	{
		name: "bot_tags table remerge with bots table",
		function: func() {
			// Check if the table exists
			if exists := tableExists("bot_tags"); exists {
				// Remove the old column from bots if it exists
				if colExists("bots", "tags") {
					_, err := pgpool.Exec(ctx, "ALTER TABLE bots DROP COLUMN tags")

					if err != nil {
						panic(err)
					}
				}

				// Add the column
				_, err := pgpool.Exec(ctx, "ALTER TABLE bots ADD COLUMN tags TEXT[] DEFAULT '{}'")

				if err != nil {
					panic(err)
				}

				// Create an index
				_, err = pgpool.Exec(ctx, "CREATE INDEX bots_tags_idx ON bots USING GIN (tags)")

				if err != nil {
					panic(err)
				}

				// Migrate the data
				botTags, err := pgpool.Query(ctx, "select bot_id, tag from bot_tags")

				if err != nil {
					panic(err)
				}

				defer botTags.Close()

				for botTags.Next() {
					var botID int
					var tag string

					err = botTags.Scan(&botID, &tag)

					if err != nil {
						panic(err)
					}

					statusBoldYellow("Migrating bot", botID, "with a tag of", tag)

					_, err = pgpool.Exec(ctx, "update bots set tags = array_append(tags, $1) where bot_id = $2", tag, botID)

					if err != nil {
						panic(err)
					}
				}

				// Drop the table
				_, err = pgpool.Exec(ctx, "drop table bot_tags")

				if err != nil {
					panic(err)
				}
			} else {
				alrMigrated()
				return
			}
		},
	},
	{
		name: "server_tags rename to server_list_tags for consistency",
		function: func() {
			if tableExists("server_list_tags") {
				alrMigrated()
				return
			}

			_, err := pgpool.Exec(ctx, "ALTER TABLE server_tags RENAME TO server_list_tags")

			if err != nil {
				panic(err)
			}
		},
	},
	{
		name: "vanity.id",
		function: func() {
			if colExists("vanity", "id") {
				alrMigrated()
				return
			}

			_, err := pgpool.Exec(ctx, "ALTER TABLE vanity ADD COLUMN id SERIAL PRIMARY KEY")

			if err != nil {
				panic(err)
			}
		},
	},
	{
		name: "Update invites using P: syntax to fully resolved oauth2 urls",
		function: func() {
			bots, err := pgpool.Query(ctx, "select bot_id, client_id, invite from bots")

			if err != nil {
				panic(err)
			}

			defer bots.Close()

			for bots.Next() {
				var botID int
				var clientID pgtype.Int8
				var invite string

				err = bots.Scan(&botID, &clientID, &invite)

				if err != nil {
					panic(err)
				}

				var id = botID

				if clientID.Status == pgtype.Present && clientID.Int != 0 && clientID.Int != int64(botID) {
					fmt.Println("Bot", botID, "has a client id of", clientID.Int)
					id = int(clientID.Int)
				}

				if strings.HasPrefix(invite, "P:") {
					invite = "https://discord.com/oauth2/authorize?client_id=" + strconv.Itoa(id) + "&scope=bot%20applications.commands&permissions=" + strings.TrimPrefix(invite, "P:")
					fmt.Println(invite, botID)
				} else if !strings.HasPrefix(invite, "https://") {
					invite = "https://discord.com/oauth2/authorize?client_id=" + strconv.Itoa(id) + "&scope=bot%20applications.commands&permissions=0"
					fmt.Println(invite, botID)
				}

				_, err = pgpool.Exec(ctx, "update bots set invite = $1 where bot_id = $2", invite, botID)

				if err != nil {
					panic(err)
				}
			}
		},
	},
	{
		name: "Remove id from bots",
		function: func() {
			if !colExists("bots", "id") {
				alrMigrated()
				return
			}

			_, err := pgpool.Exec(ctx, "ALTER TABLE bots DROP COLUMN id")

			if err != nil {
				panic(err)
			}
		},
	},
}
