#!/usr/bin/env python3
"""Build the architecture-independent client on Linux packaging VM 101."""
import argparse
import pathlib
import shutil
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('source', type=pathlib.Path)
p.add_argument('version')
p.add_argument('output', type=pathlib.Path)
a = p.parse_args()
subprocess.run(['dpkg', '--validate-version', a.version], check=True)
a.output.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='kylin-deb-') as temp:
    root = pathlib.Path(temp)
    def put(path, text, mode=0o644):
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        dest.chmod(mode)
    shutil.copytree(a.source / 'src/kylin_client', root / 'usr/lib/kylin-client/kylin_client', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    put('usr/bin/kylin-client', '#!/bin/sh\nPYTHONPATH="/usr/lib/kylin-client${PYTHONPATH:+:$PYTHONPATH}" exec /usr/bin/python3 -m kylin_client.client "$@"\n', 0o755)
    put('usr/bin/kylin-client-tunnel', '#!/bin/sh\nPYTHONPATH="/usr/lib/kylin-client${PYTHONPATH:+:$PYTHONPATH}" exec /usr/bin/python3 -m kylin_client.tunnel "$@"\n', 0o755)
    for src, dest in [('share/com.sleepymario.KylinClient.desktop', 'usr/share/applications/com.sleepymario.KylinClient.desktop'), ('share/kylin-client.svg', 'usr/share/icons/hicolor/scalable/apps/kylin-client.svg'), ('LICENSE', 'usr/share/doc/kylin-client/copyright')]:
        target = root / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(a.source / src, target)
    put('DEBIAN/control', f'''Package: kylin-client
Version: {a.version}
Section: net
Priority: optional
Architecture: all
Maintainer: SleepyMario <admin@sleepymario.com>
Depends: openssh-client, python3 (>= 3.11), python3-gi, gir1.2-gtk-3.0, gir1.2-webkit2-4.1
Homepage: https://github.com/SleepyMario/mushroom-overlay
Description: Desktop client for a central Kylin service
 GTK and WebKitGTK client with themes, zoom, and shared conversations.
 Server, model, credentials and user records are not included.
''')
    subprocess.run(['dpkg-deb', '--root-owner-group', '--build', str(root), str(a.output / f'kylin-client_{a.version}_all.deb')], check=True)
