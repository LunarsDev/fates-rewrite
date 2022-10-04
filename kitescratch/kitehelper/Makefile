all:
	go build -v
package:
	rm -rf bin
	mkdir bin
	GOOS=linux GOARCH=amd64 go build -o bin/kitehelper_linux_amd64
	GOOS=darwin GOARCH=amd64 go build -o bin/kitehelper_mac_amd64
	GOOS=darwin GOARCH=arm64 go build -o bin/kitehelper_mac_arm64
	GOOS=windows GOARCH=amd64 go build -o bin/kitehelper_windows_amd64.exe