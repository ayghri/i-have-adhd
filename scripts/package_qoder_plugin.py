#!/usr/bin/env python3
"""Build a Qoder-importable ZIP from the canonical plugin files."""

import argparse
import json
import pathlib
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".qoder-plugin" / "plugin.json"
PACKAGE_ROOTS = (ROOT / ".qoder-plugin", ROOT / "skills", ROOT / "hooks")
PACKAGE_FILES = (ROOT / "README.md", ROOT / "INSTALL.md", ROOT / "LICENSE")
IGNORED_NAMES = {".DS_Store", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def package_files() -> list[pathlib.Path]:
    files = list(PACKAGE_FILES)
    for package_root in PACKAGE_ROOTS:
        files.extend(path for path in package_root.rglob("*") if path.is_file())
    return sorted(
        {
            path
            for path in files
            if not any(part in IGNORED_NAMES for part in path.parts)
            and path.suffix not in IGNORED_SUFFIXES
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=ROOT / "dist" / "qoder",
        help="Output directory (default: <repo>/dist/qoder)",
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf8"))
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{manifest['name']}-{manifest['version']}.zip"

    with zipfile.ZipFile(
        archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for path in package_files():
            archive.write(path, path.relative_to(ROOT).as_posix())

    print(archive_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
