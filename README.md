# Audio Converter

A small Python command-line utility for converting audio files for mobile and game development.

Primary use case: converting `.ogg` files to `.mp3` for mobile-friendly audio pipelines.

## Scope

This project is intentionally simple:

- Convert a single audio file.
- Convert every matching file in a folder.
- Optionally search folders recursively.
- Default conversion is `.ogg` to `.mp3`.
- Uses FFmpeg for reliable audio conversion.

This is not intended to be a full digital audio workstation, editor, tag manager, or batch mastering tool. Tiny hammer, specific nail.

## Requirements

- Python 3.10 or newer recommended.
- FFmpeg installed separately and available on your system PATH.

FFmpeg website:

```text
https://ffmpeg.org/
```

### Install FFmpeg

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

## Options

| Option         | Purpose                                           |
| -------------- | ------------------------------------------------- |
| `--file`       | Convert one file.                                 |
| `--folder`     | Convert all matching files in a folder.           |
| `--output-dir` | Place converted files in a chosen folder.         |
| `--input-ext`  | Input extension for folder mode. Default: `.ogg`. |
| `--format`     | Output format. Default: `mp3`.                    |
| `--bitrate`    | Audio bitrate. Default: `192k`.                   |
| `--recursive`  | Include subfolders in folder mode.                |
| `--overwrite`  | Replace existing output files.                    |
| `--dry-run`    | Print conversion commands without running them.   |

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

## Notes

- MP3 is broadly compatible across mobile platforms.
- Keep original `.ogg` files as source assets.
- Export converted files into a separate folder when possible.
- If you later want AAC/M4A support, the script can be extended.
