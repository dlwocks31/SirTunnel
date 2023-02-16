#/bin/bash

caddyVersion=2.1.1
caddyArch=$(uname -m | grep -q 'x86_64' && echo 'amd64' || echo 'arm64')

echo Download Caddy
caddyGz=caddy_${caddyVersion}_linux_${caddyArch}.tar.gz
curl -s -O -L https://github.com/caddyserver/caddy/releases/download/v${caddyVersion}/${caddyGz}
tar xf ${caddyGz}

echo Clean up extra Caddy files
rm ${caddyGz}
rm LICENSE
rm README.md

echo Enable Caddy to bind low ports
sudo setcap 'cap_net_bind_service=+ep' caddy
