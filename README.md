# Audio Converter

A small Python command-line utility for converting audio files for mobile and game development.

Primary use case: converting `.ogg` files to `.mp3` for mobile-friendly audio pipelines.

The tool can also export to:

- `.mp3`
- `.wav`
- `.ogg`
- `.m4a`
- `.aac`
- `.flac`

This is intentionally a small utility, not a full digital audio workstation, editor, tag manager, or batch mastering tool. Tiny hammer, specific nail.

## Scope

This project is intentionally simple:

- Convert a single audio file.
- Convert every matching file in a folder.
- Optionally search folders recursively.
- Default conversion is `.ogg` to `.mp3`.
- Supports common output formats useful for games and mobile workflows.
- Uses FFmpeg for reliable audio conversion.

Out of scope for now:

- GUI app
- Metadata/tag editing
- Audio trimming
- Normalization/mastering
- Cloud upload
- Asset library management
- Auto-import into game engines

## Requirements

- Python 3.10 or newer recommended.
- FFmpeg installed separately and available on your system PATH.

FFmpeg website:

```text
https://ffmpeg.org/
```

## Install FFmpeg

macOS with Homebrew:

```bash
brew install ffmpeg
```

Windows with winget:

```powershell
winget install Gyan.FFmpeg
```

Windows with Chocolatey:

```powershell
choco install ffmpeg
```

Ubuntu / Debian Linux:

```bash
sudo apt update
sudo apt install ffmpeg
```

Fedora Linux:

```bash
sudo dnf install ffmpeg
```

Arch Linux:

```bash
sudo pacman -S ffmpeg
```

Check FFmpeg is available after installing:

```bash
ffmpeg -version
```

If that command prints FFmpeg version information, the converter is ready to use.

## Files

```text
audio_converter.py
README.md
```

## Basic Usage

Convert one `.ogg` file to `.mp3` in the same folder:

```bash
python audio_converter.py --file sounds/jump.ogg
```

Convert one file into a specific output folder:

```bash
python audio_converter.py --file sounds/jump.ogg --output-dir converted
```

Convert all `.ogg` files in a folder:

```bash
python audio_converter.py --folder sounds
```

Convert all `.ogg` files in a folder and its subfolders:

```bash
python audio_converter.py --folder sounds --recursive --output-dir converted
```

Overwrite existing converted files:

```bash
python audio_converter.py --folder sounds --overwrite
```

Preview what would happen without converting anything:

```bash
python audio_converter.py --folder sounds --recursive --dry-run
```

## Output Formats

Supported output formats:

| Format | Codec | Best For |
| ------ | ----- | -------- |
| `mp3` | `libmp3lame` | Mobile-friendly compressed audio, general compatibility |
| `wav` | `pcm_s16le` | Editing, Unity-friendly source/intermediate files |
| `ogg` | `libvorbis` | Desktop/web/game-engine audio workflows |
| `m4a` | `aac` | Mobile-friendly compressed audio, especially Apple-heavy workflows |
| `aac` | `aac` | Raw AAC output when specifically needed |
| `flac` | `flac` | Lossless archive/intermediate files |

The default output format is:

```text
mp3
```

## Options

| Option | Purpose |
| ------ | ------- |
| `--file` | Convert one file. |
| `--folder` | Convert all matching files in a folder. |
| `--output-dir` | Place converted files in a chosen folder. |
| `--input-ext` | Input extension for folder mode. Default: `.ogg`. |
| `--format` | Output format. Supported: `mp3`, `wav`, `ogg`, `m4a`, `aac`, `flac`. Default: `mp3`. |
| `--bitrate` | Audio bitrate for lossy formats. Default: `192k`. |
| `--recursive` | Include subfolders in folder mode. |
| `--overwrite` | Replace existing output files. |
| `--dry-run` | Print conversion commands without running them. |

## Recommended Mobile Defaults

For most mobile game sound effects and short music clips:

```bash
python audio_converter.py --folder audio_raw --recursive --output-dir audio_mobile --format mp3 --bitrate 192k
```

For smaller files, try:

```bash
python audio_converter.py --folder audio_raw --recursive --output-dir audio_mobile --format mp3 --bitrate 128k
```

Use your ears. A laser pew-pew does not need audiophile treatment.

## Example Format Conversions

Convert `.ogg` files to `.mp3`:

```bash
python audio_converter.py --folder audio_raw --recursive --output-dir audio_mp3 --format mp3
```

Convert `.ogg` files to `.wav`:

```bash
python audio_converter.py --folder audio_raw --recursive --output-dir audio_wav --format wav
```

Convert `.ogg` files to `.m4a`:

```bash
python audio_converter.py --folder audio_raw --recursive --output-dir audio_m4a --format m4a
```

Convert `.ogg` files to `.flac`:

```bash
python audio_converter.py --folder audio_raw --recursive --output-dir audio_flac --format flac
```

Convert `.wav` files to `.mp3`:

```bash
python audio_converter.py --folder audio_raw --input-ext wav --recursive --output-dir audio_mp3 --format mp3
```

## Notes

- MP3 is broadly compatible across mobile platforms.
- WAV is useful for editing and clean source/intermediate assets.
- OGG is useful in many game and web workflows, but may not be ideal for every mobile target.
- M4A/AAC can be useful for mobile-focused workflows.
- FLAC is useful when you want lossless compression.
- Keep original audio files as source assets.
- Export converted files into a separate folder when possible.
- Use `--dry-run` before large batch conversions.
- Use `--overwrite` only when you are sure you want to replace existing files.

## Current Status

Current working milestone:

```text
Single file conversion -> folder conversion -> recursive batch conversion -> safe overwrite handling -> dry run support -> common output formats
```

This tool is considered useful as a local CLI helper for game/audio asset prep.
