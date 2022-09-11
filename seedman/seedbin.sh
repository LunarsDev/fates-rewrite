# Use this to generate the seedman binaries for all supported archs

dir=$(pwd)

# Check if $dir ends with /seedman

if [[ $dir =~ "seedman" ]]; then
    echo "In seedman dir. Changing directory to ../"
    cd ../
fi

# Run create_seed_files.py
python3 seedman/create_seed_files.py

cd seedman

echo "Building seedman exec"

GOOS=linux GOARCH=amd64 go build -o bin/seedman_linux_amd64
GOOS=darwin GOARCH=amd64 go build -o bin/seedman_mac_amd64
GOOS=darwin GOARCH=arm64 go build -o bin/seedman_mac_arm64
GOOS=windows GOARCH=amd64 go build -o bin/seedman_windows_amd64.exe
