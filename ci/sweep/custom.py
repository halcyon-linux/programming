"""The custom version feeds for the programming registry.

Each function implements one upstream whose version discovery cannot be
expressed by the generic github-release/github-tag feeds. Only feeds
referenced by an [updates] table in ci/packages.toml belong here; `sweep.py
--check` rejects an unreferenced custom_* function.
"""

from __future__ import annotations

import re
from pathlib import Path

import feeds
from spec import SpecFile


def _custom_zig_minor(spec: SpecFile, minor: str) -> None:
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    versions = [
        tag for tag in feeds.github_tag_names("ziglang/zig")
        if re.fullmatch(rf"{re.escape(minor)}\.[0-9]+", tag)
    ]
    versions.sort(key=cmp_to_key(rpmvercmp), reverse=True)
    if not versions:
        raise feeds.FeedError(f"zig{minor.replace('.', '')}: no {minor}.x release tags")
    spec.set_version(versions[0])


def custom_zig015(spec: SpecFile, pkg_dir: Path) -> None:
    _custom_zig_minor(spec, "0.15")


def custom_zig017(spec: SpecFile, pkg_dir: Path) -> None:
    _custom_zig_minor(spec, "0.17")


def _astral_binary_feed(spec: SpecFile, repo: str, pkg_name: str) -> None:
    """Astral (ty/ruff) binary feed: GitHub releases with tar.gz assets."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/{repo}/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        version = tag.removeprefix("v")
        if not re.fullmatch(r"[0-9][0-9.]*", version):
            continue

        # Check for the x86_64-unknown-linux-gnu.tar.gz asset
        expected_asset = f"{pkg_name}-x86_64-unknown-linux-gnu.tar.gz"
        for asset in release.get("assets", []):
            if asset.get("name") == expected_asset:
                digest = asset.get("digest", "")
                if digest.startswith("sha256:"):
                    digest = digest[len("sha256:"):]
                else:
                    digest = "none"
                spec.set_version(version)
                if spec.get_global("digest") is not None:
                    spec.set_global("digest", digest)
                return
    raise feeds.FeedError(
        f"{pkg_name}: no stable release in the last 30 ships its x86_64-linux-gnu archive")


def custom_ty(spec: SpecFile, pkg_dir: Path) -> None:
    _astral_binary_feed(spec, "astral-sh/ty", "ty")


def custom_ruff(spec: SpecFile, pkg_dir: Path) -> None:
    _astral_binary_feed(spec, "astral-sh/ruff", "ruff")


def custom_uv(spec: SpecFile, pkg_dir: Path) -> None:
    """uv binary feed: GitHub releases with tar.gz assets."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/astral-sh/uv/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        version = tag.removeprefix("v")
        if not re.fullmatch(r"[0-9][0-9.]*", version):
            continue

        # Check for the x86_64-unknown-linux-musl.tar.gz asset
        expected_asset = "uv-x86_64-unknown-linux-musl.tar.gz"
        for asset in release.get("assets", []):
            if asset.get("name") == expected_asset:
                digest = asset.get("digest", "")
                if digest.startswith("sha256:"):
                    digest = digest[len("sha256:"):]
                else:
                    digest = "none"
                spec.set_version(version)
                if spec.get_global("digest") is not None:
                    spec.set_global("digest", digest)
                return
    raise feeds.FeedError(
        "uv: no stable release in the last 30 ships its x86_64-linux-musl archive")


def custom_pyrefly(spec: SpecFile, pkg_dir: Path) -> None:
    """Pyrefly binary feed: GitHub releases with tar.gz assets."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/meta/pyrefly/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        version = tag.removeprefix("v")
        if not re.fullmatch(r"[0-9][0-9.]*", version):
            continue

        # Check for the linux-x86_64.tar.gz asset
        expected_asset = "pyrefly-linux-x86_64.tar.gz"
        for asset in release.get("assets", []):
            if asset.get("name") == expected_asset:
                digest = asset.get("digest", "")
                if digest.startswith("sha256:"):
                    digest = digest[len("sha256:"):]
                else:
                    digest = "none"
                spec.set_version(version)
                if spec.get_global("digest") is not None:
                    spec.set_global("digest", digest)
                return
    raise feeds.FeedError(
        "pyrefly: no stable release in the last 30 ships its linux-x86_64 archive")


def custom_pixi(spec: SpecFile, pkg_dir: Path) -> None:
    """pixi binary feed: GitHub releases with tar.gz assets."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/prefix-dev/pixi/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        version = tag.removeprefix("v")
        if not re.fullmatch(r"[0-9][0-9.]*", version):
            continue

        # Check for the x86_64-unknown-linux-musl.tar.gz asset
        expected_asset = "pixi-x86_64-unknown-linux-musl.tar.gz"
        for asset in release.get("assets", []):
            if asset.get("name") == expected_asset:
                spec.set_version(version)
                return
    raise feeds.FeedError(
        "pixi: no stable release in the last 30 ships its x86_64-linux-musl archive")


def custom_bun(spec: SpecFile, pkg_dir: Path) -> None:
    """bun binary feed: GitHub releases with zip assets."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/oven-sh/bun/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        version = tag.removeprefix("bun-v")
        if not re.fullmatch(r"[0-9][0-9.]*", version):
            continue

        # Check for the linux-x64-baseline.zip asset
        expected_asset = "bun-linux-x64-baseline.zip"
        for asset in release.get("assets", []):
            if asset.get("name") == expected_asset:
                spec.set_version(version)
                return
    raise feeds.FeedError(
        "bun: no stable release in the last 30 ships its linux-x64-baseline archive")


def custom_marksman(spec: SpecFile, pkg_dir: Path) -> None:
    """Marksman binary feed: GitHub releases with date-based tags."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/artempyanykh/marksman/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        # marksman uses date-based tags like 2026-02-08
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", tag):
            continue

        # Check for the linux-x64 asset
        expected_asset = "marksman-linux-x64"
        for asset in release.get("assets", []):
            if asset.get("name") == expected_asset:
                # Convert date tag to dot format for RPM version
                version = tag.replace("-", ".")
                spec.set_version(version)
                spec.set_global("markstag", tag)
                return
    raise feeds.FeedError(
        "marksman: no stable release in the last 30 ships its linux-x64 binary")


def custom_texlab(spec: SpecFile, pkg_dir: Path) -> None:
    """texlab source build feed: GitHub releases with tag-based tarballs."""
    from functools import cmp_to_key
    from vercmp import rpmvercmp

    releases = feeds.fetch_json(
        f"https://api.github.com/repos/latex-lsp/texlab/releases?per_page=30")
    for release in releases:
        if release.get("draft") or release.get("prerelease"):
            continue
        tag = release.get("tag_name", "")
        version = tag.removeprefix("v")
        if not re.fullmatch(r"[0-9][0-9.]*", version):
            continue

        # Verify the source tarball exists
        url = f"https://github.com/latex-lsp/texlab/archive/refs/tags/{tag}.tar.gz"
        if feeds.head_probe(url):
            spec.set_version(version)
            return
    raise feeds.FeedError(
        "texlab: no stable release in the last 30 ships its source tarball")