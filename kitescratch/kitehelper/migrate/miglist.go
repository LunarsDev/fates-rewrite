package migrate

import (
	"encoding/json"
	"fmt"
	"io"
	"kitehelper/common"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/fatih/color"
	"github.com/jackc/pgtype"
	"gopkg.in/yaml.v3"
)

// Contains the list of migrations

var (
	statusBoldErr = color.New(color.Bold, color.FgRed).PrintlnFunc()
)

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
		name: "Validate and set bot id and client id properly",
		function: func() {
			cacheFile, err := os.OpenFile(common.GetRepoRoot()+"/kitescratch/kitehelper/migrate/migcache/cidcache.yaml", os.O_RDWR|os.O_CREATE, 0755)

			if err != nil {
				panic(err)
			}

			migToDeleteFile, err := os.OpenFile(common.GetRepoRoot()+"/kitescratch/kitehelper/migrate/migcache/dellist.yaml", os.O_RDWR|os.O_CREATE, 0755)

			if err != nil {
				panic(err)
			}

			var delBots []int

			err = yaml.NewDecoder(migToDeleteFile).Decode(&delBots)

			if err != nil {
				panic(err)
			}

			for _, bot := range delBots {
				_, err = pgpool.Exec(ctx, "DELETE FROM bots WHERE bot_id = $1", bot)

				if err != nil {
					panic(err)
				}
			}

			var cache map[int]int

			err = yaml.NewDecoder(cacheFile).Decode(&cache)

			if err != nil {
				panic(err)
			}

			cacheFile.Close()

			client := http.Client{
				Timeout: 30 * time.Second,
			}

			bots, err := pgpool.Query(ctx, "select bot_id, client_id from bots")

			if err != nil {
				panic(err)
			}

			var count pgtype.Int8

			err = pgpool.QueryRow(ctx, "select count(*) from bots").Scan(&count)

			if err != nil {
				panic(err)
			}

			defer bots.Close()

			invalidCount := []int{}

			i := 0

			delBotFunc := func(botId int, auto bool) {
				flag := true
				for flag {
					var delete string
					if !auto {
						delete = common.AskInput("This bot is likely bad, do you want to delete it?")
					} else {
						delete = "Y"
					}

					if strings.ToLower(delete) == "y" {
						_, err := pgpool.Exec(ctx, "delete from bots where bot_id = $1", botId)

						if err != nil {
							panic(err)
						}

						delBots = append(delBots, botId)

						// Write to the file
						migToDeleteFile, err := os.OpenFile(common.GetRepoRoot()+"/kitescratch/kitehelper/migrate/migcache/dellist.yaml", os.O_RDWR|os.O_CREATE, 0755)

						if err != nil {
							panic(err)
						}

						err = yaml.NewEncoder(migToDeleteFile).Encode(delBots)

						if err != nil {
							panic(err)
						}

						flag = false
					} else if strings.ToLower(delete) == "n" {
						flag = false
					} else {
						statusBoldErr("Invalid option. Use Y or N")
					}
				}
			}

			for bots.Next() {
				i++

				var botId int
				var clientId pgtype.Int8

				err = bots.Scan(&botId, &clientId)

				if err != nil {
					panic(err)
				}

				var appId string
				if clientId.Status == pgtype.Present && clientId.Int != 0 {
					appId = strconv.FormatInt(clientId.Int, 10)
				} else {
					appId = strconv.Itoa(botId)
				}

				statusBoldBlue("Validating bot", botId, "with client id", appId, "["+strconv.Itoa(i)+"/"+strconv.FormatInt(count.Int, 10)+"]")

				if v, ok := cache[botId]; ok {
					statusBoldBlue("Using cached client id", v, "for bot", botId)
					_, err = pgpool.Exec(ctx, "UPDATE bots SET client_id = $1 WHERE bot_id = $2", v, botId)

					if err != nil {
						panic(err)
					}
					continue
				}

				// Query japi.rest for the client id

				time.Sleep(1 * time.Second)
				resp, err := client.Get("https://japi.rest/discord/v1/application/" + appId)

				if err != nil {
					panic(err)
				}

				if resp.StatusCode == 429 {
					statusBoldYellow("Handling ratelimit for bot", appId)

					// Read body to string
					body, err := io.ReadAll(resp.Body)

					if err != nil {
						panic(err)
					}

					// Close the body
					resp.Body.Close()

					statusBoldYellow("Body:", string(body))

					time.Sleep(120 * time.Second)

					resp, err = client.Get("https://japi.rest/discord/v1/application/" + appId)

					if err != nil {
						panic(err)
					}
				}

				if resp.StatusCode != 200 {
					statusBoldErr("Bot", botId, "has an invalid client id of", appId, "got status code", resp.StatusCode)

					// There is no way this bot exists, delete it, this is done as the bot is obviously bad
					if botId > 700000000000000000 {
						statusBoldErr("Deleting obvious bad bot")
						delBotFunc(botId, true)
					} else {
						delBotFunc(botId, false)
					}

					// Read body to string
					body, err := io.ReadAll(resp.Body)

					if err != nil {
						panic(err)
					}

					// Close the body
					resp.Body.Close()

					statusBoldYellow("Body:", string(body))

					invalidCount = append(invalidCount, botId)

					continue
				}

				var app map[string]any

				err = json.NewDecoder(resp.Body).Decode(&app)

				if err != nil {
					panic(err)
				}

				resp.Body.Close()

				var botData = app["data"].(map[string]any)

				// Check if the bot id sent is the same as the one in the database
				fmt.Println(botData)

				if v, ok := botData["bot"]; ok {

					if v == nil {
						statusBoldErr("Application doesnt have a bot")
						_, err = pgpool.Exec(ctx, "delete from bots where bot_id = $1", botId)

						if err != nil {
							panic(err)
						}

						delBots = append(delBots, botId)

						// Write to the file
						migToDeleteFile, err := os.OpenFile(common.GetRepoRoot()+"/kitescratch/kitehelper/migrate/migcache/dellist.yaml", os.O_RDWR|os.O_CREATE, 0755)

						if err != nil {
							panic(err)
						}

						err = yaml.NewEncoder(migToDeleteFile).Encode(delBots)

						if err != nil {
							panic(err)
						}

						continue
					}

					if botData["bot"].(map[string]any)["id"].(string) != strconv.Itoa(botId) {
						statusBoldErr("Bot", botId, "has an invalid client id of", appId, "(expected", botData["bot"].(map[string]any)["id"].(string), "and", botData["application"].(map[string]any)["id"].(string), ")")

						rId := common.AskInput("Enter the client ID for this bot if possible: ")

						rid, err := strconv.Atoi(rId)

						if err != nil {
							panic(err)
						}

						_, err = pgpool.Exec(ctx, "UPDATE bots SET client_id = $1 WHERE bot_id = $2", rid, botId)

						if err != nil {
							panic(err)
						}
					} else {
						id, err := strconv.Atoi(botData["application"].(map[string]any)["id"].(string))

						if err != nil {
							panic(err)
						}
						cache[botId] = id

						// Write to the cache file
						cacheFile, err := os.OpenFile(common.GetRepoRoot()+"/kitescratch/kitehelper/migrate/migcache/cidcache.yaml", os.O_RDWR|os.O_CREATE, 0755)

						if err != nil {
							panic(err)
						}

						err = yaml.NewEncoder(cacheFile).Encode(cache)

						if err != nil {
							panic(err)
						}

						_, err = pgpool.Exec(ctx, "UPDATE bots SET client_id = $1 WHERE bot_id = $2", id, botId)

						if err != nil {
							panic(err)
						}
					}
				} else {
					statusBoldErr("Application has no bot struct. This is a bug")

					delBotFunc(botId, false)

					invalidCount = append(invalidCount, botId)
				}
			}

			fmt.Println("Invalid count:", invalidCount)
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
