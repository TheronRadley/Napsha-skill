#!/usr/bin/env python3
"""Build the two-file skill ZIP reproducibly, without evaluation material."""
from pathlib import Path
import hashlib
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'ai-subjectivity-inquiry'


def main():
    meta = yaml.safe_load((SKILL / 'SKILL.md').read_text().split('---', 2)[1])
    version = meta['metadata']['version']
    target = ROOT / 'dist' / f'ai-subjectivity-inquiry-v{version}.zip'
    target.parent.mkdir(exist_ok=True)
    members = [SKILL / 'SKILL.md', SKILL / 'references/respect-under-uncertainty.md']
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in members:
            info = zipfile.ZipInfo(path.relative_to(SKILL.parent).as_posix(),
                                   date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    checksum = hashlib.sha256(target.read_bytes()).hexdigest()
    (ROOT / 'dist/SHA256SUMS.txt').write_text(f'{checksum}  {target.name}\n')
    print(f'Built {target.relative_to(ROOT)} ({target.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
