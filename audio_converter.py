#!/usr/bin/env python3
"""
Audio Converter

Small CLI utility for converting audio files for mobile/game development.
Primary target: .ogg -> .mp3, but supports other FFmpeg-supported formats.

Requires FFmpeg installed and available on PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_INPUT_EXT = ".ogg"
DEFAULT_OUTPUT_FORMAT = "mp3"
DEFAULT_BITRATE = "192k"


def require_ffmpeg() -> None:
    """Exit early if FFmpeg is not installed or not on PATH."""
    if shutil.which("ffmpeg") is None:
        print(
            "Error: FFmpeg was not found on PATH.\n"
            "Install FFmpeg first, then run this script again.",
            file=sys.stderr,
        )
        sys.exit(1)


def normalize_ext(value: str) -> str:
    """Normalize an extension or format string."""
    value = value.strip().lower()
    if not value:
        raise ValueError("File extension / format cannot be empty.")
    return value if value.startswith(".") else f".{value}"


def build_output_path(
    input_file: Path,
    output_dir: Path | None,
    output_format: str,
    preserve_structure_root: Path | None = None,
) -> Path:
    """Build the destination path for a converted file."""
    output_ext = normalize_ext(output_format)

    if output_dir is None:
        return input_file.with_suffix(output_ext)

    if preserve_structure_root is not None:
        relative_path = input_file.relative_to(preserve_structure_root)
        return (output_dir / relative_path).with_suffix(output_ext)

    return output_dir / input_file.with_suffix(output_ext).name


def convert_file(
    input_file: Path,
    output_file: Path,
    bitrate: str,
    overwrite: bool,
    dry_run: bool,
) -> bool:
    """Convert a single file using FFmpeg. Returns True if conversion succeeded."""
    if not input_file.exists() or not input_file.is_file():
        print(f"Skipping missing file: {input_file}")
        return False

    if output_file.exists() and not overwrite:
        print(f"Skipping existing file: {output_file}")
        return False

    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-i",
        str(input_file),
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        bitrate,
        str(output_file),
    ]

    if dry_run:
        print("DRY RUN:", " ".join(command))
        return True

    print(f"Converting: {input_file} -> {output_file}")

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"Failed: {input_file} ({exc})", file=sys.stderr)
        return False


def find_input_files(input_dir: Path, input_ext: str, recursive: bool) -> list[Path]:
    """Find matching input files in a folder."""
    pattern = f"*{normalize_ext(input_ext)}"
    iterator = input_dir.rglob(pattern) if recursive else input_dir.glob(pattern)
    return sorted(path for path in iterator if path.is_file())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert audio files for mobile/game development. Default: .ogg to .mp3."
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--file",
        type=Path,
        help="Convert one audio file.",
    )
    mode.add_argument(
        "--folder",
        type=Path,
        help="Convert all matching files in a folder.",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder. Defaults to the source file/folder location.",
    )
    parser.add_argument(
        "--input-ext",
        default=DEFAULT_INPUT_EXT,
        help="Input extension for folder mode. Default: .ogg",
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_OUTPUT_FORMAT,
        help="Output format/extension. Default: mp3",
    )
    parser.add_argument(
        "--bitrate",
        default=DEFAULT_BITRATE,
        help="Audio bitrate. Default: 192k",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search subfolders when using --folder.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing converted files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be converted without creating files.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require_ffmpeg()

    converted = 0
    failed = 0

    if args.file:
        input_file = args.file.resolve()
        output_file = build_output_path(input_file, args.output_dir, args.format)
        ok = convert_file(input_file, output_file, args.bitrate, args.overwrite, args.dry_run)
        converted += int(ok)
        failed += int(not ok)

    if args.folder:
        input_dir = args.folder.resolve()

        if not input_dir.exists() or not input_dir.is_dir():
            print(f"Error: Folder does not exist: {input_dir}", file=sys.stderr)
            return 1

        files = find_input_files(input_dir, args.input_ext, args.recursive)

        if not files:
            print(f"No {normalize_ext(args.input_ext)} files found in {input_dir}")
            return 0

        for input_file in files:
            output_file = build_output_path(
                input_file=input_file,
                output_dir=args.output_dir,
                output_format=args.format,
                preserve_structure_root=input_dir if args.output_dir and args.recursive else None,
            )
            ok = convert_file(input_file, output_file, args.bitrate, args.overwrite, args.dry_run)
            converted += int(ok)
            failed += int(not ok)

    print(f"Done. Converted: {converted}. Skipped/failed: {failed}.")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
