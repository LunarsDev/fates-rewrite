package main

import (
	"context"
	_ "embed"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strconv"
	"strings"

	"github.com/jackc/pgx/v4/pgxpool"
	"github.com/joho/godotenv"
)

var ctx = context.Background()

//go:embed schema.sql
var schema []byte

//go:embed seed_data.json
var seedData []byte

//go:embed seed_meta.json
var seedMetaBytes []byte

type seed struct {
	Table string           `json:"table"`
	Data  []map[string]any `json:"data"`
}

type seedMeta struct {
	Nonce     string `json:"nonce"`
	Version   int    `json:"version"`
	CreatedAt string `json:"created_at"`
}

func init() {
	godotenv.Load()
}

func main() {
	// Try recovering from a panic in defer
	defer func() {
		if r := recover(); r != nil {
			fmt.Println("ERROR:", r)

			var a string

			fmt.Scanln(&a)

			os.Exit(1)
		}
	}()

	if runtime.GOOS == "linux" || runtime.GOOS == "darwin" {
		// Check if psql is installed
		path, err := exec.LookPath("psql")

		if err != nil || path == "" {
			fmt.Println("psql is not installed")

			if runtime.GOOS == "linux" {
				// Check for apt
				if path, err := exec.LookPath("apt"); err == nil && path != "" {
					// Warn this is experimental
					fmt.Printf("Do you wish for seedman to try and install PostgreSQL. This is an experimental feature. It may not work as expected (y/n): ")

					// Ask for permission
					var answer string

					fmt.Scanln(&answer)

					if answer == "y" || answer == "Y" {
						fmt.Println("Trying to install psql...")

						// Add postgres ppa
						shCmd := "sudo sh -c 'echo \"deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list"

						if err := exec.Command("sh", "-c", shCmd).Run(); err != nil {
							fmt.Println("Error adding ppa:", err)
							os.Exit(1)
						}

						cmd := exec.Command("sudo", "apt", "install", "postgresql-14")
						cmd.Stdout = os.Stdout
						cmd.Stderr = os.Stderr
						err := cmd.Run()
						if err != nil {
							fmt.Println("Error installing psql")
							os.Exit(1)
						}

						// Since this is a dev machine, allow password login
						shCmd = "sudo sed -i '/^host/s/ident/md5/' /etc/postgresql/14/main/pg_hba.conf"

						if err := exec.Command("sh", "-c", shCmd).Run(); err != nil {
							fmt.Println("Error enabling password login:", err)
							os.Exit(1)
						}

						// Change identification mode
						shCmd = "sudo sed -i '/^local/s/peer/trust/' /etc/postgresql/14/main/pg_hba.conf"

						if err := exec.Command("sh", "-c", shCmd).Run(); err != nil {
							fmt.Println("Error changing identification mode:", err)
							os.Exit(1)
						}

						// Restart postgresql
						shCmd = "sudo systemctl restart postgresql"

						if err := exec.Command("sh", "-c", shCmd).Run(); err != nil {
							fmt.Println("Error restarting postgresql:", err)
							os.Exit(1)
						}
					}
				}
			} else {
				os.Exit(1)
			}
		}
	}

	// Create postgres conn
	conn, err := pgxpool.Connect(ctx, "")

	if err != nil {
		panic(err)
	}

	var seedInf []seed
	// Load seed data from seedData json
	err = json.Unmarshal(seedData, &seedInf)

	if err != nil {
		panic(err)
	}

	var seedMeta seedMeta

	// Load seed meta from seedMeta json
	err = json.Unmarshal(seedMetaBytes, &seedMeta)

	if err != nil {
		panic(err)
	}

	// Unpack schema to seedman.tmp
	f, err := os.Create("seedman.tmp")

	defer func() {
		f.Close()
		os.Remove("seedman.tmp")
	}()

	if err != nil {
		panic("Could not unpack tmp files" + err.Error())
	}

	_, err = f.Write(schema)

	if err != nil {
		panic("Could not unpack tmp files for writing" + err.Error())
	}

	// Create role root
	conn.Exec(ctx, "CREATE ROLE root")

	conn.Exec(ctx, "DROP DATABASE infinity")
	conn.Exec(ctx, "CREATE DATABASE infinity")

	// Use pg_restore to restore seedman.tmp
	cmd := exec.Command("pg_restore", "-d", "infinity", "-h", "localhost", "-p", "5432", "seedman.tmp")

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	outCode := cmd.Run()

	if outCode != nil {
		panic(outCode)
	}

	if !cmd.ProcessState.Success() {
		panic(outCode)
	}

	os.Setenv("PGDATABASE", "infinity")

	conn, err = pgxpool.Connect(ctx, "")

	if err != nil {
		panic("conn failed" + err.Error())
	}

	// Create the seed_info table
	conn.Exec(ctx, "CREATE TABLE seed_info (nonce TEXT NOT NULL, version INTEGER NOT NULL, created_at TIMESTAMPTZ NOT NULL)")

	// Insert seed info
	conn.Exec(ctx, "INSERT INTO seed_info (nonce, version, created_at) VALUES ($1, $2, $3)", seedMeta.Nonce, seedMeta.Version, seedMeta.CreatedAt)

	// Loop over seed data and insert into db
	for _, s := range seedInf {
		for _, d := range s.Data {
			var i int = 1
			var args []any
			var keys []string
			var sqlArgs []string

			// Loop over all map props
			for k, v := range d {
				keys = append(keys, k)
				args = append(args, v)
				sqlArgs = append(sqlArgs, "$"+strconv.Itoa(i))
				i++
			}

			// Create sql string
			fmt.Println(s.Table)
			sql := "INSERT INTO " + s.Table + " (" + strings.Join(keys, ", ") + ") VALUES (" + strings.Join(sqlArgs, ", ") + ")"

			fmt.Println(sql, args)

			_, err := conn.Exec(ctx, sql, args...)

			if err != nil {
				panic("Could not insert sql" + err.Error())
			}

			i = 1
		}
	}
}
