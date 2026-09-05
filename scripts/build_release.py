#!/usr/bin/env python3
"""Build/check reproducible release assets from one clean, immutable Git commit.

No tags, releases, network requests, installations or deployments are performed.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import tempfile
import zipfile

from asset_validation import validate_png
from build_skills import check as check_generated
from runtime_validate import PLUGIN_RELATIVE, ROOT, validate_package
from validate import validate_directory


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(['git', *args], cwd=root, check=False, capture_output=True)
    if result.returncode:
        raise ValueError('git command failed: ' + result.stderr.decode('utf-8', errors='replace').strip())
    return result.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_bytes(files: dict[str, tuple[bytes, int]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, (data, mode) in sorted(files.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (0o100000 | mode) << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def source_snapshot(root: Path, commit: str, destination: Path) -> dict[str, tuple[bytes, int]]:
    files = {}
    with tarfile.open(fileobj=io.BytesIO(git(root, 'archive', '--format=tar', commit))) as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            if name.is_absolute() or '..' in name.parts or '\\' in member.name:
                raise ValueError('unsafe source archive path')
            if member.isdir():
                continue
            if not member.isfile() or member.name in files:
                raise ValueError('source must contain only unique regular files')
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError('source archive file has no data')
            data = handle.read()
            mode = 0o755 if member.mode & 0o111 else 0o644
            files[member.name] = (data, mode)
            path = destination / member.name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return files


def release_artifacts(root: Path = ROOT) -> dict[str, bytes]:
    if git(root, 'status', '--porcelain', '--untracked-files=normal'):
        raise ValueError('release requires a clean Git worktree and index')
    commit = git(root, 'rev-parse', 'HEAD').decode().strip()
    tree = git(root, 'rev-parse', 'HEAD^{tree}').decode().strip()
    with tempfile.TemporaryDirectory(prefix='servotab-release-') as raw:
        snapshot = Path(raw)
        source = source_snapshot(root, commit, snapshot)
        version = (snapshot / 'VERSION').read_text().strip()
        if not re.fullmatch(r'0|[1-9][0-9]*', version.split('.')[0]) or not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version):
            raise ValueError('release VERSION must be a stable numeric major.minor.patch')
        errors = check_generated(snapshot)
        errors += validate_directory(snapshot / PLUGIN_RELATIVE / 'skills')
        errors += validate_package(snapshot)
        for name, size in (('composer-icon.png', (512, 512)), ('logo.png', (1024, 1024))):
            errors += validate_png(snapshot / PLUGIN_RELATIVE / 'assets' / name, size)
        if errors:
            raise ValueError('release validation failed:\n- ' + '\n- '.join(errors))
        manifest = json.loads((snapshot / 'PACK_MANIFEST.json').read_text())
        plugin_files = {
            'servotab/' + str(PurePosixPath(entry['path']).relative_to(PLUGIN_RELATIVE.as_posix())): source[entry['path']]
            for entry in manifest['files']
        }
        # Source ZIP carries the marketplace and maintainer tooling. The portal ZIP
        # contains ONLY the manifest-owned 69-file plugin payload.
        outputs = {
            f'servotab-{version}-plugin.zip': zip_bytes(plugin_files),
            f'servotab-{version}-source.zip': zip_bytes({f'servotab-{version}/{name}': item for name, item in source.items()}),
        }
        receipt = {
            'schema_version': 1,
            'product': 'servotab',
            'version': version,
            'source_commit': commit,
            'source_tree': tree,
            'package_file_count': len(plugin_files),
            'pack_manifest_sha256': sha256(source['PACK_MANIFEST.json'][0]),
            'assets': {name: {'size': len(data), 'sha256': sha256(data)} for name, data in sorted(outputs.items())},
            'evidence_scope': 'Reproducible source and validated package identity only; no host, model-behavior, deployment or publication claim.',
        }
        outputs['release-receipt.json'] = (json.dumps(receipt, indent=2, sort_keys=True) + '\n').encode()
        outputs['SHA256SUMS'] = ''.join(f'{sha256(data)}  {name}\n' for name, data in sorted(outputs.items())).encode()
        return outputs


def build(root: Path, output: Path, *, check: bool = False) -> None:
    expected = release_artifacts(root)
    if check:
        if output.is_symlink() or not output.is_dir() or {p.name for p in output.iterdir()} != set(expected):
            raise ValueError('release output must contain exactly the four expected artifacts')
        for name, data in expected.items():
            path = output / name
            if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
                raise ValueError(f'release artifact mismatch: {name}')
        return
    # Refuse overwrites. Compute and validate everything before creating output.
    output.mkdir(parents=True, exist_ok=False)
    for name, data in expected.items():
        with (output / name).open('xb') as handle:
            handle.write(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--check', action='store_true', help='Compare existing assets byte-for-byte; never overwrite')
    args = parser.parse_args()
    try:
        build(ROOT, args.output, check=args.check)
    except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as exc:
        print(f'ERROR: {exc}')
        return 1
    print('Release artifacts verified.' if args.check else 'Built four reproducible release artifacts.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
