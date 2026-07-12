#!/usr/bin/env python3
"""
Audio Converter

Small CLI utility for converting audio files for mobile/game development.
Default no-argument behavior:
    ./sounds/*.ogg -> ./converted/<timestamp>/*.mp3

Requires FFmpeg installed and available on PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


DEFAULT_INPUT_FORMATS = ["ogg"]
DEFAULT_OUTPUT_FORMAT = "mp3"
DEFAULT_BITRATE = "192k"
DEFAULT_FOLDER = Path("sounds")
DEFAULT_OUTPUT_DIR = Path("converted")

SUPPORTED_AUDIO_FORMATS = {
    "aac",
    "aiff",
    "aif",
    "flac",
    "m4a",
    "mp3",
    "oga",
    "ogg",
    "opus",
    "wav",
    "wma",
}

# Keep codec choices explicit where it helps compatibility.
# For formats not listed here, FFmpeg will use its default encoder for that container.
AUDIO_CODECS = {
    "aac": "aac",
    "m4a": "aac",
    "mp3": "libmp3lame",
    "ogg": "libvorbis",
    "oga": "libvorbis",
    "opus": "libopus",
    "flac": "flac",
    "wav": "pcm_s16le",
}

BITRATE_FORMATS = {"aac", "m4a", "mp3", "ogg", "oga", "opus"}


class Status(str, Enum):
    CONVERTED = "converted"
    WOULD_CONVERT = "would_convert"
    ALREADY_TARGET = "already_target"
    UNSUPPORTED = "unsupported"
    OUTPUT_EXISTS = "output_exists"
    MISSING = "missing"
    FAILED = "failed"


@dataclass
class Result:
    status: Status
    source: Path
    output: Path | None = None
    message: str = ""


@dataclass
class Summary:
    results: list[Result] = field(default_factory=list)

    def add(self, result: Result) -> None:
        self.results.append(result)

    def count(self, status: Status) -> int:
        return sum(1 for item in self.results if item.status == status)

    @property
    def failed(self) -> int:
        return self.count(Status.FAILED) + self.count(Status.MISSING)

    def print(self) -> None:
        print("\nAudio conversion complete.")
        print(f"Converted: {self.count(Status.CONVERTED)}")
        print(f"Would convert: {self.count(Status.WOULD_CONVERT)}")
        print(f"Already target format: {self.count(Status.ALREADY_TARGET)}")
        print(f"Unsupported files skipped: {self.count(Status.UNSUPPORTED)}")
        print(f"Existing outputs skipped: {self.count(Status.OUTPUT_EXISTS)}")
        print(f"Missing files: {self.count(Status.MISSING)}")
        print(f"Failed: {self.count(Status.FAILED)}")


def require_ffmpeg() -> None:
    """Exit early if FFmpeg is not installed or not on PATH."""
    if shutil.which("ffmpeg") is None:
        print(
            "Error: FFmpeg was not found on PATH.\n"
            "Install FFmpeg first, then run this script again.",
            file=sys.stderr,
        )
        sys.exit(1)


def normalize_format(value: str) -> str:
    """Normalize an extension or format string to a lowercase format without a dot."""
    value = value.strip().lower().lstrip(".")
    if not value:
        raise ValueError("File extension / format cannot be empty.")
    return value


def normalize_formats(values: list[str] | None) -> set[str]:
    """Normalize a list of extensions/formats."""
    if not values:
        return set()
    return {normalize_format(value) for value in values}


def extension_for(format_name: str) -> str:
    return f".{normalize_format(format_name)}"


def make_run_folder(base_output_dir: Path, enabled: bool) -> Path:
    """Create a timestamped output folder for this conversion run."""
    if not enabled:
        return base_output_dir

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return base_output_dir / f"converted_{timestamp}"


def resolve_output_base(args: argparse.Namespace, no_args: bool) -> Path | None:
    """
    Return the base output folder.

    Normal behavior:
    - If --output-dir is set, use it.
    - If no options are provided, use ./converted.
    - Otherwise save beside source files.
    """
    if args.output_dir is not None:
        return args.output_dir
    if no_args:
        return DEFAULT_OUTPUT_DIR
    return None


def build_output_path(
    input_file: Path,
    output_dir: Path | None,
    output_format: str,
    preserve_structure_root: Path | None = None,
) -> Path:
    """Build the destination path for a converted file."""
    output_ext = extension_for(output_format)

    if output_dir is None:
        return input_file.with_suffix(output_ext)

    if preserve_structure_root is not None:
        relative_path = input_file.relative_to(preserve_structure_root)
        return (output_dir / relative_path).with_suffix(output_ext)

    return output_dir / input_file.with_suffix(output_ext).name


def build_ffmpeg_command(
    input_file: Path,
    output_file: Path,
    output_format: str,
    bitrate: str,
    overwrite: bool,
) -> list[str]:
    """Build an FFmpeg command for the requested output format."""
    format_name = normalize_format(output_format)
    codec = AUDIO_CODECS.get(format_name)

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-i",
        str(input_file),
        "-vn",
    ]

    if codec:
        command.extend(["-codec:a", codec])

    if bitrate and format_name in BITRATE_FORMATS:
        command.extend(["-b:a", bitrate])

    command.append(str(output_file))
    return command


def convert_file(
    input_file: Path,
    output_file: Path,
    output_format: str,
    bitrate: str,
    overwrite: bool,
    dry_run: bool,
) -> Result:
    """Convert a single file using FFmpeg."""
    if not input_file.exists() or not input_file.is_file():
        print(f"[MISSING]   {input_file}")
        return Result(Status.MISSING, input_file, output_file, "Source file was not found.")

    source_format = normalize_format(input_file.suffix)
    target_format = normalize_format(output_format)

    if source_format == target_format:
        print(f"[SKIPPED]   {input_file} - already .{target_format}")
        return Result(
            Status.ALREADY_TARGET,
            input_file,
            input_file,
            f"File was already .{target_format} format.",
        )

    if output_file.exists() and not overwrite:
        print(f"[SKIPPED]   {input_file} - output already exists: {output_file}")
        return Result(Status.OUTPUT_EXISTS, input_file, output_file, "Output already exists.")

    command = build_ffmpeg_command(input_file, output_file, output_format, bitrate, overwrite)

    if dry_run:
        print(f"[DRY RUN]   {input_file} -> {output_file}")
        print("            " + " ".join(command))
        return Result(Status.WOULD_CONVERT, input_file, output_file, "Dry run only.")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"[CONVERT]   {input_file} -> {output_file}")

    try:
        subprocess.run(command, check=True)
        return Result(Status.CONVERTED, input_file, output_file)
    except subprocess.CalledProcessError as exc:
        print(f"[FAILED]    {input_file} ({exc})", file=sys.stderr)
        return Result(Status.FAILED, input_file, output_file, str(exc))


def find_folder_files(
    input_dir: Path,
    input_formats: set[str],
    all_audio: bool,
    recursive: bool,
) -> list[Result]:
    """Find files for folder mode and mark unsupported files clearly."""
    iterator = input_dir.rglob("*") if recursive else input_dir.glob("*")
    results: list[Result] = []

    for path in sorted(item for item in iterator if item.is_file()):
        source_format = normalize_format(path.suffix)

        if all_audio:
            if source_format in SUPPORTED_AUDIO_FORMATS:
                results.append(Result(Status.WOULD_CONVERT, path))
            else:
                results.append(Result(Status.UNSUPPORTED, path, message="Unsupported file type."))
        else:
            if source_format in input_formats:
                results.append(Result(Status.WOULD_CONVERT, path))
            elif source_format in SUPPORTED_AUDIO_FORMATS:
                results.append(Result(Status.UNSUPPORTED, path, message="Audio file does not match selected input format filter."))
            else:
                results.append(Result(Status.UNSUPPORTED, path, message="Unsupported file type."))

    return results


def print_unsupported(result: Result) -> None:
    print(f"[SKIPPED]   {result.source} - {result.message}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert audio files for mobile/game development. "
            "Default with no options: ./sounds/*.ogg -> ./converted/<timestamp>/*.mp3."
        )
    )

    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument(
        "--file",
        type=Path,
        help="Convert one audio file.",
    )
    mode.add_argument(
        "--folder",
        type=Path,
        help="Convert matching files in a folder.",
    )

    input_mode = parser.add_mutually_exclusive_group(required=False)
    input_mode.add_argument(
        "--all-audio",
        action="store_true",
        help="Convert every supported audio file found in folder mode.",
    )
    input_mode.add_argument(
        "--input-formats",
        nargs="+",
        default=None,
        help="Folder mode filter. Example: --input-formats ogg wav flac",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder. Defaults to source location, except no-argument mode uses ./converted.",
    )
    parser.add_argument(
        "--format",
        default=DEFAULT_OUTPUT_FORMAT,
        help="Output format/extension. Default: mp3",
    )
    parser.add_argument(
        "--bitrate",
        default=DEFAULT_BITRATE,
        help="Audio bitrate for compressed formats. Default: 192k",
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
    parser.add_argument(
        "--no-run-folder",
        action="store_true",
        help="Do not create a timestamped subfolder inside --output-dir.",
    )

    args = parser.parse_args(argv)

    if not args.file and not args.folder and argv:
        parser.error("Choose --file or --folder, or run with no options for the default ./sounds/*.ogg conversion.")

    if args.file and (args.all_audio or args.input_formats):
        parser.error("--all-audio and --input-formats are only used with --folder mode.")

    return args


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    no_args = len(argv) == 0
    args = parse_args(argv)
    require_ffmpeg()

    if no_args:
        args.folder = DEFAULT_FOLDER
        args.output_dir = DEFAULT_OUTPUT_DIR
        args.input_formats = DEFAULT_INPUT_FORMATS
        args.format = DEFAULT_OUTPUT_FORMAT
        print("No options supplied. Using default conversion:")
        print(f"  Input:  ./{DEFAULT_FOLDER}/*.ogg")
        print(f"  Output: ./{DEFAULT_OUTPUT_DIR}/converted_<timestamp>/*.mp3\n")

    output_format = normalize_format(args.format)
    output_base = resolve_output_base(args, no_args)
    create_run_folder = output_base is not None and not args.no_run_folder
    output_dir = make_run_folder(output_base.resolve(), create_run_folder) if output_base else None

    if output_dir:
        print(f"Output folder: {output_dir}")

    summary = Summary()

    if args.file:
        input_file = args.file.resolve()
        output_file = build_output_path(input_file, output_dir, output_format)
        summary.add(convert_file(input_file, output_file, output_format, args.bitrate, args.overwrite, args.dry_run))

    if args.folder:
        input_dir = args.folder.resolve()

        if not input_dir.exists() or not input_dir.is_dir():
            print(f"Error: Folder does not exist: {input_dir}", file=sys.stderr)
            return 1

        input_formats = normalize_formats(args.input_formats) or set(DEFAULT_INPUT_FORMATS)
        folder_results = find_folder_files(
            input_dir=input_dir,
            input_formats=input_formats,
            all_audio=args.all_audio,
            recursive=args.recursive,
        )

        if not folder_results:
            print(f"No files found in {input_dir}")
            return 0

        if not args.all_audio:
            formats_text = ", ".join(f".{item}" for item in sorted(input_formats))
            print(f"Input filter: {formats_text}")
        else:
            print("Input filter: all supported audio formats")

        for result in folder_results:
            if result.status == Status.UNSUPPORTED:
                print_unsupported(result)
                summary.add(result)
                continue

            input_file = result.source
            output_file = build_output_path(
                input_file=input_file,
                output_dir=output_dir,
                output_format=output_format,
                preserve_structure_root=input_dir if output_dir and args.recursive else None,
            )
            summary.add(convert_file(input_file, output_file, output_format, args.bitrate, args.overwrite, args.dry_run))

    summary.print()
    return 0 if summary.failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
