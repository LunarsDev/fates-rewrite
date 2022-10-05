package migrate

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
}
