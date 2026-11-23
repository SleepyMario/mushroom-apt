# Mushroom APT

Signed Debian packages for Mushroom applications. Linux distribution formats are Debian packages and the separate [Gentoo overlay](https://github.com/SleepyMario/mushroom-overlay).

Repository: https://sleepymario.com/mushroom-apt/
Suite: `stable`; component: `main`; current client platform: Ubuntu 26.04 amd64.

## Build ownership

- VM 101: Linux packaging, including all .deb builds.
- VM 201: Windows packaging.
- VM 301: Android packaging.

Qylyn Client source lives in `SleepyMario/mushroom-overlay`, under `src/kylin-client`. This repository owns Debian packaging, publication and optional client update tooling. Weightrail and Streamchat are potential future packages, not currently published here.

## Rename compatibility — 2026-11-23

Qylyn (麒麟), formerly Kylin, is the same project. Official website: https://www.qylyn.com. New installs use `qylyn-client`; its dependency retains the legacy `kylin-client` package so existing updaters keep working. Both command names use identical settings, authentication and browser storage. Historical release evidence below keeps its original package names and versions. No record or settings migration is performed.

## Install

Download `mushroom-archive-keyring.gpg` from the repository URL and inspect its fingerprint before trusting it:

`6EF6 7798 E367 BBE7 93D4 FBD1 E9BC 26C3 D226 81BA`

Install it as `/etc/apt/keyrings/mushroom-archive-keyring.gpg` (root-owned, mode 0644). Create `/etc/apt/sources.list.d/mushroom.sources`:

```text
Types: deb
URIs: https://sleepymario.com/mushroom-apt/
Suites: stable
Components: main
Architectures: amd64
Signed-By: /etc/apt/keyrings/mushroom-archive-keyring.gpg
```

Run `sudo apt-get update` and `sudo apt-get install qylyn-client`. Configure the private service connection separately. Packages contain no model, server archive, credentials or user records.

## Optional automatic updates

Install `client-update/mushroom-kylin-update` in `/usr/local/sbin/` and the accompanying service/timer in `/etc/systemd/system/`. Enable `mushroom-kylin-update.timer` after daemon-reload. It checks daily and after boot, with up to 15 minutes of random delay. It refreshes only Mushroom metadata and requests an upgrade of Qylyn Client only; necessary package dependencies can be resolved by APT. It does not change Ubuntu's general update policy or restart the app. A running app uses the new version on its next launch. Existing settings and WebKit storage are retained.

## Build and publish

On VM 101, use an Ubuntu 26.04 build environment with Python 3 and dpkg-dev:

```sh
python3 scripts/build-kylin-client.py /path/to/kylin-client VERSION /path/to/output
```

Review the package contents, install and test before release. Copy the legacy .deb into the repository host's `pool/main/k/kylin-client/` and the canonical .deb into `pool/main/q/qylyn-client/`, then run `scripts/publish.sh` there. Keep previous package versions for rollback. The publisher creates signed indexes and by-hash copies. Publication is operator-controlled; clients do not build or pull arbitrary source commits.

The signing directory must remain outside the served tree, root-only. The initial signing key expires in November 2028; arrange rotation before expiry. Never commit private keys. The current release metadata does not use Valid-Until; freshness expiry and automated release production are future work.

## Initial release: 2026-11-22

- Version: `0.1.0+git20261122.875daa6-1`
- Source commit: `875daa6b6f72a51bfeef869b60227562c8bcec51`
- Built on VM 101 in Ubuntu 26.04 container.
- Container digest: `sha256:d66b366dac61b575bee2aef07e9c26e8070096fbe84a3d4d3eb0da069b5d76db`
- Package SHA256: `d36cf41d263a136acc94e35d304cd9c14f64ea5cb6b6365a61502ba135d74ea8`
- Verified signed APT installation on ThinkPad Ubuntu 26.04, client service reachability, successful updater service, active daily timer and unchanged configuration hash. Existing app and private tunnel stayed running. A fresh graphical launch of the packaged version remains a user-side verification step.

## Qylyn rename build: 2026-11-23

- Version: `0.1.0+git20261123.07bce54-1`; source commit `07bce54459ecaca6c153fe3cf2c195cbe8b29a86`.
- Both packages built on VM 101 using existing Ubuntu 26.04 image `mushroom/desktop-test@sha256:ea19d9be404c4f8472a308af2972624b6aba2e46b49632b401728adbb890f8e1`.
- All 32 client tests passed. Clean-container installation was blocked by Ubuntu mirror connectivity and an unavailable WebKit dependency in that image.
- Actual ThinkPad installation succeeded with its existing dependencies; configuration and connection-profile hashes unchanged. Both command families remain available.
- ThinkPad connection check returns HTTP 401 with both the preserved previous client and the new client. Authentication and fresh graphical launch remain unverified; no credentials were changed.
- Legacy package SHA256: `a7edaced9ac88f97321bcdf0b4467ca7b0ab2eba1eef3748f791a368ae1d1f46`.
- Canonical package SHA256: `d38bf945586d9061c947de60eea8fefff1ae44533563ae0b8adb7662683e8eb8`.
