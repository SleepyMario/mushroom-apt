# Nightly Docker builds

The owner reauthorized nightly Docker publication on 2026-11-22. Linux builds use VM101; VM201 is Windows and VM301 Android. This infrastructure is shared packaging support, not another application project.

The hv host timer runs at 01:00 Asia/Taipei. The host launcher starts VM101 if stopped, waits for the guest agent, invokes its serialized oneshot build service, and propagates failure. It leaves the builder running to avoid interrupting unrelated work. Persistent timers catch missed runs when hv returns.

The VM101 service runs as ashwin with Docker access, Nice19 and idle I/O scheduling. It builds Weightrail, Streamchat CLI/server, then WSM. Sources are dedicated clean checkouts under ~/Builds/mushroom-nightly/sources, updated by fast-forward only. Existing development worktrees are not used. Existing builder SSH access fetches required WSM curricula. Existing Docker Hub credentials remain outside this repository.

Published images:

- sleepiestmario/weightrail:nightly
- sleepiestmario/streamchat-cli:nightly
- sleepiestmario/streamchat-server:nightly
- sleepiestmario/whacksmacker:nightly

Each gets a dated nightly-UTC_TIMESTAMP-SOURCE_COMMIT tag first. The dated registry digest must verify before the moving nightly tag is pushed; that digest is checked too. Stable/latest/versioned release tags are untouched. Nightly timestamps are development identifiers, not independent platform release versions.

WSM runs its existing test:docker suite and exports its curated Docker context. Publication checks executable help, with an isolated WSM web health check. Weightrail records and reads back disposable sample measurements. Streamchat images compile both intended targets and pass CLI help; this does not test live Twitch/Kick/YouTube/Discord credentials or integrations. No user data mounts or public listening ports are used.

Logs: VM101 ~/Builds/mushroom-nightly/logs/. hv and VM101 systemd units expose failure. Failed projects do not prevent the remaining projects being attempted; the overall run still fails. Build preparation refuses less than3GiB free. Generated WSM context is removed before upload. Existing images/volumes are not automatically pruned; builder disk capacity needs monitoring. No release numbering changes are made here.

Install the runner as /usr/local/bin/mushroom-docker-nightly and its service on VM101. Install the host launcher as /usr/local/sbin/mushroom-docker-nightly-host plus host service/timer on hv. Enable the host timer only after validating the build environment. All private SSH/registry setup is separate.
