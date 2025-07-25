#!/usr/bin/env -S uv run --script

from itertools import chain
from pathlib import Path
import argparse
import hashlib

ROOT_INDEX_HTML = """
<!DOCTYPE html>
<html>
  <body>
{links}
  </body>
</html>
""".strip()

PACKAGE_INDEX_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Links for {name}</title>
  </head>
  <body>
    <h1>Links for {name}</h1>
{links}
  </body>
</html>
""".strip()


def calc_sha256(file_path):
    hasher = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)

    return hasher.hexdigest()


def index_package(package_dir: Path) -> bool:
    links = []

    for path in sorted(chain(package_dir.glob("*.tar.gz"), package_dir.glob("*.whl"))):
        if path.is_file():
            sha256 = calc_sha256(path)
            links.append(f'    <a href="{path}#sha256={sha256}">{path.name}</a><br>')

    with open(package_dir / "index.html", "w") as file:
        print(
            PACKAGE_INDEX_HTML.format(name=package_dir.name, links="\n".join(links)),
            file=file,
        )

    return len(links) > 0


def write_root_index(root: Path, packages: list[str]):
    links = [f'    <a href="/{name}/">{name}</a>' for name in packages]

    with open(root / "index.html", "w") as file:
        print(ROOT_INDEX_HTML.format(links="\n".join(links)), file=file)


def main(args):
    root = Path(args.repo_dir)
    packages = []

    for item in root.iterdir():
        if not item.is_dir():
            continue

        if index_package(item):
            packages.append(item.name)
            print(f"indexed package: {item.name}")

    write_root_index(root, packages)
    print(f"indexed {len(packages)} packages")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PEP-503 Python package repository index files")
    parser.add_argument("repo_dir", type=Path, help="Path to PyPI repo dir")
    main(parser.parse_args())
