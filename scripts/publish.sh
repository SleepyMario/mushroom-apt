#!/bin/bash
# Run on the repository host. Signing material must never be inside ROOT.
set -euo pipefail
ROOT=${MUSHROOM_ROOT:-/srv/mushroom-apt}
export GNUPGHOME=${MUSHROOM_GNUPGHOME:-/var/lib/mushroom-apt/signing}
exec 9>/run/lock/mushroom-apt-publish.lock
flock 9
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
cd "$ROOT"
mkdir -p dists/stable/main/binary-amd64/by-hash/{SHA256,SHA512}
dpkg-scanpackages --multiversion pool /dev/null > "$stage/Packages"
gzip -n -9 -c "$stage/Packages" > "$stage/Packages.gz"
index=dists/stable/main/binary-amd64
for name in Packages Packages.gz; do
 hash=$(sha256sum "$stage/$name" | cut -d' ' -f1)
 install -m 0644 "$stage/$name" "$index/by-hash/SHA256/$hash"
 hash512=$(sha512sum "$stage/$name" | cut -d' ' -f1)
 install -m 0644 "$stage/$name" "$index/by-hash/SHA512/$hash512"
 install -m 0644 "$stage/$name" "$index/$name.new"
 mv "$index/$name.new" "$index/$name"
done
apt-ftparchive -o APT::FTPArchive::Release::Origin=Mushroom -o APT::FTPArchive::Release::Label=Mushroom -o APT::FTPArchive::Release::Suite=stable -o APT::FTPArchive::Release::Codename=stable -o APT::FTPArchive::Release::Architectures=amd64 -o APT::FTPArchive::Release::Components=main -o APT::FTPArchive::Release::Acquire-By-Hash=yes release dists/stable > "$stage/Release"
gpg --batch --yes --armor --detach-sign -o "$stage/Release.gpg" "$stage/Release"
gpg --batch --yes --clearsign -o "$stage/InRelease" "$stage/Release"
for name in Release Release.gpg InRelease; do
 install -m 0644 "$stage/$name" "dists/stable/$name.new"
 mv "dists/stable/$name.new" "dists/stable/$name"
done
gpg --batch --export > "$ROOT/mushroom-archive-keyring.gpg.new"
chmod 644 "$ROOT/mushroom-archive-keyring.gpg.new"
mv "$ROOT/mushroom-archive-keyring.gpg.new" "$ROOT/mushroom-archive-keyring.gpg"
echo 'Published signed Mushroom package indexes.'
