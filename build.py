"""Build the VPM zip and refresh index.json for the MCP for Unity package.

Usage:
    python build.py

Reads Packages/com.coplaydev.unity-mcp/package.json, writes
dist/<name>-<version>.zip, and adds/updates that version in index.json
(the VPM repository listing that VCC / ALCOM consume).
"""

import hashlib
import json
import zipfile
from pathlib import Path

OWNER = "haroon911"
REPO = "unity-mcp-vpm"
LISTING_ID = "com.haroon911.unity-mcp-vpm"
LISTING_NAME = "MCP for Unity (VPM mirror)"
BRANCH = "main"

ROOT = Path(__file__).resolve().parent
PKG_DIR = ROOT / "Packages" / "com.coplaydev.unity-mcp"
DIST = ROOT / "dist"
INDEX = ROOT / "index.json"

LISTING_URL = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/index.json"


def build_zip(name: str, version: str) -> Path:
    DIST.mkdir(exist_ok=True)
    zip_path = DIST / f"{name}-{version}.zip"
    # Forward-slash entry names and package.json at the zip root, as VPM requires.
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(PKG_DIR.rglob("*")):
            if file.is_file():
                zf.write(file, file.relative_to(PKG_DIR).as_posix())
    return zip_path


def load_listing() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {
        "name": LISTING_NAME,
        "id": LISTING_ID,
        "author": OWNER,
        "url": LISTING_URL,
        "packages": {},
    }


def main() -> None:
    pkg = json.loads((PKG_DIR / "package.json").read_text(encoding="utf-8"))
    name, version = pkg["name"], pkg["version"]

    zip_path = build_zip(name, version)
    sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    asset_url = (
        f"https://github.com/{OWNER}/{REPO}/releases/download/v{version}/{zip_path.name}"
    )

    listing = load_listing()
    package_entry = listing["packages"].setdefault(name, {"versions": {}})
    package_entry["versions"][version] = {**pkg, "url": asset_url, "zipSHA256": sha256}

    INDEX.write_text(json.dumps(listing, indent=2) + "\n", encoding="utf-8")

    print(f"Built   {zip_path}")
    print(f"SHA256  {sha256}")
    print(f"Listing {INDEX}")
    print(f"Add this URL in VCC/ALCOM: {LISTING_URL}")


if __name__ == "__main__":
    main()
